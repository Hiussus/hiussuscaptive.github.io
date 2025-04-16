# Captive Portal mit SMS-Verifizierung

Dieses Projekt ist ein Captive Portal zur mobilen Benutzerverifizierung via SMS (E-Mail to SMS Gateway).

## 🔐 Features
- Eingabe von Mobilnummer
- Versand eines OTP-Codes via Mail-to-SMS
- Verifizierungscode-Seite
- Sichere Speicherung mit `.env`

## 🚀 Installation

```bash
git clone <repo-url>
cd captive-portal-production
pip install -r requirements.txt
cp .env.example .env  # und Werte eintragen
python app.py
```

## ⚙️ .env Konfiguration

```env
SECRET_KEY=flask_secret_key
EMAIL_ADDRESS=absender@mail.de
EMAIL_PASSWORD=passwort
SMTP_SERVER=smtp.server.de
SMTP_PORT=587
SMS_GATEWAY_DOMAIN=vodafone-sms.de
```

## 🧪 Testen

Starte das Projekt und rufe `http://localhost:5000` im Browser auf.