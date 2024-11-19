
from typing import List
from django.conf import settings
from django.core.mail import send_mail
from ninja import Schema

class EmailNotificationSchema(Schema):
    subject: str
    message: str
    recipients: List[str]

def trigger_user_notification(request, notification: EmailNotificationSchema):
    
    subject = "This email is from HR Adminstartion"
    recipients = notification.recipients
    message = "Your account has been activated. you can login now.Thank you for registeration"

    # Here, you can call your existing _notifyUserRegistrationStatus function
    # or extract the common logic to a separate function to reuse it
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
    return {"message": "User notification triggered successfully"}
 
