from django.contrib import admin
from .models import BookCategory, BookProduct, Card, Order, Liked

admin.site.register(BookCategory)
admin.site.register(BookProduct)
admin.site.register(Card)
admin.site.register(Liked)
admin.site.register(Order)