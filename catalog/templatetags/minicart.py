import contextlib
from django import template
from catalog.models import Category, Order
from common.models import Tree


register = template.Library()


@register.simple_tag(takes_context=True)
def minicart(context):
    order_cost = 0
    order_quantity = 0

    session = context.request.session

    if 'order_id' in session:
        with contextlib.suppress(Order.DoesNotExist):
            order = Order.objects.get(pk=session['order_id'])
            for i in order.items.all():
                order_quantity = order_quantity + i.quantity
                order_cost = order_cost + i.quantity * i.offer.price
    return {'order_cost': order_cost, 'order_quantity': order_quantity}
