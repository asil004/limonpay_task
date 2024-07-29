from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models

CARD_TYPES = (
    ('HUMO', 'Humo'),
    ('UZCARD', 'UzCard'),
)


class CustomUserManager(BaseUserManager):
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def _create_user(self, phone_number, password, **extra_fields):
        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=50)

    REQUIRED_FIELDS = []
    username = None

    EMAIL_FIELD = 'phone_number'
    USERNAME_FIELD = 'phone_number'

    objects = CustomUserManager()

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return f"{self.phone_number}"


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=6, choices=CARD_TYPES)
    card_number = models.CharField(max_length=16, unique=True)
    expiration_date = models.CharField(max_length=5)
    currency = models.CharField(max_length=3, default="UZS")
    value = models.DecimalField(decimal_places=4, max_digits=15, default=0)

    def __str__(self):
        return f"{self.id} - {self.card_number}"


class MerchantCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Merchant(models.Model):
    name = models.CharField(max_length=50)
    merchant_category = models.ForeignKey(MerchantCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class BaseTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    ip_address = models.GenericIPAddressField()
    device_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Transaction for {self.merchant.name} from {self.user.id} on {self.created_at}"


# Payment Transactions
class PhonePaymentTransaction(BaseTransaction):
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.phone_number}"


class CardPaymentTransaction(BaseTransaction):
    card_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.card_number}"
