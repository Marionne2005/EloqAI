from django.contrib import admin

# Register your models here.
from .models import Goal, InterestProfile, Video, Podcast, Exercise, SpeechExercise, DailyLog

admin.site.register([Goal, InterestProfile, Video, Podcast, Exercise, SpeechExercise, DailyLog])
