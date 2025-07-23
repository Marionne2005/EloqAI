from datetime import timedelta, date
from Eloq_app.models import DailyLog

def compute_streak(user):
    today = date.today()
    streak = 0

    for i in range(0, 100):  # Vérifie les 100 derniers jours max
        check_day = today - timedelta(days=i)
        if DailyLog.objects.filter(user=user, date=check_day, exercise_done=True).exists():
            streak += 1
        else:
            break  # dès qu'un jour est manqué, on arrête
    return streak
