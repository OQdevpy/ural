# -*- coding: utf-8 -*-

from django.views.generic import View, TemplateView, RedirectView
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Prefetch
from .models import Category, Product, Offer, Order, OrderItem
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from .forms import OrderAddOfferForm, OrderUpdateOfferForm, OrderForm
from common.models import Page

base_crumbs = (
  {'title': u'Главная', 'url': '/', 'position' : 1},
  {'title': u'Каталог', 'url': '/catalog/', 'position' : 2},
)


class CatalogView(TemplateView):
    template_name = "catalog/catalog.html"

    def get_context_data(self, **kwargs):
        context = super(CatalogView, self).get_context_data(**kwargs)

        try:
            context['page'] = Page.objects.get(alias='сatalog')
        except:
            pass

        context['breadcrumbs'] = base_crumbs
        context['categories'] = Category.objects.filter(level=0, is_active=True)

        return context


class CategoryView(TemplateView):
    template_name = "catalog/category.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)

        category_alias = self.kwargs['category_alias']
        country = self.kwargs['country']

        category = get_object_or_404(
            Category,
            alias=category_alias,
            is_active=True,
        )
        context['category'] = category

        context['root_category'] = Category.objects.get(
            tree_id=category.tree_id,
            level=0,
        )

        child_tree = list(
            Category.objects.filter(
                lft__gte=category.lft,
                rght__lte=category.rght,
                tree_id=category.tree_id
            ).values('id')
        )
        categories_in = [c['id'] for c in child_tree]
        products = Product.objects.filter(
            is_active=True,
            categories__in=categories_in
        ).prefetch_related('offers')
        for p in products:
            ofrs = list(p.offers.all())
            if ofrs:
                p.first_offer = ofrs[0]
        products = products.filter(city=country)        
        context['products'] = products
        context['breadcrumbs'] = base_crumbs + (
            {
                'title': context['category'].title,
                'url': context['category'].get_absolute_url,
                'position': 3
            },
        )

        return context


class ProductRootView(RedirectView):
    permanent = False
    query_string = True
    # pattern_name = 'article-detail'


class ProductView(TemplateView):
    template_name = "catalog/product.html"

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        country = self.kwargs.get('country','ufa')

        product_alias = self.kwargs['product_alias']

        context['product'] = get_object_or_404(
            Product,
            alias=product_alias,
            is_active=True,
            city = country
        )

        category = context['product'].category

        if not category or not category.is_active:
            raise Http404(':(')

        context['category'] = category
        context['breadcrumbs'] = base_crumbs + (
            {
                'title': context['category'].title,
                'url': context['category'].get_absolute_url,
                'position': 3
            },
            {
                'title': context['product'].title,
                'url': context['product'].get_absolute_url,
                'position': 4
            }
        )

        return context


class PowerLineSupportView(TemplateView):
    template_name = "catalog/power-line-support.html"

    def get_context_data(self, **kwargs):
        context = super(PowerLineSupportView, self).get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=37)
        context['breadcrumbs'] = base_crumbs + (
            {
                'title': u'Калькулятор стоимости деревянных опор ЛЭП',
                'url': '',
                'position': 4
            },
        )
        return context


# ============================================================================


def get_order(request):
    session = request.session
    order = None

    if not 'order_id' in session:
        order = Order.objects.create()
    else:
        try:
            order = Order.objects.get(pk=session['order_id'])
        except Exception as e:
            order = Order.objects.create()

    session['order_id'] = order.id
    return order


class OrderView(TemplateView):
    template_name = "catalog/order.html"

    def _render_email_body(self, order):
        return render_to_string('catalog/email/new.html', {'order': order})

    def send_manager_email(self, order):
        send_mail(
            'Новый заказ %s на сайте uekopora.ru' % order.id,
            '.',
            settings.EMAIL_HOST_USER,
            settings.MANAGER_EMAILS,
            fail_silently=True,
            html_message=self._render_email_body(order),
        )

    def send_client_email(self, order):
        send_mail(
            'Вы оформили заказ %s на сайте uekopora.ru' % order.id,
            '.',
            settings.EMAIL_HOST_USER,
            [order.email],
            fail_silently=True,
            html_message=self._render_email_body(order),
        )

    def post(self, request, *args, **kwargs):
        session = self.request.session
        resp = {
            'status': False,
            'message': u'Ошибки в форме заказа'
        }

        order = get_order(self.request)
        form = OrderForm(self.request.POST, instance=order)

        if not form.is_valid():
            resp['data'] = form.errors

            return JsonResponse(resp)

        new_order = form.save(commit=False)
        new_order.status = 1
        new_order.save()

        self.send_client_email(new_order)
        self.send_manager_email(new_order)

        resp['message'] = u'Заказ оформлен'
        resp['status'] = True
        resp['data'] = {'redirect': '/order/success/'}

        session['order_id'] = None
        session['last_order_id'] = new_order.id
        return JsonResponse(resp)

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)

        context['order'] = get_order(self.request)

        context['order_items'] = (
            context['order']
            .items
            .prefetch_related('offer', 'offer__product')
            .all()
        )

        context['form'] = OrderForm()

        context['breadcrumbs'] = [
            {'title': u'Главная', 'url': '/', 'position' : 1},
            {'title': u'Ваш заказ', 'url': '/order/', 'position' : 2},
        ]

        return context


class OrderSuccessView(TemplateView):
    template_name = "catalog/order-success.html"

    def get_context_data(self, **kwargs):
        pk = self.request.session['last_order_id']

        context = super(OrderSuccessView, self).get_context_data(**kwargs)
        context['order'] = get_object_or_404(Order, id=pk)

        return context


class OrderActionsView(View):
    order = None

    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden(u'Доступ запрещен')

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST запросы
        1) Необходимый url : r'^order/(?P<cart_action>[\w-]+)/$'
        2) self.kwargs['cart_action'] должно присутствовать
           в списке разрешенных
        """
        cart_action = self.kwargs['cart_action']
        status = False
        message = u''
        errors = []

        self.request = request
        self.order = get_order(request)

        allowed_actions = {
            'add'     : self._add,
            'update'  : self._update,
            'remove'  : self._remove,
            'clear'   : self._clear,
            'submit'  : self._submit
        }

        try:
            status, message, errors, data = allowed_actions[cart_action]()
        except KeyError as e:
            return HttpResponseForbidden(f'Неизвестный метод: {str(cart_action)}')

        order_cost = 0
        order_quantity = 0
        for i in self.order.items.all():
            order_quantity = order_quantity + i.quantity
            order_cost = order_cost + i.quantity * i.price

        data['order_cost'] = order_cost
        data['order_quantity'] = order_quantity

        return JsonResponse({
            'status'    : status,
            'message'   : message,
            'errors'    : errors,
            'data'      : data,
            'action'    : cart_action
        })

    # def _get_count(self):


    def _add(self):
        """Добавляет товар в корзину.
        1) Если товар уже есть в корзине, вызывает метод апдейт.
        2) Форма отвечает за валидацию и отчистку параметров.
        """
        form = OrderAddOfferForm(self.request.POST)

        if form.is_valid():
            offer_id = form.cleaned_data['offer_id']
            quantity = form.cleaned_data['quantity']

            offer = Offer.objects.get(pk=offer_id)

            try:
                item = self.order.items.get(offer=offer)
                item.price = offer.price
                item.quantity = item.quantity + quantity
                item.save()
                msg = u'Количество товара в корзине обновлено'
            except Exception as e:
                item = self.order.items.create(
                    offer_id=offer_id,
                    quantity=quantity,
                    price=offer.price
                )
                msg = u'Товар добавлен в корзину'

            return True, msg, [], {'buttons' : ('checkout',)}
        else:
            return False, u'Ошибка', form.errors, {}

    def _update(self):
        """Изменяет количество товара в корзине.
        1) Форма отвечает за валидацию и отчистку параметров.
        """
        form = OrderUpdateOfferForm(self.request.POST)
        errors = []

        if form.is_valid():
            status = False
            order_offer_id = form.cleaned_data['order_offer_id']
            quantity = form.cleaned_data['quantity']

            try:
                item = self.order.items.get(pk=order_offer_id)
                item.quantity = quantity
                item.save()
                msg = u'Количество товара в корзине обновлено'
                status = True
            except Exception as e:
                msg = u'Ошибка'
        else:
            msg = u'Ошибка'
            errors = form.errors

        return status, msg, errors, {'reload': True}

    def _remove(self):
        """Удаляет товар из корзины.
        1) Форма отвечает за валидацию и отчистку параметров.
        """
        return True, u'Товар удален из корзины', []

    def _clear(self):
        """Очищает корзину"""
        return True, u'Корзина очищена', []

    def _submit(self):
        """Отправляет заказ
        1) Форма отвечает за валидацию и отчистку параметров.
        """
        return True, u'Заказ отправлен', []
