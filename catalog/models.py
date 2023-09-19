from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import TreeNode, SeoNode, PageNode
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill
from mptt.models import TreeForeignKey, TreeManyToManyField
from multiselectfield import MultiSelectField

CITIES = (
    ("ekaterinburg", "Екатеринбург"),
    ('ufa', 'Уфа'),
    ('sant-peterburg', 'Санкт-Петербург'),
    ('tyumen', 'Тюмень'),
    ('magadan', 'Магадан'),
    ('kursk', 'Курская область'),
    ('mahachkala', 'Махачкала'),


)

class City(models.Model):
    name = models.CharField(max_length=100, choices=CITIES, default='ufa',verbose_name=_("City"))

    def __str__(self) -> str:
        return self.name


class Category(TreeNode, SeoNode):
    image = models.ImageField(upload_to='categories',
                              null=True, verbose_name=_("Image"), blank=True)

    banner_text = models.TextField(verbose_name=_(
        "Banner Text"), blank=True, null=True)

    def get_absolute_url(self):
        return "/catalog/%s/" % self.alias

    class Meta:
        verbose_name = u"категория"
        verbose_name_plural = u"категории"
        ordering = ('lft', 'title',)
        app_label = 'catalog'


    def __str__(self):
        return self.title

class Product(PageNode, SeoNode):
    category = TreeForeignKey(verbose_name=_("Main Category"),
                              to=Category, blank=True, null=True,
                              on_delete=models.CASCADE,
                              related_name='native_products')

    categories = TreeManyToManyField(verbose_name=_("Additional Categories"),
                                     to=Category, related_name="products",
                                     blank=True,null=True)

    image = models.ImageField(upload_to='product_images')
    
    city = models.ManyToManyField(City, verbose_name=_("City"), blank=True, null=True)

    def get_absolute_url(self):
        return "/product/%s/" % self.alias

    class Meta:
        verbose_name = u"товар"
        verbose_name_plural = u"товары"
        ordering = ('title',)
        app_label = 'catalog'

class Offer(models.Model):
    title = models.CharField(verbose_name=_(
        "Title"), max_length=255, null=False, db_index=True, default='', blank=True)
    article = models.CharField(verbose_name=_(
        "Article"), max_length=255, blank=True, null=False, db_index=True, default='')
    product = models.ForeignKey(
        to=Product, blank=False, null=False, on_delete=models.CASCADE, related_name='offers')
    city = models.CharField(choices=CITIES, default='ufa',verbose_name=_("City"),max_length=100)
    price = models.FloatField(db_index=True, default=0,
                              blank=True, verbose_name=_("Price"))
    old_price = models.FloatField(
        db_index=True, default=0, blank=True, verbose_name=_("Old Price"))
    quantity = models.IntegerField(
        db_index=True, default=0, blank=True, verbose_name=_("Quantity"))
    order = models.IntegerField(
        db_index=True, default=500, verbose_name=_("Order"))

    class Meta:
        verbose_name = u"торговое предложение"
        verbose_name_plural = u"торговые предложения"
        ordering = ('order', 'title')
        app_label = 'catalog'


    def __str__(self):
        return self.title



class Order(models.Model):
    STATUS_CHOICES = (
        (0, _('Cart')),
        (1, _('Placed')),
        (2, _('Processed')),
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    receiver = models.CharField(verbose_name=_(
        "Receiver"), max_length=255, null=False, db_index=True, default='', blank=False)
    email = models.CharField(verbose_name=_(
        "Email"), max_length=50, null=False, db_index=True, default='', blank=False)
    phone = models.CharField(verbose_name=_(
        "Phone"), max_length=30, null=False, blank=False, db_index=True, default='')
    comment = models.TextField(verbose_name=_(
        "Comment"), null=True, blank=True)

    class Meta:
        app_label = 'catalog'
        verbose_name = u"заказ"
        verbose_name_plural = u"заказы"




                    
                  





class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, blank=True, null=True,
                              on_delete=models.CASCADE, related_name='items', db_index=True)
    offer = models.ForeignKey(to=Offer, blank=True, null=True,
                              on_delete=models.CASCADE, related_name='order_items', db_index=True)
    price = models.FloatField(db_index=True, default=0,
                              blank=True, verbose_name=_("Price"))
    quantity = models.IntegerField(
        db_index=True, default=0, blank=True, verbose_name=_("Quantity"))

    def _get_cost(self):
        return self.price * self.quantity

    cost = property(_get_cost)

    class Meta:
        app_label = 'catalog'
        verbose_name = u"позиция заказа"
        verbose_name_plural = u"позиции заказов"




