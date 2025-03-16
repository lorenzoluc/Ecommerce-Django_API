from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from polymorphic.models import PolymorphicModel

# Create your models here.

### ------------ Type of Products ------------
#PolymorphicModel for make it easy to use subclass
class Products(PolymorphicModel):
    name = models.CharField(max_length = 255)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    views = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', default='default_product.jpg')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name +(f"#{self.id}")


class Books(Products):
    pages = models.PositiveIntegerField()
    author = models.CharField(max_length = 255)

class Phones(Products):
    brand = models.CharField(max_length = 255)

### ------------ New user ------------
class CustomUser(AbstractUser):
    is_seller = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True
    )


### ------------ Purchase ------------
class Purchase(PolymorphicModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchased_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} bought {self.product.name}"
