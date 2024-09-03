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

class About(models.Model):
    introduction = models.TextField()

class Personnel(models.Model):
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='personnels')
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='index/images')
    github = models.CharField(max_length=400, blank=True, null=True)
    linkedin = models.CharField(max_length=400, blank=True, null=True)
    instagram = models.CharField(max_length=400, blank=True, null=True)

class Footer(models.Model):
    instagram = models.CharField(max_length=400, blank=True, null=True)
    facebook = models.CharField(max_length=400, blank=True, null=True)
    x = models.CharField(max_length=400, blank=True, null=True)
    youtube = models.CharField(max_length=400, blank=True, null=True)
    linkedin = models.CharField(max_length=400, blank=True, null=True)

    def __str__(self):
        return f"{self.instagram}"