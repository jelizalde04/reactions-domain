import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_NOTIFICATIONS_URL = os.getenv("WEBHOOK_NOTIFICATIONS_URL")

def send_like_webhook(data: dict):
    """
    Envía un WebHook al Notifications Service.
    """
    url = WEBHOOK_NOTIFICATIONS_URL

    if not url:
        print("[WebHook] No se configuró la URL del WebHook. Abortando envío.")
        return

    try:
        response = requests.post(url, json=data, timeout=5)
        response.raise_for_status()
        print(f"[WebHook] Notificación enviada correctamente: {response.json()}")
    except requests.RequestException as e:
        print(f"[WebHook] Error enviando la notificación: {str(e)}")
