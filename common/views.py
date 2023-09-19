# -*- coding: utf-8 -*-

from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden, JsonResponse
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Page, Slider
from catalog.models import Product, Offer
from .forms import FeedbackForm
from config import settings

base_crumbs = (
    {'title': 'Главная', 'url': '/', 'position': 1},
)

class PageView(TemplateView):
    template_name = "core/content/page.html"

    def get_context_data(self, **kwargs):
        page_alias = self.kwargs['page_alias']
        country = self.kwargs.get('country','ufa')


        context = super().get_context_data(**kwargs)
        context['page'] = Page.objects.filter(
            alias=page_alias,
            city=country,
            is_active=True
        ).first()
        title = ""
        try:
            title = context['page'].title
        except:
            title = ""

        context['breadcrumbs'] = base_crumbs + (
            {
                'title': title,
                'url': '/page_alias/',
                'position': 2,
            },
        )

        return context

class HomePageView(TemplateView):

    template_name = "core/homepage.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        try:
            context['page'] = Page.objects.get(pk=9)
        except Exception as e:
            t = u'Страница не существует'
            context['page'] = Page(
              title=t,
              content=t,
            )

        try:
            ps = Slider.objects.get(pk=1)
            context['producer_slides'] = ps.items.all()[:6]

            ss = Slider.objects.get(pk=2)
            context['cert_slides'] = ss.items.all()[:10]

            ms = Slider.objects.get(pk=6)
            context['main_slides'] = ms.items.all()[:5]
        except Exception as e:
            pass

        context['product'] = Product.objects.get(pk=37)

        return context

class CertificatesView(TemplateView):
    template_name = "core/certificates.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['certs'] = list(
                Slider.objects.filter(id__in=[8, 9])
            )
            context['page'] = Page.objects.get(pk=settings.CERTS_PAGE_ID)
        except Page.DoesNotExist:
            pass

        context['breadcrumbs'] = (
            {'title': 'Главная', 'url': '/', 'position': 1},
            {'title': 'Сертификаты', 'url': '/certs/', 'position': 2},
        )

        return context
    
def country(request, country):
    
    if not country:
        return HttpResponseForbidden('Доступ запрещен')
    qs = Product.objects.filter(city=country)
    ctx = {
        "qs": qs,
    }
    return render(request, 'core/base.html', ctx)


class FeedbackView(View):
    order = None

    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden('Доступ запрещен')

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)

        if not form.is_valid():
            return JsonResponse({
                'success': False,
                'message': 'Ошибки в форме',
            })

        send_mail(
            'Заказ обратного звонка с сайта uekopora.ru',
            '.',
            settings.EMAIL_HOST_USER,
            settings.MANAGER_EMAILS,
            fail_silently=True,
            html_message=render(request, 'core/email/feedback.html', context=form.cleaned_data),
        )

        return JsonResponse({
            'success': True,
            'message': 'Заявка отправлена',
        })

