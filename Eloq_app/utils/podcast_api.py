import requests
from django.conf import settings

def fetch_podcasts(keyword):
    url = 'https://listen-api.listennotes.com/api/v2/search'
    headers = {
        'X-ListenAPI-Key': settings.LISTEN_NOTES_API_KEY or 'DEMO_KEY'
    }
    params = {
        'q': keyword,
        'type': 'podcast',
        'language': 'English',
        'region': 'us'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        print("🛰 Status code:", response.status_code)
        print("📡 Contenu brut:", response.text)

        if response.status_code == 200:
            return response.json().get('results', [])
    except Exception as e:
        print("Erreur API:", e)
    return []
