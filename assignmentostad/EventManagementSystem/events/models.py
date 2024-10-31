from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

# Category model for event categorization
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Custom User model with additional fields
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
    )
    
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='USER')
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username


# Event model for creating and managing events
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    description = models.TextField()
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    max_capacity = models.PositiveIntegerField()
    booked_count = models.PositiveIntegerField(default=0)

    def is_fully_booked(self):
        return self.booked_count >= self.max_capacity

    def __str__(self):
        return f"{self.name} on {self.date} at {self.location}"


# Booking model for user bookings related to events
class Booking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # Prevent multiple bookings for the same event by the same user

    def __str__(self):
        return f"Booking by {self.user.username} for {self.event.name}"
