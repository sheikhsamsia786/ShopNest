from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (User, SellerDetail, Category, Products, 
                     Cart, Order, OrderDetails, ProductReview)

class UserAdmin(BaseUserAdmin):
    list_display    = ('id', 'username', 'email', 'is_seller', 'is_active')
    list_filter     = ('is_seller', 'is_active')
    search_fields   = ('username', 'email')
    ordering        = ('id',)
    filter_horizontal = ()
    fieldsets       = ()
    add_fieldsets   = ()

class ProductsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'productName', 'brand', 'price', 'quantity')
    search_fields = ('productName', 'brand')

admin.site.register(User, UserAdmin)
admin.site.register(SellerDetail)
admin.site.register(Category)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(ProductReview)