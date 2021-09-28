from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime

def validate_date(date):
    if date < datetime.date.today():
        raise ValidationError("Date cannot be in the past")

# Create your models here.
class Room(models.Model):
   

    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} -for {self.capacity} people  "

class Reservation(models.Model):
    date = models.DateField(validators=[validate_date])
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.TextField()

    def __str__(self):
        return f"{self.user} booked {self.room} on {self.date} with comments as  {self.comment}" 