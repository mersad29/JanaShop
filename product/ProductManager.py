from django.db import models

class ProductQuerySet(models.QuerySet):
    def available_products(self):
        return self.filter(in_stock=True)

    def get_price_range(self, filter, order:str):
        # min_price = self.aggregate(models.Min('price'))['price__min']
        # max_price = self.aggregate(models.Min('price'))['price__max']

        min_price = self.filter(filter).order_by(order).first().price
        max_price = self.filter(filter).order_by(order).last().price
        return min_price, max_price

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def available_product(self):
        return self.get_queryset().available_products()

    def get_price_range(self):
        return self.get_queryset().get_price_range()