from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from events.mixins import PhotoRequiredMixin
from events.models import MemberNomination, Result, NominationAttribute, EventStaff
from users.models import User


class MasterPageView(LoginRequiredMixin, PhotoRequiredMixin, TemplateView):
    template_name = "events/master_page.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['my_jobs'] = MemberNomination.objects.select_related('category_nomination__nomination',
                                                                  'category_nomination__event_category__category').filter(
            member__user=self.request.user
        ).order_by('results__score', 'photo_1').annotate(result_all=Sum('results__score', default=0))

        data['other_jobs'] = MemberNomination.objects.exclude(
            Q(photo_1=None) | Q(photo_1='') | Q(member__user=self.request.user)).select_related(
            'category_nomination__nomination',
            'category_nomination__event_category__category').order_by('results__score', 'photo_1').annotate(
            result_all=Sum('results__score', default=0))
        return data


class RefereePageView(LoginRequiredMixin, PhotoRequiredMixin, TemplateView):
    template_name = "events/referee_page.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['jobs'] = MemberNomination.objects.exclude(Q(photo_1=None) | Q(photo_1='')).select_related(
            'category_nomination__nomination',
            'category_nomination__event_category__category', ).filter(
            category_nomination__staffs__user=self.request.user,
        ).annotate(
            results_for_staff=Sum('results__score', filter=Q(results__eventstaff__user=self.request.user), default=0),
        ).order_by('results_for_staff')
        return data


class UploadPhotoView(UpdateView):
    model = MemberNomination
    template_name = 'events/upload_photo.html'
    fields = ['photo_1', 'photo_2', 'photo_3', 'photo_4']

    def get_object(self, queryset=None):
        return MemberNomination.objects.filter(pk=self.kwargs['pk']).first()

    def get_success_url(self):
        return reverse_lazy('master_page')


class RefereeAssessmentView(TemplateView):
    template_name = 'events/referee_assessment.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['attributes'] = NominationAttribute.objects.select_related().filter(
            nomination__nom__categ__id=self.kwargs['pk']
        )

        data['job'] = MemberNomination.objects.exclude(photo_1=None).select_related('category_nomination__nomination',
                                                                                    'category_nomination__event_category__category', ).filter(
            id=self.kwargs['pk']
        ).annotate(
            results_for_staff=Sum('results__score', filter=Q(results__eventstaff__user=self.request.user), default=0),
        ).order_by('results_for_staff').first()
        data['scores'] = Result.objects.filter(eventstaff__user=self.request.user,
                                               membernomination=data['job']).first()
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
                          *EventStaff.objects.filter(category_nomination__categ__in=[job]).order_by('-user__last_name')]
        nomination = job.category_nomination.nomination
        attributes = NominationAttribute.objects.filter(nomination=nomination).distinct()
        results = job.results.all().order_by('eventstaff__user__last_name')
        scores = []
        for attribute in attributes:
            score_row = []
            for result in results:
                print(result.score_retail)
                score_row.append(result.score_retail[attribute.name][0])
            scores.append({'values': score_row, 'name': attribute.name})
        data['scores'] = scores
        return data