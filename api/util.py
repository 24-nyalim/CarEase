import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

async def sendMail(email, subject, html_content):
    try:
        api_key = os.getenv("STMP2GO_API_KEY")
        if not api_key:
            raise ValueError("STMP2GO_API_KEY not found in environment variables")
        
        payload = {
            "sender": "carease@streamgrid.site",
            "to": [email],
            "subject": subject,
            "html_body": html_content,
            "text_body": "This email requires HTML to view properly."  # Optional fallback
        }

        headers = {
            "Content-Type": "application/json",
            "X-Smtp2go-Api-Key": api_key,
            "accept": "application/json"
        }

        response = requests.post(
            "https://api.smtp2go.com/v3/email/send",
            headers=headers,
            data=json.dumps(payload)
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

    except Exception as e:
        print("Error:", e)


async def createMail(email, name, subject, email_hash, legible_date, service_name):
    """
    Send a crafted appointment confirmation email using SendGrid API.

    :param email: Recipient's email address
    :param subject: Subject of the email
    :param email_hash: Unique hash for the appointment
    """
    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #2c3e50;">Hello, {name}</h2>
        <p><strong>Appointment Date:</strong> {legible_date}</p>
        <p>Your appointment for <strong>{service_name}</strong> has been successfully added!</p>
        <p>You can track the progress of your service by visiting:</p>
        <p><a href="https://carease-production.up.railway.app/progress" style="color: #3498db;">CarEase.com/progress</a></p>
        <p>Then, simply paste this code:</p>
        <p style="font-size: 18px; font-weight: bold; color: #27ae60;">{email_hash}</p>
        <p>Have a great day and drive safe!</p>
        <img src="https://dxm.content-center.totalenergies.com/api/wedia/dam/transform/xysh7dg731tahpw133wmjuk8by/roadside-vehicle-repair-service-workers-change-mount-tires-garage-car-341509-3419-jpeg.webp?option=default" 
             alt="Car Service" style="width:100%; max-width:600px; margin-top:20px; border-radius:8px;" />
        <p style="color: #95a5a6; font-size: 12px;">CarEase Team</p>
    </div>
    """
    await sendMail(email, subject, html_content)
