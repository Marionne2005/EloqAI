from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Goal(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  goals_name=models.TextField()
  
  def __str__(self):
     return self.goals_name
  
class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class InterestProfile(models.Model):
   user=models.OneToOneField(User, on_delete=models.CASCADE)
   interests=models.ManyToManyField(Interest, related_name='interest_profiles')

   def __str__(self):
      return f"Interest profile of {self.user.username}"

class Video(models.Model):
   title=models.CharField(max_length=255)
   url=models.URLField()
   related_goals=models.ManyToManyField(Interest, related_name='videos')

   def __str__(self):
      return self.title 
   
class Podcast(models.Model):
   naming=models.CharField(max_length=255)
   url=models.URLField()
   related_goals=models.ManyToManyField(Interest, related_name='podcasts')

   def __str__(self):
      return self.naming
   
class Exercise(models.Model):
   title=models.CharField(max_length=255)
   content=models.TextField()

   def __str__(self):
      return self.title
   
class SpeechExercise(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    text = models.TextField()
    source_url = models.URLField(blank=True, null=True)  # Lien vers l'original si tu veux

    def __str__(self):
        return self.title   
   
class DailyLog(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    exercise_done=models.BooleanField(default=False)
    notes=models.TextField(blank=True, null=True)

    def __str__(self):
       return f"{self.user.username} - {self.date} - {'✅' if self.exercise_done else '❌'}"

class DiscoverY(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.title      