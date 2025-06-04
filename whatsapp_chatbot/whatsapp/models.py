from django.db import models

class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    state = models.CharField(max_length=50, default='initial') 
    temp_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.phone_number

class Message(models.Model):
    STATUS_CHOICES = (
        ('sent', 'Sent'),           
        ('delivered', 'Delivered'), 
        ('read', 'Read'), 
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    is_sent = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.text} ({self.status})"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.date}: {self.details}"