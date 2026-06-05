from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='hotel')
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    verification_photo = models.ImageField(
        upload_to='hotel_verifications/', blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('drinks', 'Drinks'),
        ('desserts', 'Desserts'),
        ('local', 'Local Specials'),
    ]
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='lunch')
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.hotel.name}"
