from django import template
from catalog.models import Category, Order
from common.models import Tree


register = template.Library()

@register.simple_tag(takes_context=True)
def sidebar(context):
    tree = Tree(Category)
    context['categories'] = tree.get_tree(None)
    return context
