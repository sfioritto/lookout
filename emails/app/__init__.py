from webapp import settings
from app.model import alerts

if settings.DEBUG:
    alerts.GOOGLE_URL = "localhost:8000"
