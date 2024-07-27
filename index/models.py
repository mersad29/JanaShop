from django.db import models


class Faq(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    num = models.CharField(max_length=10, default='One')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'سوال متداول'
        verbose_name_plural = 'سوالات متداول'