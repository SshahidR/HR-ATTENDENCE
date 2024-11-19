
# from django.contrib.auth.models import User
import os
from .models import CustomUser
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from hr.api import EmailNotificationSchema
from hr.email_utils import trigger_user_notification

def activate_user(request, user_id):
    # Get the user object from the database
    print("Activating user...")
    user = get_object_or_404(CustomUser, id=user_id)
    if user.is_active:
        print("User is already active.")
        return JsonResponse({"message": "User is already active."})
    
    # Activate the user
    user.is_active = True
    user.save()
    
    # Prepare the email notification data
    notification_data = EmailNotificationSchema(
        subject="Account Activation",
        message="Your account has been activated. You can now login.Thank You for registering into our app",
        recipients=[user.email]
    )
    
    # Trigger the user notification
    trigger_user_notification(request, notification_data)
     
    return JsonResponse({"message": "User activated and notification triggered successfully"})



from PIL import Image, ImageDraw, ImageFont
from django.core.mail import EmailMessage
from django.conf import settings

def create_birthday_image(employee):
    
    
    print(f"Creating birthday image for {employee.get_full_name()}...")
    
    
    # Load your image template
    
    image_path = 'api_check\media\logs\image.jpg'
    if not os.path.exists(image_path):
        print(f"Error: Template image not found at {image_path}")
        return None

    image = Image.open(image_path)
    
    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)
    
    # Define the text and font
    text = f"Happy Birthday, {employee.get_full_name()}!"
    font_path = "path/to/your/font.ttf"
    if not os.path.exists(font_path):
        print(f"Error: Font file not found at {font_path}")
        return None

    font = ImageFont.truetype(font_path, 40)  # Adjust the font size as needed
    
    # Get text size
    text_width, text_height = draw.textsize(text, font=font)
    
    # Calculate text position
    width, height = image.size
    x = (width - text_width) / 2
    y = height - text_height - 30  # Adjust the y position as needed
    
    # Add text to image
    draw.text((x, y), text, font=font, fill="white")  # Adjust text color as needed
    
    # Save the image
    output_path = f'/tmp/birthday_{employee.username}.png'
    image.save(output_path)
    print(f"Image saved at {output_path}")
    return output_path





def send_birthday_email(employee, image_path):
    subject = 'Happy Birthday!'
    message = f'Dear {employee.get_full_name()},\n\nHappy Birthday! Have a great day!\n\nBest wishes,\nYour Company'
    
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [employee.email])
    email.attach_file(image_path)
    email.send()




# utils.py
# utils.py
from PIL import Image, ImageDraw, ImageFont
from django.core.mail import EmailMessage
from django.conf import settings
import os

def create_anniversary_image(employee):
    print(f"Creating anniversary image for {employee.get_full_name()}...")
    
    # Load your image template
    image_path = os.path.join(settings.BASE_DIR, 'api_check', 'media', 'logs', 'image.jpg')
    print(f"Checking if image path exists: {image_path}")
    if not os.path.exists(image_path):
        print(f"Error: Template image not found at {image_path}")
        return None

    image = Image.open(image_path)
    
    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)
    
    # Define the text and font
    text = f"Happy Work Anniversary, {employee.get_full_name()}!"
    font_path = os.path.join(settings.BASE_DIR, 'path', 'to', 'your', 'font.ttf')
    print(f"Checking if font path exists: {font_path}")
    if not os.path.exists(font_path):
        print(f"Error: Font file not found at {font_path}")
        return None

    font = ImageFont.truetype(font_path, 40)  # Adjust the font size as needed
    
    # Get text size
    text_width, text_height = draw.textsize(text, font=font)
    
    # Calculate text position
    width, height = image.size
    x = (width - text_width) / 2
    y = height - text_height - 30  # Adjust the y position as needed
    
    # Add text to image
    draw.text((x, y), text, font=font, fill="white")  # Adjust text color as needed
    
    # Save the image
    output_path = os.path.join('/tmp', f'anniversary_{employee.username}.png')
    image.save(output_path)
    print(f"Image saved at {output_path}")
    return output_path

def send_anniversary_email(employee, image_path):
    if not image_path:
        print(f"Error: No image path provided for {employee.get_full_name()}")
        return
    
    subject = 'Happy Work Anniversary!'
    message = f'Dear {employee.get_full_name()},\n\nHappy Work Anniversary! Thank you for being a valuable part of our team.\n\nBest wishes,\nYour Company'
    
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [employee.email])
    email.attach_file(image_path)
    email.send()
    print(f"Email sent to {employee.email}")
