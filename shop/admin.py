from django.contrib import admin

# Register your models here.
from .models import Product, Contact,Login, Orders, OrderUpdate, Signin,Payments


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','category','subcategory')

admin.site.register(Product,ProductAdmin)
admin.site.register(Contact)
admin.site.register(Orders)
# admin.site.register(OrderUpdate)
# admin.site.register(Signin)
admin.site.register(Payments)

