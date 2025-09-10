import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
RECIPIENT_ADDRESS = os.getenv("RECIPIENT_ADDRESS", "")
MAIL_SUBJECT = os.getenv("MAIL_SUBJECT", "Haftalık Endokrinoloji Makale Özetleri")
SUMMARY_LANGUAGE = os.getenv("SUMMARY_LANGUAGE", "tr")  # "tr" veya "en"

# Basit doğrulama
REQUIRED = {
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "EMAIL_ADDRESS": EMAIL_ADDRESS,
    "EMAIL_PASSWORD": EMAIL_PASSWORD,
    "RECIPIENT_ADDRESS": RECIPIENT_ADDRESS,
}
missing = [k for k, v in REQUIRED.items() if not v]
if missing:
    raise RuntimeError(f".env eksiği: {', '.join(missing)}")
