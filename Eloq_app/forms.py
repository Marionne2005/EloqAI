from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Goal, InterestProfile, Exercise, DiscoverY, Interest


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model= User
        fields= ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model=User
        fields=['username','password']

class GoalForm(forms.ModelForm):
    class Meta:
        model= Goal  
        fields=['goals_name']  

class InterestQuizForm(forms.ModelForm):
    class Meta:
        model = InterestProfile
        fields = ['interests']  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['interests'].widget = forms.CheckboxSelectMultiple()
        self.fields['interests'].queryset = Interest.objects.all()
class DiscoverYForm(forms.ModelForm):
    class Meta:
        model=DiscoverY
        fields=['title','description']