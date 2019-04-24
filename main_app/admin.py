from django.contrib import admin

from .models import Good, Order, GoodPriceRating, GoodCategoryGroup


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['good', 'name', 'phone', 'date']


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'name', 'price', 'brand']
    list_filter = ['brand', 'product_id']


@admin.register(GoodPriceRating)
class GoodPriceRatingAdmin(admin.ModelAdmin):
    list_display = ['id',  'average_rating', 'reviews', 'rating_scale', 'price', 'availability',
                    'standard_price', 'date']
    list_filter = ['product_id', 'date', 'availability', 'reviews', 'price']


@admin.register(GoodCategoryGroup)
class GoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['group_category', 'good_subcategory', 'type_group', 'good']

