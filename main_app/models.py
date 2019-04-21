from django.db import models
from django.contrib.auth.models import User


class Good(models.Model):
    product_id = models.CharField(max_length=30, verbose_name='ID')
    name = models.CharField(max_length=300, verbose_name='Name', default='na')
    price = models.FloatField(default=0, verbose_name='Price')
    brand = models.CharField(max_length=30, verbose_name='Brand', blank=True)
    images = models.ImageField(upload_to='good_images/', blank=False, default='')
    provider_name = models.CharField(max_length=30, verbose_name='NameBrand')
    type_good = models.CharField(max_length=30, verbose_name='Type', blank=True)
    currency = models.CharField(max_length=30, verbose_name='Currency', blank=True)
    overview = models.TextField(verbose_name='Overview', default='na')
    category = models.CharField(max_length=300, verbose_name='Category', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Good'
        verbose_name_plural = 'Goods'


class GoodPriceRating(models.Model):
    good = models.ManyToManyField(Good)
    average_rating = models.FloatField(default=0, verbose_name='Rating')
    reviews = models.IntegerField(verbose_name='CountReviews')
    rating_scale = models.FloatField(default=0, verbose_name='RatingScale')
    price = models.FloatField(default=0, verbose_name='Price')
    availability = models.CharField(max_length=30, verbose_name='Category')
    standard_price = models.FloatField(default=0, verbose_name='PriceWithoutActions')
    date_time_field = models.DateTimeField(auto_now_add=True, verbose_name='DateTimeOrder')
    date = models.DateField(auto_now_add=True, verbose_name='DateOrder')
    # currency = models.CharField(max_length=30, verbose_name='Currency', default=None)

    def __str__(self):
        return self.good

    class Meta:
        ordering = ["-date"]


class Order(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='order', default=None)
    good = models.ForeignKey(Good, verbose_name='GoodOrder', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name='Name')
    phone = models.CharField(max_length=30, verbose_name='PhoneNumber')
    date = models.DateTimeField(auto_now_add=True, verbose_name='DateOrder')
    email = models.CharField(max_length=30, verbose_name='EmailOrder', default='')
    text = models.CharField(max_length=200, verbose_name='TextOrder', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


