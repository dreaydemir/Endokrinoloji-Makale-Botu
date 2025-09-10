# Endokrinoloji-Makale-Botu
Endokrinoloji alanındaki Q1-Q4 indeksli seçtiğiniz dergilerde yayınlanan yeni makaleleri haftalık olarak takip eden ve anahtar kelimelere göre özetleyip e-posta ile gönderen otomatik bir yapay zeka aracı.

## Özellikler
- RSS tarama (çoklu dergi)
- Anahtar kelimeye göre filtre
- OpenAI `gpt-4o-mini` ile Türkçe/İngilizce özet
- Gmail üzerinden otomatik e-posta
- Cron ile haftalık otomasyon
- Güvenli yapılandırma (`.env`)

## Kurulum
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# .env içini doldur
python src/app.py
