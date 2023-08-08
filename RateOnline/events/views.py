from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from events.mixins import PhotoRequiredMixin
from events.models import MemberNomination, Result, NominationAttribute
from users.models import User


class MasterPageView(LoginRequiredMixin, PhotoRequiredMixin, TemplateView):
    template_name = "events/master_page.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['jobs'] = MemberNomination.objects.select_related('category_nomination__nomination',
                                                               'category_nomination__event_category__category').filter(
            member__user=self.request.user
        )
        return data


class RefereePageView(LoginRequiredMixin, PhotoRequiredMixin, TemplateView):
    template_name = "events/referee_page.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['jobs'] = MemberNomination.objects.exclude(Q(photo_1=None) | Q(photo_1='')).select_related(
            'category_nomination__nomination',
            'category_nomination__event_category__category', ).filter(
            category_nomination__staffs__user=self.request.user,
        )
        return data


class UploadPhotoView(UpdateView):
    model = MemberNomination
    template_name = 'events/upload_photo.html'
    fields = ['photo_1', 'photo_2', 'photo_3', 'photo_4']

    def post(self, request, *args, **kwargs):
        # data = {**request.POST}
        # todo: Жалуется на фильтр при отправке. Не показывает фотографию, которую выбрал.
        MemberNomination.objects.update(photo_1='photo_1', photo_2='photo_2',
                                        photo_3='photo_3', photo_4='photo_4').filter(
            id=self.kwargs['pk']
        ).first()
        return super().get(request, *args, **kwargs)

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
        ).first()
        return data

    def post(self, request, *args, **kwargs):
        data = {**request.POST}
        print(data.pop('csrfmiddlewaretoken'))
        print(data)
        score = sum([int(x[0]) for x in data.values()])
        Result.objects.create(score=score, eventstaff=request.user.eventstaff_set.first(),
                              membernomination_id=self.kwargs['pk'], score_retail=data)
        return super().get(request, *args, **kwargs)


class EvaluationsView(TemplateView):
    template_name = 'events/evaluations.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['job'] = MemberNomination.objects.exclude(Q(photo_1=None) | Q(photo_1='')).select_related(
            'category_nomination__nomination',  # todo: брать всех судей из БД, которые оценили эту работу
            'category_nomination__event_category__category', ).filter(
            member__user=self.request.user,
        )
        data['attributes'] = NominationAttribute.objects.select_related().filter(
            nomination__nom__categ__id=self.kwargs['pk']
        )
