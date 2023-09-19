# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext_lazy as _
from common.tools import make_url
from mptt.models import MPTTModel, TreeForeignKey
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField

CITIES = (
    ("ekaterinburg", "Екатеринбург"),
    ('ufa', 'Уфа'),
    ('sant-peterburg', 'Санкт-Петербург'),
    ('tyumen', 'Тюмень'),
    ('magadan', 'Магадан'),
    ('kursk', 'Курская область'),
    ('mahachkala', 'Махачкала'),


)

class PageNode(models.Model):
    """Base class for web pages"""

    is_active = models.BooleanField(
        verbose_name=_('Active'),
        default=True,
        db_index=True
    )
    alias = models.CharField(
        verbose_name=_('Alias'),
        max_length=255,
        null=False,
        blank=True,
        default="",
        help_text=_('Page URL. For example: about-us.'),
        db_index=True
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        null=False,
        db_index=True
    )
    introtext = models.TextField(
        verbose_name=_('Introductory Text'),
        null=True,
        blank=True
    )
    content = RichTextUploadingField(
        verbose_name=_('Content'),
        null=True,
        blank=True
    )
    created_at = models.DateField(
        verbose_name=_('Creation Date'),
        auto_now_add=True
    )
    updated_at = models.DateField(
        verbose_name=_('Update Date'),
        auto_now=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.alias:
            self.alias = make_url(self.title)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        verbose_name = u"страница"
        verbose_name_plural = u"страницы"


class SeoNode(models.Model):
    """Class for web pages with SEO fields"""
    

    h1 = models.CharField(
        verbose_name=_('H1'),
        max_length=255,
        null=True,
        blank=True
    )
    meta_title = models.CharField(
        verbose_name=_('Browser Window Title'),
        max_length=255,
        null=True,
        blank=True
    )
    meta_description = models.TextField(
        verbose_name=_('Meta Description'),
        null=True,
        blank=True
    )
    meta_keywords = models.TextField(
        verbose_name=_('Meta Keywords'),
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class TreeNode(MPTTModel, PageNode):
    """Class for tree-structured pages"""

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.SET_NULL,
        db_index=True
    )

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        abstract = True


class NotATreeNode(Exception):
    """Exception for the Tree class"""
    pass


class Tree:
    """Tree class"""
    def __init__(self, model):
        super().__init__()

        self.model = model
        if not issubclass(self.model, TreeNode):
            raise NotATreeNode(str(self.model) + ' is not a TreeNode')

        try:
            self.qs = self.model.objects.all().filter(is_active=True).order_by('lft')
        except Exception as e:
            raise e

    def __build_tree(self, parent_id, nodes):
        tree = [n for n in nodes if n.parent_id == parent_id]

        for n in tree:
            n.child_nodes = self.__build_tree(n.id, nodes)

        return tree

    def get_tree(self, parent_id):
        return self.__build_tree(parent_id, self.qs)


class Page(PageNode, SeoNode):
    city = models.CharField(choices=CITIES, default='ufa',verbose_name=_("City"),max_length=100)

    class Meta:
        verbose_name = u"страница"
        verbose_name_plural = u"страницы"
        app_label = "common"


class News(PageNode, SeoNode):
    city = models.CharField(choices=CITIES, default='ufa',verbose_name=_("City"),max_length=100)

    class Meta:
        verbose_name = u"новость"
        verbose_name_plural = u"новости"
        app_label = "common"


class Slider(models.Model):
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        null=False,
        db_index=True
    )
    description = RichTextUploadingField(
        verbose_name=_('Description'),
        null=True,
        blank=True
    )
    city = models.CharField(choices=CITIES, default='ufa',verbose_name=_("City"),max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"слайдер"
        verbose_name_plural = u"слайдеры"

        app_label = "common"


class SliderItem(models.Model):
    slider = models.ForeignKey(
        to=Slider,
        related_name='items',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        null=True,
        blank=True,
        db_index=True
    )
    image = models.ImageField(
        upload_to='slider',
        null=True,
        blank=True
    )

    thumb120 = ImageSpecField(
        source='image',
        processors=[ResizeToFit(120, 120, False, True)],
        format='JPEG',
        options={'quality': 70}
    )
    thumbcert = ImageSpecField(
        source='image',
        processors=[ResizeToFit(210, 297, False, True)],
        format='JPEG',
        options={'quality': 70}
    )
    cert = ImageSpecField(
        source='image',
        processors=[ResizeToFit(210*4, 297*4, False, True)],
        format='JPEG',
        options={'quality': 90}
    )
    homeslide = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1920, 450, False, True)],
        format='JPEG',
        options={'quality': 75}
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"Слайд"
        verbose_name_plural = u"Слайды"
        app_label = "common"
