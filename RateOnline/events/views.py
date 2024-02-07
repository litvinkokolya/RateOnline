from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum, Max, F, Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from events.mixins import PhotoRequiredMixin
from events.models import MemberNomination, Result, NominationAttribute, EventStaff, CategoryNomination, Category, \
    Member, MemberNominationPhoto, Event
from .forms import UploadPhotoForm
from django.forms import formset_factory


class MasterPageView(LoginRequiredMixin, PhotoRequiredMixin, TemplateView):
    template_name = "events/master_page.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user = self.request.user
        data['my_jobs'] = MemberNomination.objects.prefetch_related(
            'category_nomination__nomination',
            'category_nomination__event_category__category',
            'photos'
        ).filter(
            member__user=user
        ).annotate(
            result_all=Sum('results__score', default=0, distinct=True),
            photo_count=Count('photos', distinct=True)
        ).order_by('photo_count', 'result_all')

        for job in data['my_jobs']:
            job.photo_1 = job.photos.first().photo if job.photos.exists() else None

        data['other_jobs'] = MemberNomination.objects.exclude(
            Q(photos=None) | Q(member__user=user)).prefetch_related(
            'category_nomination__nomination',
            'category_nomination__event_category__category',
            'photos'
        ).annotate(
            result_all=Sum('results__score', default=0, distinct=True),
            photo_count=Sum('photos', distinct=True)
        ).order_by('photo_count', 'result_all')

        for job in data['other_jobs']:
            job.photo_1 = job.photos.first().photo if job.photos.exists() else None

        return data


class RefereePageView(LoginRequiredMixin, PhotoRequiredMixin, TemplateView):
    template_name = "events/referee_page.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['jobs'] = MemberNomination.objects.exclude(Q(photos=None)).prefetch_related(
            'category_nomination__nomination',
            'category_nomination__event_category__category',
            'photos'
        ).filter(
            category_nomination__staffs__user=self.request.user,
        ).annotate(
            results_for_staff=Sum('results__score', filter=Q(results__eventstaff__user=self.request.user), default=0),
        ).order_by('results_for_staff')
        return data


class UploadPhotoView(TemplateView):
    model = MemberNomination
    template_name = 'events/upload_photo.html'
    form_class = UploadPhotoForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['job'] = MemberNomination.objects.prefetch_related('category_nomination__nomination',
                                                                                    'category_nomination__event_category__category',
                                                                                    'photos').filter(
            id=self.kwargs['pk']
        ).annotate(
            results_for_staff=Sum('results__score', filter=Q(results__eventstaff__user=self.request.user), default=0),
        ).order_by('results_for_staff').first()
        formset=formset_factory(UploadPhotoForm, extra=MemberNomination.objects.get(id=self.kwargs['pk']).category_nomination.nomination.get_photo_count())
        data['formset'] = formset
        data['photos_conf'] = MemberNomination.objects.get(id=self.kwargs['pk']).category_nomination.nomination.photos_conf
        return data

    def post(self, request, *args, **kwargs):
        photos_conf = MemberNomination.objects.get(id=self.kwargs['pk']).category_nomination.nomination.photos_conf
        for index, file in request.FILES.items():
            id_photo = index.split('_')[1]
            for photo_type, photo_list in photos_conf.items():
                for photo_data in photo_list:
                    if str(photo_data['id']) == id_photo:
                        if photo_type == 'before':
                            MemberNominationPhoto.objects.create(
                                member_nomination=MemberNomination.objects.get(id=self.kwargs['pk']),
                                photo=file,
                                before_after='BE'
                            )
                        elif photo_type == 'after':
                            MemberNominationPhoto.objects.create(
                                member_nomination=MemberNomination.objects.get(id=self.kwargs['pk']),
                                photo=file,
                                before_after='AF'
                            )
                        break  # совпадение id = выход
        return redirect(reverse_lazy('master_page'))



class RefereeAssessmentView(TemplateView):
    template_name = 'events/referee_assessment.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['attributes'] = NominationAttribute.objects.select_related().filter(
            nomination__nom__categ__id=self.kwargs['pk']
        )

        data['job'] = MemberNomination.objects.exclude(photos=None).prefetch_related('category_nomination__nomination',
                                                                                    'category_nomination__event_category__category',
                                                                                   'photos'
                                                                                   ).filter(
            id=self.kwargs['pk']
        ).annotate(
            results_for_staff=Sum('results__score', filter=Q(results__eventstaff__user=self.request.user), default=0),
        ).order_by('results_for_staff').first()
        data['all_photos'] = data['job'].photos.all()
        data['scores'] = Result.objects.filter(eventstaff__user=self.request.user,
                                               membernomination=data['job']).first()
        photo_conf = MemberNomination.objects.get(id=self.kwargs['pk']).category_nomination.nomination.photos_conf
        data['all_photos'] = data['job'].photos.all()

        name_dict = {photo['id']: photo['name'] for photo in photo_conf['before'] + photo_conf['after']}

        photos = {'BE': [], 'AF': []}
        i = 1
        for photo in data['all_photos']:
            photo_data = {
                'id': photo.id,
                'url': photo.photo.url,
                'name': name_dict.get(i),
            }
            i += 1
            photos[photo.before_after].append(photo_data)

        data['photos'] = photos

        return data

    def post(self, request, *args, **kwargs):
        data = {**request.POST}
        print(data.pop('csrfmiddlewaretoken'))
        print(data)
        score = sum([int(x[0]) for x in data.values()])
        Result.objects.create(score=score, eventstaff=request.user.eventstaff_set.first(),
                              membernomination_id=self.kwargs['pk'], score_retail=data)
        return redirect(reverse_lazy('referee_page'))


class EvaluationsView(TemplateView):
    template_name = 'events/evaluations.html'

    def get_context_data(self, **kwargs):
        job = MemberNomination.objects.get(pk=self.kwargs['pk'])
        data = super().get_context_data(**kwargs)
        data['staffs'] = [None,
                          *EventStaff.objects.filter(category_nomination__categ__in=[job]).order_by('user__last_name')]
        nomination = job.category_nomination.nomination
        attributes = NominationAttribute.objects.filter(nomination=nomination).distinct()
        results = job.results.all().order_by('eventstaff__user__last_name')
        scores = []
        for attribute in attributes:
            score_row = []
            for result in results:
                score_row.append(result.score_retail[attribute.name][0])
            scores.append({'values': score_row, 'name': attribute.name})
        data['scores'] = scores
        data['job'] = job
        data['all_photos'] = data['job'].photos.all()
        data['user_request'] = self.request.user

        photo_conf = nomination.photos_conf
        name_dict = {photo['id']: photo['name'] for photo in photo_conf['before'] + photo_conf['after']}

        photos = {'BE': [], 'AF': []}
        i = 1
        for photo in data['all_photos']:
            photo_data = {
                'id': photo.id,
                'url': photo.photo.url,
                'name': name_dict.get(i),
            }
            i += 1
            photos[photo.before_after].append(photo_data)

        data['photos'] = photos

        return data


class ResultOfAllEvents(TemplateView):
    template_name = 'events/end_result.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        win_nominations = {}
        nominations = CategoryNomination.objects.all()
        member_nominations_all = MemberNomination.objects.all().annotate(total_score=Sum('results__score')).order_by(
            '-total_score')

        for nomination in nominations:
            member_nominations = member_nominations_all.filter(category_nomination=nomination)

            if member_nominations.count() >= 4:
                top_three = member_nominations[:3]
                win_nominations[nomination] = top_three

                for member_nomination in top_three:
                    countResults = Result.objects.filter(membernomination=member_nomination).count()
                    num_scores = member_nomination.results.annotate(num_scores=Count('id')).values('num_scores').first()
                    if num_scores:
                        member_nomination.average_score = round(member_nomination.total_score / countResults, 2)
                    else:
                        member_nomination.average_score = 0

                win_nominations[nomination] = top_three

        data['win_nominations'] = win_nominations


# БЛОК 2 НОМИНЦА
        def get_members(event):
            return (
                Member.objects.filter(event=event)
                .annotate(count_nom=Count("membernom"))
                .filter(count_nom=2)
            )

        def get_members_gte_3(event):
            return (
                Member.objects.filter(event=event)
                .annotate(count_nom=Count("membernom"))
                .filter(count_nom__gte=3)
            )

        def get_sorted_members(members):
            return members.annotate(
                total_score=Sum("membernom__results__score")
            ).order_by("-total_score")

        def get_sorted_members_for_top3(members):
            members = members.prefetch_related("membernom__category_nomination__nomination", "membernom__results")
            members_with_scores = {}

            for member in members:
                top_3_nominations = member.membernom.annotate(
                    total_score=Sum("results__score")
                ).order_by("-total_score")[:3]
                total_score = sum(nomination.total_score or 0 for nomination in top_3_nominations)
                members_with_scores[member.id] = total_score

            sorted_members = sorted(
                members_with_scores.items(), key=lambda x: x[1], reverse=True
            )[:3]
            return [member_id for member_id, _ in sorted_members]

        event = Event.objects.first()
        winner_two_nominations = get_sorted_members(get_members(event)).first()
        winner_id_for_three = get_sorted_members_for_top3(get_members_gte_3(event))[0]
        winner_for_three = Member.objects.get(id=winner_id_for_three)

        data['winner_two_nominations'] = winner_two_nominations
        data['winner_for_three'] = winner_for_three




# ВЫИГРАННЫЕ КАТЕГОРИИ (ГРАН-ПРИ)
        win_categories = {}
        categories = Category.objects.all()

        for category in categories:
            member_nominations = MemberNomination.objects.filter(category_nomination__event_category__category=category)
            members = set(member_nominations.values_list('member', flat=True))
            top_three = []
            members_all = Member.objects.all()
            for member in members:
                total = sum(Result.objects.filter(
                    membernomination__member=member,
                    membernomination__category_nomination__event_category__category=category,
                ).values_list('score', flat=True))
                top_three.append({'member': members_all.get(pk=member), 'total': total})
            top_three = sorted(top_three, reverse=True, key=lambda x: x['total'])[:3]
            win_categories[category] = top_three

        data['win_categories'] = win_categories

        return data
