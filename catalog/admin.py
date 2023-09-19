# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Order, OrderItem, Product, Offer
from common.admin import *

class OfferInline(admin.TabularInline):
    model = Offer
    fields = ('title', 'price', 'old_price', 'article', 'quantity', 'order')
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'city',)
    list_display_links = ('id', 'title',)
    list_filter = ('city',)
    fieldsets = (
        (_('Page'), {
          'fields': node_default_fields + ('image', 'category'),
        }),
        (_('Additional Categories'), {
            'classes': ('collapse',),
            'fields': ('categories',),
        }),
        seo_fieldset,
        date_fieldset,
    )
    filter_horizontal = ('categories',)
    readonly_fields = ("created_at", "updated_at",)
    inlines = [
        OfferInline,
    ]

    def save_related(self, request, form, *args, **kwargs):
        super().save_related(request, form, *args, **kwargs)
        obj = form.instance
        if obj.category:
            obj.categories.add(obj.category)


class TreeNodeAdmin(DraggableMPTTAdmin, NodeAdmin):
    def get_node_fieldsets(self):
        return (
            tree_node_default_fieldset,
            seo_fieldset,
            date_fieldset,
        )

    list_display = ('tree_actions', 'indented_title', 'is_active', 'alias',)
    list_editable = ('is_active',)

@admin.register(Category)
class CategoryAdmin(TreeNodeAdmin):
    def get_node_fieldsets(self):
        return (
            (_('Page'), {
              'fields': tree_node_default_fields + ('image', 'banner_text'),
            }), 
            seo_fieldset,
            date_fieldset,
        )

# admin.site.register(Order)
# admin.site.register(OrderItem)