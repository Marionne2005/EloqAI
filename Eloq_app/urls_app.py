from django.urls import path
from .views import (
    register_view, login_view, dashboard_view,
    set_goals_view, delete_goal_view, interests_quiz_view,
    recommendations_view, daily_exercise_view,
    exercise_detail_view, logout_view,discovery_view,Discovery
)

urlpatterns = [
    path("register/", register_view, name='register'),
    path("login/", login_view, name='login'),
    path("logout/", logout_view, name='logout'),
    path("home/", dashboard_view, name='home'),
    path("goals/", set_goals_view, name='goal'),
    path("goals/delete/<int:goal_id>/", delete_goal_view, name='delete_goal'),
    path("quiz/", interests_quiz_view, name='interests_quiz'),
    path("recommendations/", recommendations_view, name='podcast_recommendation'),
    path("exercises/", daily_exercise_view, name='daily_exercise'),
    path("exercises/<int:exercise_id>/", exercise_detail_view, name='exercise_detail'),
    #path("tracker/", exercise_tracker_view, name='exercise_tracker'),
    path("discovery/",discovery_view,name='discovery'),
    path("discovery_details/",Discovery,name='discovery_details')
]
