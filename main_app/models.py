from django.db import models
from datetime import datetime, date, time


class Good(models.Model):
    product_id = models.CharField(max_length=30, verbose_name='ID_Good')
    name = models.CharField(max_length=300, verbose_name='Name', default='na')
    price = models.FloatField(default=0, verbose_name='Price')
    brand = models.CharField(max_length=30, verbose_name='Brand', blank=True)
    images = models.ImageField(upload_to='good_images/', blank=False, default='')
    provider_name = models.CharField(max_length=30, verbose_name='Name Company')
    currency = models.CharField(max_length=30, verbose_name='Currency', blank=True)
    overview = models.TextField(verbose_name='Overview', default='na')
    category = models.CharField(max_length=30, verbose_name='Category', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Good'
        verbose_name_plural = 'Goods'


class GoodCategoryGroup(models.Model):
    good = models.OneToOneField(Good, on_delete=models.CASCADE, related_name='CommentUser')
    group_category = models.CharField(max_length=300, verbose_name='Group Category', default='')
    good_subcategory = models.CharField(max_length=300, verbose_name='Group Subcategory', default='')
    type_group = models.CharField(max_length=300, verbose_name='TypeGroup', default='na')

    class Meta:
        verbose_name = 'GroupGood'
        verbose_name_plural = 'GroupGoods'

    def __str__(self):
        return self.good_subcategory


class GoodPriceRating(models.Model):
    product_id = models.CharField(max_length=30, verbose_name='ID_Good', default='na')
    # good = models.ForeignKey(Good, verbose_name='Price', on_delete=models.CASCADE, default=0)
    average_rating = models.FloatField(default=0, verbose_name='Rating')
    reviews = models.IntegerField(verbose_name='Count Reviews')
    rating_scale = models.FloatField(default=0, verbose_name='Rating Scale')
    price = models.FloatField(default=0, verbose_name='Price')
    availability = models.CharField(max_length=30, verbose_name='Availability')
    standard_price = models.FloatField(default=0, verbose_name='Price Without Actions')
    date = models.DateField(verbose_name='UpdateValue', default='2001-10-25')

    class Meta:
        verbose_name = 'PriceRating'
        verbose_name_plural = 'PriceRatings'
        ordering = ["-date"]

    def __str__(self):
        return self.product_id


class Order(models.Model):

    good = models.ForeignKey(Good, verbose_name='Good', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name='Name Person')
    phone = models.IntegerField(verbose_name='Phone Number')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date Order')
    email = models.EmailField(max_length=70,blank=True, verbose_name='Email')
    text = models.CharField(max_length=200, verbose_name='Text Order', default='')
    status = models.CharField(max_length=30, verbose_name='Status', default=False)

    def __str__(self):
        return self.good

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'



