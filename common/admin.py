from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from mptt.admin import DraggableMPTTAdmin
from .models import Page, Slider, SliderItem

node_default_fields = ('is_active', 'title', 'alias', 'introtext', 'content','city')
tree_node_default_fields = ('is_active', 'title', 'alias', 'parent', 'introtext', 'content',)
date_fields = ('created_at', 'updated_at',)
seo_fields = ('h1', 'meta_title', 'meta_description', 'meta_keywords',)

node_default_fieldset = (None, {
    'fields': node_default_fields
})
tree_node_default_fieldset = (None, {
    'fields': tree_node_default_fields
})
date_fieldset = (_('Information'), {
    'classes': ('collapse',),
    'fields': date_fields
})
seo_fieldset = (_('SEO'), {
    'classes': ('collapse',),
    'fields': seo_fields
})


class NodeAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fieldsets = self.get_node_fieldsets()

    def get_node_fieldsets(self):
        return (
            node_default_fieldset,
            seo_fieldset,
            date_fieldset,
        )

    readonly_fields = ("created_at", "updated_at",)
    list_display = ('title', 'is_active', 'alias', 'created_at', 'updated_at')
    list_editable = ('is_active',)


# class TreeNodeAdmin(DraggableMPTTAdmin, NodeAdmin):
#     def get_node_fieldsets(self):
#         return (
#             tree_node_default_fieldset,
#             seo_fieldset,
#             date_fieldset,
#         )

#     list_display = ('tree_actions', 'indented_title', 'is_active', 'alias',)
#     list_editable = ('is_active',)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    fieldsets = (
        node_default_fieldset,
        seo_fieldset,
        date_fieldset,
    )
    list_display = ('id','title', 'is_active', 'alias', 'city')
    list_display_links = ('title',)
    list_editable = ('is_active','city')
    readonly_fields = ("created_at", "updated_at",)
    list_filter = ('city','is_active')
    ordering = ('-city','title')



class SliderItemInline(admin.TabularInline):
    model = SliderItem
    extra = 3


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    inlines = [SliderItemInline,]
    list_display = ('id','title',  'city')

    list_display_links = ('title',)
    list_editable = ('city',)
    list_filter = ('city',)
    ordering = ('-city','title')
