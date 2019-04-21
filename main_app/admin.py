from django.contrib import admin

from .models import Good, Order, GoodPriceRating


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['good', 'name', 'phone', 'date']


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ['price', 'name', 'brand', 'images']


@admin.register(GoodPriceRating)
class GoodPriceRatingAdmin(admin.ModelAdmin):
    list_display = ['average_rating', 'reviews', 'rating_scale', 'price', 'availability',
                    'standard_price', 'date_time_field', 'date']

