# utils/mailersend_utils.py
import requests
import json

from decouple import config
from django.template.loader import render_to_string

MAILERSEND_API_KEY = config('MAILERSEND_API_KEY')
MAILERSEND_FROM_EMAIL = "noreply@daffodilrobotics.com"
MAILERSEND_FROM_NAME = "Daffodil Robotics"

def send_mailersend_email(to_list, subject, body_or_template, context=None, is_template=False):
    recipients = [{"email": email, "name": ""} for email in to_list]

    if is_template:
        if context is None:
            context = {}
        html_content = render_to_string(body_or_template, context)
        text_content = context.get("text_fallback", "This is an HTML email.")
    else:
        text_content = body_or_template
        html_content = None

    payload = {
        "from": {"email": MAILERSEND_FROM_EMAIL, "name": MAILERSEND_FROM_NAME},
        "to": recipients,
        "subject": subject,
        "text": text_content,
    }

    if html_content:
        payload["html"] = html_content

    headers = {
        "Authorization": f"Bearer {MAILERSEND_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://api.mailersend.com/v1/email", headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        # Try to parse JSON safely
        try:
            resp_json = response.json()
        except ValueError:
            resp_json = {"message": "No JSON response (likely success)"}

        return {"status": "success", "response": resp_json}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "error": str(e)}
