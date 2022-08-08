from django.db import models


# Create your models here.
class Order(models.Model):
    number = models.PositiveIntegerField("№")
    order_number = models.PositiveIntegerField("заказ №", unique=True)
    cost_dollar = models.PositiveIntegerField("стоимость,$")
    delivery_date = models.DateField("Дата")
    cost_rubles = models.PositiveIntegerField("стоимость в руб.")

    def __str__(self):
        return f"Заказ: {self.order_number}"

    class Meta:
        ordering = ['number']


class TelegramID(models.Model):
    user_id = models.CharField("ID", max_length=128)

    def __str__(self):
        return self.user_id