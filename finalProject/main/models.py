from django.db import models
from auth_.models import User


class BookCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('category_name')


class BookCategory(models.Model):
    category_name = models.CharField(max_length=50)
    objects = BookCategoryManager()

    class Meta:
        verbose_name = 'Категория книг'
        verbose_name_plural = 'Категории книг'

    def __str__(self):
        return self.category_name

class BookManager(models.Manager):
    def get_by_category_without_relation(self, category_name):
        return self.filter(category=category_name)


class BookProduct(models.Model):
    product_name = models.CharField(max_length=150)
    description = models.CharField(max_length=200, blank=True)
    price = models.FloatField()
    category = models.ForeignKey(BookCategory, on_delete=models.RESTRICT, related_name='books')


    objects = models.Manager()

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ('product_name','price')


class Card(models.Model):
    number = models.CharField(max_length=20,blank=True)
    code = models.CharField(max_length=10, blank=True)
    customer = models.OneToOneField(User, on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Карты'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return self.number


class Liked(models.Model):
    cart_product = models.ManyToManyField(BookProduct)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Понравился'
        verbose_name_plural = 'Понравились'


class Order(models.Model):
    price = models.FloatField();
    address = models.CharField(max_length=150)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_product = models.ManyToManyField(Liked)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'