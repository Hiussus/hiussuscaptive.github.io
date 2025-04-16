from flask import Flask, request, render_template, redirect, session, flash
import random
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMS_GATEWAY_DOMAIN = os.getenv("SMS_GATEWAY_DOMAIN")

def send_sms(phone_number, otp):
    to = f"{phone_number}@{SMS_GATEWAY_DOMAIN}"
    msg = EmailMessage()
    msg.set_content(f"Ihr Login-Code: {otp}")
    msg["Subject"] = "Ihr WLAN-Zugangscode"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        number = request.form["number"]
        if not number.isdigit() or len(number) < 8:
            flash("Ungültige Nummer.")
            return redirect("/")

        otp = str(random.randint(100000, 999999))
        session["otp"] = otp
        session["number"] = number
        try:
            send_sms(number, otp)
            return redirect("/verify")
        except Exception as e:
            flash("Fehler beim Senden der Nachricht.")
            return redirect("/")

    return render_template("index.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        user_otp = request.form["otp"]
        if user_otp == session.get("otp"):
            return "Verifiziert! Zugang gewährt."
        else:
            flash("Falscher Code.")
            return redirect("/verify")

    return render_template("verify.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)