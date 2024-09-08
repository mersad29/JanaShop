from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError("لطفا یک شماره تلفن وارد کنید")

        user = self.model(
            phone=phone
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone=phone,
            password=password
        )
        user.is_admin = True
        user.save()
        return user

class CustomUser(AbstractBaseUser):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone = models.CharField(max_length=11, unique=True)
    telephone = models.CharField(max_length=11, unique=True, blank=True, null=True)
    email = models.EmailField()
    date_of_birth = models.DateTimeField(blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    national_code = models.CharField(max_length=10, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=100, blank=True, null=True, unique=True)
    image = models.ImageField(upload_to='account/images', blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.fname} - {self.lname} - {self.phone} - {self.telephone} -" \
               f"{self.email} - {self.email} - {self.date_of_birth} - {self.card_number}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Otp(models.Model):
    token = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    code = models.IntegerField()
    expiration_date = models.DateTimeField(auto_now_add=True)

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='useraddress')
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=300)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone = models.BigIntegerField(max_length=12)
    postal_code = models.BigIntegerField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.phone}-{self.postal_code}"

    class Meta:
        verbose_name = 'نشانی'
        verbose_name_plural = 'نشانی ها'
