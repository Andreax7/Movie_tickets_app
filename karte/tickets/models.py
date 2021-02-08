from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movies(models.Model):
    MovieName = models.CharField(max_length=100)
    lenght = models.CharField(max_length=20)
    genre = models.CharField(max_length=50)
    TotalSeat = models.PositiveIntegerField()
   
    def __str__(self):
        return str(self.MovieName)
      
  
class Ticket(models.Model):
    id_ticket = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    MovieName = models.ForeignKey(Movies, on_delete=models.CASCADE)
    Seat = models.PositiveIntegerField()
  
    def __str__(self):
        return str(self.id_ticket)
