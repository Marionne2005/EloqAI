from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from Eloq_app.forms import UserRegistrationForm, GoalForm, InterestQuizForm,DiscoverYForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from Eloq_app.utils.podcast_api import fetch_podcasts
from Eloq_app.utils.youtube_api import daily_texts
from datetime import date
from django.contrib.auth import logout
from datetime import datetime, timedelta
from .models import Goal, InterestProfile, Video, Exercise, SpeechExercise, DiscoverY,Interest,DailyLog
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from Eloq_app.utils.utils import compute_streak



def register_view(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            try:
                send_mail(
                    subject='🎉 Bienvenue chez EloqAI !',
                    message=(
                        f"Bonjour {register_form.cleaned_data['username']},\n\n"
                        "Merci de vous être inscrit(e) sur EloqAI. 🚀\n\n"
                        "Votre parcours d'élocution personnalisé commence dès aujourd’hui !\n"
                        "👉 Connectez-vous pour accéder à vos exercices, recommandations et suivre votre progrès.\n\n"
                        "Si vous avez des questions, n'hésitez pas à nous contacter.\n\n"
                        "À très bientôt,\n"
                        "-- L’équipe EloqAI"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[register_form.cleaned_data['email']],
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            except Exception as e:
                return HttpResponse(f'Erreur lors de l\'envoi de l\'email : {str(e)}')

            return render(request, 'index.html', {
                'register_form': UserRegistrationForm(),  # Clear form
                'login_form': AuthenticationForm(),
                'show_signin': True  # Show sign-in after sign-up
            })
        else:
            return render(request, 'index.html', {
                'register_form': register_form,
                'login_form': AuthenticationForm(),
                'show_signin': False
            })
    else:
        return render(request, 'index.html', {
            'register_form': UserRegistrationForm(),
            'login_form': AuthenticationForm(),
            'show_signin': False
        })

def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')  # vers ton dashboard par exemple
        else:
            return render(request, 'index.html', {
                'register_form': UserRegistrationForm(),
                'login_form': login_form,
                'show_signin': True,
                'error': 'Invalid username or password'
            })
    else:
        return render(request, 'index.html', {
            'register_form': UserRegistrationForm(),
            'login_form': AuthenticationForm(),
            'show_signin': True
        })


@login_required
def dashboard_view(request):
    total = DailyLog.objects.filter(user=request.user, exercise_done=True).count()
    streak = compute_streak(request.user)  # à définir
    return render(request, 'home.html',{
        'username': request.user.username,
        'total_exercises': total,
        'current_streak': streak,
    })


@login_required
def set_goals_view(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user  # ⬅️ assigner l'utilisateur actuel
            goal.save()
            return redirect('goal')  # ou une page de confirmation
    else:
        form = GoalForm()
    all_goals = Goal.objects.filter(user=request.user)    
    return render(request, 'set_goals.html', {'form': form, 'goals': all_goals})

@login_required
def delete_goal_view(request, goal_id):
    goal = Goal.objects.get(id=goal_id, user=request.user)
    goal.delete()
    return redirect('goal')

@login_required
def interests_quiz_view(request):
    profile, created = InterestProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = InterestQuizForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)  # crée l’objet mais ne sauve pas les ManyToMany
            profile.user = request.user
            profile.save()
            form.save_m2m()  # maintenant on peut enregistrer les ManyToMany
            return redirect('podcast_recommendation')
        else:
            print("❌ Form errors:", form.errors)
    else:
        form = InterestQuizForm(instance=profile)

    return render(request, 'quiz_interests.html', {'form': form})




@login_required
def recommendations_view(request):
    user = request.user

    try:
        interest_profile = InterestProfile.objects.get(user=user)
    except InterestProfile.DoesNotExist:
        return redirect('interests_quiz')

    goals = interest_profile.interests.all()

    # Mot-clé pour API podcasts (tu peux faire plus dynamique selon goals)
    keyword = "Public Speaking"

    # Appel API pour podcasts
    podcasts = fetch_podcasts(keyword)  # Retourne liste de dicts

    # Récupérer vidéos liées aux goals dans la base de données
    videos = Video.objects.filter(related_goals__in=goals).distinct()

    print("🔍 Podcasts trouvés:", len(podcasts))

    return render(request, 'recomand.html', {
        'podcasts': podcasts,
        'videos': videos,
        'keyword': keyword
    })

@login_required
def daily_exercise_view(request):
    exercises=SpeechExercise.objects.all().order_by('level')
    return render(request, 'exercise.html', {'exercises': exercises})

@login_required
def exercise_detail_view(request, exercise_id):
    exercise=SpeechExercise.objects.get(pk=exercise_id)
    return render(request, 'exercise_detail.html', {'exercise':exercise})


""" @login_required

def exercise_tracker_view(request):
    today = date.today()
    past_week = [today - timedelta(days=i) for i in range(6, -1, -1)]
    completed_days = DailyLog.objects.filter(user=request.user, exercise_done=True).values_list('date', flat=True)
    return render(request, 'tracker.html', {'dates': past_week, 'completed_days': completed_days}) """

@login_required
def Discovery(request):
    return render(request,"discovery.html")

@login_required
def discovery_view(request):
    if request.method == 'POST':
        form = DiscoverYForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            form = DiscoverYForm()  # reset form after save
    else:
        form = DiscoverYForm()

    # Récupérer toutes les découvertes de l'utilisateur connecté
    discoveries = request.user.discovery_set.all()

    return render(request, "discovery.html", {
        "form": form,
        "discoveries": discoveries
    })



def logout_view(request):
    logout(request)
    return redirect('login')

