
import datetime
import os
import statistics
import traceback
import cv2
from ninja import Schema
from ninja.responses import JsonResponse

from django.core.exceptions import ObjectDoesNotExist
import json
from django.core.files.uploadedfile import InMemoryUploadedFile

from .schema import EmailOTPSchema
from django.shortcuts import get_object_or_404

from .models import CustomUser, MasterTable

import random
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.hashers import make_password


import requests
import random
import json
from ninja import NinjaAPI, Schema
from django.core.mail import send_mail
from django.conf import settings
from typing import List
from django.forms import ValidationError
from ninja import NinjaAPI, Schema
from django.http import Http404, HttpResponse, JsonResponse
from pydantic import BaseModel
from requests import HTTPError
from .models import BankAccount, BusinessTrip, CustomUser, DocumentForLabourCard, DocumentForPassport, DocumentForVisa, EmployeeAttendanceException, EmployeeList, DetectedFaces, EmployeeReimbursement, EmployeeResumption, EmployeeTravel, LabourContract, Leaves, MedicalReimbursement, daywiseAttendance,  userAttendance,LeaveApplication, visitingCard
# from django.contrib.auth.models import CustomUser
from rest_framework.authtoken.models import Token
from django.forms.models import model_to_dict
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from datetime import time, timedelta
import numpy as np
from django.contrib.auth import logout
from django.core.files.storage import default_storage
import base64
from django.conf import settings  # Importing settings module
from ninja.security import HttpBearer
import face_recognition
from django.core.files.storage import default_storage
from datetime import datetime
api = NinjaAPI()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token

@api.get("/bearer", auth=AuthBearer())
def bearer(request):
    return {"token": request.auth}



#<-------------AUTHENTICATION SECTION----------->


class RegisterSchema(Schema):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    image_data: str
    emp_id: str
    department: str
    designation: str
    group: str
    address: str
    country: str
    state: str
    whats_up_number: str
    date_of_birth: str
    date_joined: str

@api.post("/register")
def register_user(request, data: RegisterSchema):
    try:
        # Extract data from request
        emp_id = data.emp_id
        first_name = data.first_name
        last_name = data.last_name
        email = data.email
        password = data.password
        image_data = data.image_data
        department = data.department
        phone_number = data.phone_number
        designation = data.designation
        group = data.group
        address = data.address
        country = data.country
        state = data.state
        whats_up_number = data.whats_up_number
        date_of_birth = data.date_of_birth
        date_joined = data.date_joined

        # Combine first_name and last_name to create username
        username = f"{first_name}_{last_name}"

        # Decode the image
        image_data_decoded = base64.b64decode(image_data)
        nparr = np.frombuffer(image_data_decoded, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Convert image to RGB (face_recognition library expects RGB)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Use face_recognition to detect faces
        face_locations = face_recognition.face_locations(rgb_image)

        # Ensure at least one face is detected
        if len(face_locations) == 0:
            return JsonResponse({"error": "No face detected in the provided image"}, status=400)

        # Get the first detected face encoding
        face_encoding = face_recognition.face_encodings(rgb_image, known_face_locations=face_locations)[0]

        # Check if the face already exists in the system
        existing_faces = DetectedFaces.objects.all()
        for existing_face in existing_faces:
            stored_image_path = os.path.join(settings.MEDIA_ROOT, str(existing_face.image))
            stored_image = face_recognition.load_image_file(stored_image_path)
            stored_face_encoding = face_recognition.face_encodings(stored_image)[0]

            # Compare face encodings using face_recognition library
            matches = face_recognition.compare_faces([stored_face_encoding], face_encoding, tolerance=0.6)
            if matches[0]:
                return JsonResponse({"error": "This face is already registered to another user"}, status=400)

        # Create the user with is_active=False
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=False,
            department=department,
            designation=designation,
            phone_number=phone_number,
            emp_id=emp_id,
            group=group,
            address=address,
            country=country,
            state=state,
            whats_up_number=whats_up_number,
            date_of_birth=date_of_birth,
            date_joined=date_joined
        )

        customer = EmployeeList.objects.create(username=first_name + ' ' + last_name, email=email, status='active')

        # Save the full image
        profile_images_folder = os.path.join(settings.MEDIA_ROOT, 'profile_images')
        os.makedirs(profile_images_folder, exist_ok=True)

        image_path = f'profile_images/{username}_{user.id}.jpg'  # Path relative to media root
        cv2.imwrite(os.path.join(settings.MEDIA_ROOT, image_path), image)

        detected_face = DetectedFaces.objects.create(user=user, image=image_path, x=face_locations[0][3], y=face_locations[0][0], width=face_locations[0][1]-face_locations[0][3], height=face_locations[0][2]-face_locations[0][0])

        user_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_active": user.is_active,
            "image_path": detected_face.image.url,
            "department": user.department,
            "designation": user.designation,
            "phone_number": user.phone_number,
            "emp_id": user.emp_id,
            "group": user.group,
            "address": user.address,
            "country": user.country,
            "state": user.state,
            "whats_up_number": user.whats_up_number,
            "date_of_birth": user.date_of_birth,
            "date_joined": user.date_joined,
        }

        return JsonResponse({"message": "CustomUser registered successfully and face detected", "user": user_data})

    except Exception as e:
        return JsonResponse({"error": f"Failed to register user: {str(e)}"}, status=400)

#Admin Mail
class EmailNotificationSchema(Schema):
    subject: str
    message: str
    recipients: List[str]
    
@api.post("/send_admin_notification")
def send_admin_notification(request, notification: EmailNotificationSchema):
    subject = notification.subject
    recipients = notification.recipients
    message = notification.message
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
    return {"message": "Admin notification sent successfully"}



#<-------------------Face Login---------------------->



import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FaceLoginSchema(BaseModel):
    image_data: str

class HTTPError(Exception):
    def init(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail

def verify_eye_positions(eyes):
    if len(eyes) != 2:
        return False
    
    # Check if eyes are roughly on the same horizontal level
    y_diff = abs(eyes[0][1] - eyes[1][1])
    return y_diff < 40  # Adjust this threshold as needed

def verify_face_landmarks(image, face_location):
    landmarks = face_recognition.face_landmarks(image, [face_location])
    if not landmarks:
        return False
    
    landmarks = landmarks[0]
    expected_landmarks = ['chin', 'left_eyebrow', 'right_eyebrow', 'nose_bridge', 'nose_tip', 'left_eye', 'right_eye', 'top_lip', 'bottom_lip']
    
    return all(landmark in landmarks for landmark in expected_landmarks)

@api.post("/loginFace")
def face_login(request, data: FaceLoginSchema):
    try:
        image_data = data.image_data

        # Decoding base64 image data
        image_data_decoded = base64.b64decode(image_data)
        nparr = np.frombuffer(image_data_decoded, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPError(400, "Invalid image data")

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect face locations and encodings
        face_locations = face_recognition.face_locations(image_rgb)
        face_encodings = face_recognition.face_encodings(image_rgb, face_locations)

        if not face_encodings:
            return {'authenticated': False, 'error': "No clear face detected. Please try again."}

        # Perform eye detection
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        min_eye_size = (20, 20)
        eyes = eye_cascade.detectMultiScale(gray_image, 1.3, 5, minSize=min_eye_size)

        if len(eyes) < 2:
            return {'authenticated': False, 'error': "Both eyes must be clearly visible. Please adjust and try again."}

        if not verify_eye_positions(eyes):
            return {'authenticated': False, 'error': "Eye positions are not correct. Please adjust and try again."}

        # Iterate through each registered face and compare with provided face
        all_detected_faces = DetectedFaces.objects.all()
        for detected_face in all_detected_faces:
            user = detected_face.user
            if not user.is_active:
                continue

            stored_image_path = os.path.join(settings.MEDIA_ROOT, str(detected_face.image))
            stored_image = face_recognition.load_image_file(stored_image_path)
            stored_face_encodings = face_recognition.face_encodings(stored_image)

            if not stored_face_encodings:
                continue

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(stored_face_encodings, face_encoding, tolerance=0.4)
                face_distances = face_recognition.face_distance(stored_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                logger.info(f"Face distance: {face_distances[best_match_index]}")
                logger.info(f"Number of eyes detected: {len(eyes)}")

                if matches[best_match_index] and face_distances[best_match_index] < 0.4:
                    if verify_face_landmarks(image_rgb, face_locations[0]):
                        token, created = Token.objects.get_or_create(user=user)
                        return {'authenticated': True, 'token': token.key, 'user': model_to_dict(user)}
                    else:
                        return {'authenticated': False, 'error': "Face landmarks do not match. Please try again."}

        return {'authenticated': False, 'error': "No matching face found in the system"}

    except Exception as e:
        error_message = f"Failed to authenticate user: {e}"
        logger.error(error_message)
        logger.error(traceback.format_exc())
        raise HTTPError(400,error_message)

#<-----------------------------Login----------------------------->

import logging
logger = logging.getLogger(__name__)

class LoginSchema(Schema):
    username: str
    password: str

    

@api.post("/login")
def login(request, data: LoginSchema):
    try:
        # First, attempt to find the user in CustomUser
        user = CustomUser.objects.get(username__iexact=data.username)
    except CustomUser.DoesNotExist:
        # If user is not found in CustomUser, attempt to find entries in MasterTable
        master_entries = MasterTable.objects.filter(username__iexact=data.username)
        if not master_entries.exists():
            return JsonResponse({"error": "User not found"}, status=404)

        master_entry = master_entries.first()

        # Create the CustomUser from MasterTable entry
        user, created = CustomUser.objects.get_or_create(
            username=master_entry.username,
            defaults={
                'department': master_entry.department,
                'emp_id': master_entry.emp_id,
                'phone_number': master_entry.phone_number,
                'designation': master_entry.designation,
                'group': master_entry.group,
                'address': master_entry.address,
                'country': master_entry.country,
                'state': master_entry.state,
                'whats_up_number': master_entry.whats_up_number,
                'date_of_birth': master_entry.date_of_birth,
                'date_joined': master_entry.date_joined,
                'otp': master_entry.otp,
                'is_active': master_entry.is_active,
                'email': master_entry.email,
                'first_name': master_entry.first_name,
                'last_name': master_entry.last_name,
            }
        )

        if created:
            user.set_password(master_entry.password)
            user.save()
    else:
        # User is found in CustomUser, no need to check MasterTable
        pass

    if not user.check_password(data.password):
        return JsonResponse({"error": "Invalid password"}, status=401)

    if not user.is_active:
        return JsonResponse({"error": "Account not activated"}, status=401)

    # Generate or retrieve the token
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])
    token, created = Token.objects.get_or_create(user=user)

    # Handle additional logic for leaves, attendance, etc., if master_entries exists
    master_entries = MasterTable.objects.filter(username__iexact=data.username)
    for master_entry in master_entries:
        if not Leaves.objects.filter(master_entry=master_entry).exists():
                Leaves.objects.create(
                    master_entry=master_entry,
                    user=user,
                    emp_id=master_entry.emp_id,
                    email=master_entry.email,
                    username=f"{master_entry.first_name} {master_entry.last_name}",
                    department=master_entry.department,
                    group=master_entry.group,
                    start_date=master_entry.start_date,
                    end_date=master_entry.end_date,
                    replaced_by=master_entry.replaced_by,
                    leave_reason=master_entry.leave_reason,
                    leave_type=master_entry.leave_type,
                    category=master_entry.category,
                    passport_withdrawal_date=master_entry.passport_withdrawal_date,
                    request_for_airticket=master_entry.request_for_airticket,
                    leaves_comments=master_entry.leaves_comments,
                    leaves_status=master_entry.leaves_status,
                    leave_balance=master_entry.leave_balance,
                    duration=master_entry.duration,
                    leaves_applied_date=master_entry.leaves_applied_date,
                )
                logger.info("Leave entry created for master_entry id: %s", master_entry.id)
        else:
            logger.info("Leave entry already exists for master_entry id: %s", master_entry.id)
            
            

        if not daywiseAttendance.objects.filter(master_entry=master_entry).exists():
                daywiseAttendance.objects.create(
                    user=user,
                    master_entry=master_entry,
                    username=f"{master_entry.first_name} {master_entry.last_name}",
                    check_in=master_entry.check_in,
                    check_out=master_entry.check_out,
                    status=master_entry.status,
                    timeShortageExceed=master_entry.timeShortageExceed,
                    total_hours=master_entry.total_hours,
                    chk_date=master_entry.chk_date,
                )
                logger.info("daywiseAttendance created for emp_id: %s", master_entry.emp_id)
        else:
            logger.info("daywiseAttendance entry already exists for master_entry id: %s", master_entry.id)

        if not EmployeeAttendanceException.objects.filter(master_entry=master_entry).exists(): 
                EmployeeAttendanceException.objects.create(
                    user=user,
                    master_entry=master_entry,
                    emp_id=master_entry.emp_id,
                    email=master_entry.email,
                    username=f"{master_entry.first_name} {master_entry.last_name}",
                    department=master_entry.department,
                    group=master_entry.group,
                    date_of_exception=master_entry.date_of_exception,
                    hours_late_in=master_entry.hours_late_in,
                    minutes_late_in=master_entry.minutes_late_in,
                    hours_early_out=master_entry.hours_early_out,
                    attendanceException_reason=master_entry.attendanceException_reason,
                    attendanceException_status=master_entry.attendanceException_status,
                    reason_category=master_entry.reason_category,
                    attendanceExceptionApplied_date=master_entry.attendanceExceptionApplied_date,
                    minutes_early_out=master_entry.minutes_early_out,
                )
                logger.info("EmployeeAttendanceException created for emp_id: %s", master_entry.emp_id)
        else:
            logger.info("EmployeeAttendanceException entry already exists for master_entry id: %s", master_entry.id)
            
        if not BusinessTrip.objects.filter(master_entry=master_entry).exists():
                BusinessTrip.objects.create(
                    user=user,
                    master_entry=master_entry,
                    emp_id=master_entry.emp_id,
                    email=master_entry.email,
                    username=f"{master_entry.first_name} {master_entry.last_name}",
                    department=master_entry.department,
                    group=master_entry.group,
                    employee_name=master_entry.employee_name,
                    country_travel_to=master_entry.country_travel_to,
                    businesstrip_reason=master_entry.businesstrip_reason,
                    reimbursement_amount=master_entry.reimbursement_amount,
                    travel_request=master_entry.travel_request,
                    mode_of_payment=master_entry.mode_of_payment,
                    amount_to_be_paid_back=master_entry.amount_to_be_paid_back,
                    effective_date=master_entry.effective_date,
                    businessTrip_comments=master_entry.businessTrip_comments,
                    businessTrip_status=master_entry.businessTrip_status,
                    businessTrip_applied_date=master_entry.businessTrip_applied_date,
                )
                logger.info("BusinessTrip entry created for emp_id: %s", master_entry.emp_id)
        else:
            logger.info("BusinessTrip entry already exists for master_entry id: %s", master_entry.id)
            
        if not visitingCard.objects.filter(master_entry=master_entry).exists():
                visitingCard.objects.create(
                    user=user,
                    master_entry=master_entry,
                    email=master_entry.email,
                    username=f"{master_entry.first_name} {master_entry.last_name}",
                    mobilenum=master_entry.mobilenum,
                    designation=master_entry.designation,
                    poBox=master_entry.poBox,
                    Visitingcountry=master_entry.Visitingcountry,
                    telphone=master_entry.telphone,
                    extnum=master_entry.extnum,
                    faxnum=master_entry.faxnum,
                )
                logger.info("visitingCard entry created for emp_id: %s", master_entry.emp_id)
        else:
                logger.info("visitingCard entry entry already exists for master_entry id: %s", master_entry.id)
            
        if not EmployeeTravel.objects.filter(master_entry=master_entry).exists():
                EmployeeTravel.objects.create(
                    user=user,
                    master_entry=master_entry,
                    emp_id=master_entry.emp_id,
                    email=master_entry.email,
                    username=f"{master_entry.first_name} {master_entry.last_name}",
                    department=master_entry.department,
                    group=master_entry.group,
                    request_type=master_entry.request_type,
                    purpose_of_visit=master_entry.purpose_of_visit,
                    travel_start_date=master_entry.travel_start_date,
                    travel_end_date=master_entry.travel_end_date,
                    country_of_travel=master_entry.country_of_travel,
                    entity_company_traveling_for=master_entry.entity_company_traveling_for,
                    advance_amount_required=master_entry.advance_amount_required,
                    currency=master_entry.currency,
                    visa_to_be_processed=master_entry.visa_to_be_processed,
                    book_hotel_accommodation=master_entry.book_hotel_accommodation,
                    flight_ticket_required=master_entry.flight_ticket_required,
                    visa_letter_required=master_entry.visa_letter_required,
                    employeetravel_comments=master_entry.employeetravel_comments,
                    employeetravel_status=master_entry.employeetravel_status,
                    employeetravel_applied_date=master_entry.employeetravel_applied_date,
                )
                logger.info("EmployeeTravel entry created for emp_id: %s", master_entry.emp_id)
        else:
            logger.info("EmployeeTravel  entry already exists for master_entry id: %s", master_entry.id)
            
        if not DocumentForVisa.objects.filter(master_entry=master_entry).exists():
            DocumentForVisa.objects.create(
                    user=user,
                    master_entry=master_entry,
                    emp_id=master_entry.emp_id,
                    email=master_entry.email,
                    username=f"{master_entry.first_name} {master_entry.last_name}",
                    department=master_entry.department,
                    group=master_entry.group,
                    Visacountry_name=master_entry.Visacountry_name,
                    Visadocument_type=master_entry.Visadocument_type,
                    Visacategory=master_entry.Visacategory,
                    Visasub_category=master_entry.Visasub_category,
                    Visadocument_number=master_entry.Visadocument_number,
                    Visaissued_by=master_entry.Visaissued_by,
                    Visaissued_at=master_entry.Visaissued_at,
                    Visaissued_date=master_entry.Visaissued_date,
                    Visaissuing_authority=master_entry.Visaissuing_authority,
                    Visavalid_from=master_entry.Visavalid_from,
                    Visavalid_to=master_entry.Visavalid_to,
                    Visaverified_by=master_entry.Visaverified_by,
                    Visaverified_date=master_entry.Visaverified_date,
                    visa_number=master_entry.visa_number,
                    visa_type=master_entry.visa_type,
                    sponsor_type=master_entry.sponsor_type,
                    sponsor_name=master_entry.sponsor_name,
                    sponsor_relationship=master_entry.sponsor_relationship,
                    sponsor_number=master_entry.sponsor_number,
                    sponsor_nationality=master_entry.sponsor_nationality,
                    emirate=master_entry.emirate,
                    documentforvisa_status=master_entry.documentforvisa_status,
                    documentforvisaApplie_date=master_entry.documentforvisaApplie_date,
                )
            logger.info("DocumentForVisa created for emp_id: %s", master_entry.emp_id)
        else:
            logger.info("DocumentForVisa  entry already exists for master_entry id: %s", master_entry.id)
                              
        if not DocumentForLabourCard.objects.filter(master_entry=master_entry).exists():
                DocumentForLabourCard.objects.create(
                    user=user,
                    master_entry=master_entry,
                    emp_id=master_entry.emp_id,
                    email=master_entry.email,
                    username=f"{master_entry.first_name} {master_entry.last_name}",
                    department=master_entry.department,
                    group=master_entry.group,

                    LabourCardcountry_name=master_entry.LabourCardcountry_name,
                    LabourCarddocument_type=master_entry.LabourCarddocument_type,
                    LabourCardcategory=master_entry.LabourCardcategory,
                    LabourCardsub_category=master_entry.LabourCardsub_category,
                    LabourCarddocument_number=master_entry.LabourCarddocument_number,
                    LabourCardissued_by=master_entry.LabourCardissued_by,
                    LabourCardissued_at=master_entry.LabourCardissued_at,
                    LabourCardissued_date=master_entry.LabourCardissued_date,
                    LabourCardissuing_authority=master_entry.LabourCardissuing_authority,
                    LabourCardvalid_from=master_entry.LabourCardvalid_from,
                    LabourCardvalid_to=master_entry.LabourCardvalid_to,
                    LabourCardverified_by=master_entry.LabourCardverified_by,
                    LabourCardverified_date=master_entry.LabourCardverified_date,

                    aly_personal_id_number=master_entry.aly_personal_id_number,
                    aly_work_permit_number=master_entry.aly_work_permit_number,
                    aly_place_of_issue=master_entry.aly_place_of_issue,
                    
                    
                    documentForlabourcard_status = master_entry.documentForlabourcard_status,
                    documentForlabourcardApplied_date=master_entry.documentForlabourcardApplied_date,
                )

                logger.info("DocumentForLabourCard created for emp_id: %s", master_entry.emp_id)
        else:
            logger.info("DocumentForLabourCard entry already exists for master_entry id: %s", master_entry.id)
                       
        if not EmployeeResumption.objects.filter(master_entry=master_entry).exists():
                EmployeeResumption.objects.create(
                    user=user,
                    master_entry=master_entry,
                    emp_id=master_entry.emp_id,
                    email=master_entry.email,
                    username=f"{master_entry.first_name} {master_entry.last_name}",
                    department=master_entry.department,
                    group=master_entry.group,

                    enter_date = master_entry.enter_date,
                    resumption_Status = master_entry.resumption_Status,
                    other = master_entry.other,
                    days_overstayed = master_entry.days_overstayed,
                    resumption_comment = master_entry.resumption_comment,
                    resumption_status=master_entry.resumption_status,
                    resumptionApplied_date = master_entry.resumptionApplied_date,
                )

                logger.info("Employee Resumotion created for emp_id: %s", master_entry.emp_id)
        else:
            logger.info("Labour card entry already exists for master_entry id: %s", master_entry.id)
            
        if not EmployeeReimbursement.objects.filter(master_entry=master_entry).exists():
                EmployeeReimbursement.objects.create(
                    user=user,
                    master_entry=master_entry,
                    emp_id=master_entry.emp_id,
                    email=master_entry.email,
                    username=f"{master_entry.first_name} {master_entry.last_name}",
                    department=master_entry.department,
                    group=master_entry.group,
                    enter_amount =master_entry.enter_amount ,
                    note=master_entry.note,
                    reimbursement_type=master_entry.reimbursement_type,
                    employeereimbursement_status=master_entry.employeereimbursement_status,
                    employeereimbursement_comment =master_entry. employeereimbursement_comment ,
                    employeereimbursement_applied_date =master_entry.employeereimbursement_applied_date,
                
                )
                logger.info("EmployeeReimbursement entry created for emp_id: %s", master_entry.emp_id)
        else:
            logger.info("Labour card entry already exists for master_entry id: %s", master_entry.id)
            
        if not MedicalReimbursement.objects.filter(master_entry=master_entry).exists():
                MedicalReimbursement.objects.create(
                    user=user,
                    master_entry=master_entry,
                    emp_id=master_entry.emp_id,
                    email=master_entry.email,
                    username=f"{master_entry.first_name} {master_entry.last_name}",
                    department=master_entry.department,
                    group=master_entry.group,
                    amount_aed=master_entry.amount_aed,
                    medicalreimbursement_reason=master_entry.medicalreimbursement_reason,
                    medicalReimbursement_comments=master_entry.medicalReimbursement_comments,
                    medicalReimbursement_status=master_entry.medicalReimbursement_status,
                    medicalReimbursement_applied_date=master_entry.medicalReimbursement_applied_date,
                    type_of_claim=master_entry.type_of_claim
                )
                logger.info("Leave entry created for emp_id: %s", master_entry.emp_id)
        else:
            logger.info("Labour card entry already exists for master_entry id: %s", master_entry.id)
            
        if not BankAccount.objects.filter(master_entry=master_entry).exists():
            BankAccount.objects.create(
                user=user,
                master_entry=master_entry,
                emp_id=master_entry.emp_id,
                email=master_entry.email,
                username=f"{master_entry.first_name} {master_entry.last_name}",
                department=master_entry.department,
                group=master_entry.group,
                bank_name=master_entry.bank_name,
                branch=master_entry.branch,
                iban_number=master_entry.iban_number,
                Bankstart_date=master_entry.Bankstart_date,
                bank_code=master_entry.bank_code,
                bankaccount_comment=master_entry.bankaccount_comment,
                bankaccount_status=master_entry.bankaccount_status,
                bankaccount_applied_date=master_entry.bankaccount_applied_date,
            )
            logger.info("BankAccount entry created for emp_id: %s", master_entry.emp_id)
        else:
            logger.info("BankAccount entry already exists for master_entry id: %s", master_entry.id)
        if not DocumentForPassport.objects.filter(master_entry=master_entry).exists():
                DocumentForPassport.objects.create(
                    user=user,
                    master_entry=master_entry,
                    emp_id=master_entry.emp_id,
                    email=master_entry.email,
                    username=f"{master_entry.first_name} {master_entry.last_name}",
                    department=master_entry.department,
                    group=master_entry.group,
                    Passport_country_name=master_entry.Passport_country_name,
                    Passport_document_type=master_entry.Passport_document_type,
                    Passport_category=master_entry.Passport_category,
                    Passport_sub_category=master_entry.Passport_sub_category,
                    Passport_document_number=master_entry.Passport_document_number,
                    Passport_issued_by=master_entry.Passport_issued_by,
                    Passport_issued_at=master_entry.Passport_issued_at,
                    Passport_issued_date=master_entry.Passport_issued_date,
                    Passport_issuing_authority=master_entry.Passport_issuing_authority,
                    Passport_valid_from=master_entry.Passport_valid_from,
                    Passport_valid_to=master_entry.Passport_valid_to,
                    Passport_verified_by=master_entry.Passport_verified_by,
                    Passport_verified_date=master_entry.Passport_verified_date,
                    passport_number=master_entry.passport_number,
                    passport_type=master_entry.passport_type,
                    country_of_issue=master_entry.country_of_issue,
                    place_of_issue=master_entry.place_of_issue,
                    number_of_accompanying_person=master_entry.number_of_accompanying_person,
                    previous_passport_number=master_entry.previous_passport_number,
                    documentforpassport_status=master_entry.documentforpassport_status,
                    documentforpassportApplied_date=master_entry.documentforpassportApplied_date,
                )
                logger.info("Passport entry created for emp_id: %s", master_entry.emp_id)
        else:
            logger.info("DocumentForPassport entry already exists for master_entry id: %s", master_entry.id)
            

    user_dict = {
        'username': user.username,
        
    }

    return JsonResponse({'token': token.key, 'user': user_dict})





#<-------------------userdetails-------------------->

@api.get('/user_details')
def get_user_details(request):
    token = request.headers.get('Authorization')

    if not token:
        return JsonResponse({"error": "Authorization header missing"}, status=401)

    try:
        token = token.split()[1]
        auth = TokenAuthentication()
        user, _ = auth.authenticate_credentials(token)

        if not user.username or not user.first_name or not user.last_name or not user.email:
            return JsonResponse({"error": "Required user details are missing"}, status=400)

        # Fetch all available user data
        username = user.username
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        department=user.department
        emp_id=user.emp_id
        designation = user.designation
        phone_number = user.phone_number
        group = user.group
        address = user.address
        country = user.country
        state = user.state
        whats_up_number = user.whats_up_number
        date_of_birth  = user.date_of_birth
        date_joined  = user.date_joined
    


        # Check if face data is available
        detected_face = DetectedFaces.objects.filter(user=user).first()
        if detected_face:
            image_path = detected_face.image.name
            if default_storage.exists(image_path):
                with default_storage.open(image_path, 'rb') as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            else:
                encoded_image = None  # Set encoded_image to None if image is not found
        else:
            encoded_image = None  # Set encoded_image to None if no face is registered

        return JsonResponse({
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "user_image": encoded_image,
            "department":department,
            "emp_id":emp_id,
            "designation": designation,
            "phone_number": phone_number,
            "group" : group,
            "address" : address,
            "country" : country,
            "state" : state,
            "whats_up_number": whats_up_number,
            "date_of_birth" : date_of_birth,
            "date_joined" :date_joined,
            
            
            # Add more fields here as needed
        }, status=200)

    except IndexError:
        return JsonResponse({"error": "Token not provided"}, status=401)
    except AuthenticationFailed:
        return JsonResponse({"error": "Authentication failed"}, status=401)
    


#<-----------------------update-details--------------------->
class UserUpdateDTO(BaseModel):
    phone_number: str
    address: str
    country: str
    whats_up_number: str
    date_of_birth: str



@api.put('/update-details')
def update_user(request, user_data: UserUpdateDTO):
    token = request.headers.get('Authorization')

    if not token:
        return JsonResponse({"error": "Authorization header missing"}, status=401)


    try:
        token = token.split()[1]
        auth = TokenAuthentication()
        user, _ = auth.authenticate_credentials(token)


       
        # user.department = user_data.department
        # user.Emp_Id = user_data.Emp_Id
        user.phone_number = user_data.phone_number
        user.country=user_data.country
        user.whats_up_number=user_data.whats_up_number
        user.date_of_birth=user_data.date_of_birth
        user.address = user_data.address

            # Update other fields as needed
        user.save()
        return {"success": True, "message": "CustomUser profile updated successfully"}
    except CustomUser.DoesNotExist:
            return {"success": False, "message": "CustomUser not found"}



from PIL import Image
import io
# #edit_image



import logging

logger = logging.getLogger(__name__)

class UserImageEditSchema(Schema):
    image_data: str

# @api.put("/user_details/edit_image")
# def edit_user_image(request):
#     logger.info("Received request to edit user image")
#     if request.method != 'PUT':
#         logger.warning("Invalid method used")
#         return JsonResponse({"error": "Invalid method"}, status=405)

#     token = request.headers.get('Authorization')
#     if not token:
#         logger.warning("Authorization header missing")
#         return JsonResponse({"error": "Authorization header missing"}, status=401)

#     try:
#         token = token.split()[1]
#         auth = TokenAuthentication()
#         user, _ = auth.authenticate_credentials(token)
#         logger.info(f"User authenticated: {user.username}")

#         try:
#             body_data = json.loads(request.body.decode('utf-8'))
#             schema = UserImageEditSchema(**body_data)
#             image_data = schema.image_data
#             logger.info("Image data successfully extracted from request")
#         except (json.JSONDecodeError, KeyError, TypeError) as e:
#             logger.error(f"Invalid input data: {str(e)}")
#             return JsonResponse({"error": f"Invalid input data: {str(e)}"}, status=400)

#         image_data = image_data.strip()
#         if len(image_data) % 4 != 0:
#             image_data += '=' * (4 - len(image_data) % 4)

#         try:
#             image_data_decoded = base64.b64decode(image_data)
#             logger.info("Image data successfully decoded")
#         except (base64.binascii.Error, ValueError) as e:
#             logger.error(f"Invalid base64-encoded string: {str(e)}")
#             return JsonResponse({"error": f"Invalid base64-encoded string: {str(e)}"}, status=400)

#         image = Image.open(io.BytesIO(image_data_decoded))
#         image = np.array(image)
#         logger.info("Image successfully converted to numpy array")

#         uploaded_face_encodings = face_recognition.face_encodings(image)
#         if not uploaded_face_encodings:
#             logger.warning("No face detected in the uploaded image")
#             return JsonResponse({"error": "No face detected"}, status=400)

#         uploaded_face_encoding = uploaded_face_encodings[0]
#         logger.info("Face encoding successfully extracted from uploaded image")

#         try:
#             detected_face = DetectedFaces.objects.get(user=user)
#             existing_face_encoding = np.frombuffer(detected_face.features, dtype=np.float64)
#             distance = face_recognition.face_distance([existing_face_encoding], uploaded_face_encoding)[0]
#             logger.info(f"Face distance from existing face: {distance}")

#             if distance < 0.6:
#                 detected_face.image.save(f'{user.username}_{user.id}.jpg', io.BytesIO(image_data_decoded))
#                 detected_face.save_features(uploaded_face_encoding.tobytes())
#                 logger.info("User image successfully updated")
#                 return JsonResponse({"message": "CustomUser image updated successfully"})
#             else:
#                 logger.warning("Face does not match the current face")
#                 return JsonResponse({"error": "Face does not match the current face. Please ensure the same face is used for editing."}, status=403)
        
#         except DetectedFaces.DoesNotExist:
#             logger.info("No existing face found for user, checking against all faces")
#             existing_faces = DetectedFaces.objects.all()
#             for detected_face in existing_faces:
#                 if detected_face.features:
#                     stored_face_encoding = np.frombuffer(detected_face.features, dtype=np.float64)
#                     distance = face_recognition.face_distance([stored_face_encoding], uploaded_face_encoding)[0]
#                     logger.info(f"Comparing with user {detected_face.user.username}, distance: {distance}")
#                     if distance < 0.6:
#                         logger.warning("Face already associated with another user")
#                         return JsonResponse({"error": "This face is already associated with another user"}, status=403)

#             logger.info("Saving new face for the current user")
#             detected_face = DetectedFaces(user=user, features=uploaded_face_encoding.tobytes())
#             detected_face.image.save(f'{user.username}_{user.id}.jpg', io.BytesIO(image_data_decoded))
#             detected_face.save()
            
#             return JsonResponse({"message": "CustomUser image updated successfully"})

#     except IndexError:
#         logger.error("Token not provided")
#         return JsonResponse({"error": "Token not provided"}, status=401)
#     except AuthenticationFailed:
#         logger.error("Authentication failed")
#         return JsonResponse({"error": "Authentication failed"}, status=401)
#     except Exception as e:
#         logger.exception(f"Internal server error: {e}")
#         return JsonResponse({"error": str(e)}, status=500)


@api.put("/user_details/edit_image")
def edit_user_image(request):
    logger.info("Received request to edit user image")
    if request.method != 'PUT':
        logger.warning("Invalid method used")
        return JsonResponse({"error": "Invalid method"}, status=405)

    token = request.headers.get('Authorization')
    if not token:
        logger.warning("Authorization header missing")
        return JsonResponse({"error": "Authorization header missing"}, status=401)

    try:
        token = token.split()[1]
        auth = TokenAuthentication()
        user, _ = auth.authenticate_credentials(token)
        logger.info(f"User authenticated: {user.username}")

        try:
            body_data = json.loads(request.body.decode('utf-8'))
            schema = UserImageEditSchema(**body_data)
            image_data = schema.image_data
            logger.info("Image data successfully extracted from request")
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.error(f"Invalid input data: {str(e)}")
            return JsonResponse({"error": f"Invalid input data: {str(e)}"}, status=400)

        image_data = image_data.strip()
        if len(image_data) % 4 != 0:
            image_data += '=' * (4 - len(image_data) % 4)

        try:
            image_data_decoded = base64.b64decode(image_data)
            logger.info("Image data successfully decoded")
        except (base64.binascii.Error, ValueError) as e:
            logger.error(f"Invalid base64-encoded string: {str(e)}")
            return JsonResponse({"error": f"Invalid base64-encoded string: {str(e)}"}, status=400)

        image = Image.open(io.BytesIO(image_data_decoded))
        image = np.array(image)
        logger.info("Image successfully converted to numpy array")

        uploaded_face_encodings = face_recognition.face_encodings(image)
        if not uploaded_face_encodings:
            logger.warning("No face detected in the uploaded image")
            return JsonResponse({"error": "No face detected"}, status=400)

        uploaded_face_encoding = uploaded_face_encodings[0]
        logger.info("Face encoding successfully extracted from uploaded image")

        try:
            detected_face = DetectedFaces.objects.get(user=user)
            if detected_face.features is None:
                logger.warning("No existing face features found for user")
                # Treat this as a new face upload
                detected_face.image.save(f'{user.username}_{user.id}.jpg', io.BytesIO(image_data_decoded))
                detected_face.save_features(uploaded_face_encoding.tobytes())
                logger.info("User image successfully updated with new features")
                return JsonResponse({"message": "CustomUser image updated successfully"})
            else:
                existing_face_encoding = np.frombuffer(detected_face.features, dtype=np.float64)
                distance = face_recognition.face_distance([existing_face_encoding], uploaded_face_encoding)[0]
                logger.info(f"Face distance from existing face: {distance}")

            if distance < 0.6:
                detected_face.image.save(f'{user.username}_{user.id}.jpg', io.BytesIO(image_data_decoded))
                detected_face.save_features(uploaded_face_encoding.tobytes())
                logger.info("User image successfully updated")
                return JsonResponse({"message": "CustomUser image updated successfully"})
            else:
                logger.warning("Face does not match the current face")
                return JsonResponse({"error": "Face does not match the current face. Please ensure the same face is used for editing."}, status=403)
        
        except DetectedFaces.DoesNotExist:
            logger.info("No existing face found for user, checking against all faces")
            existing_faces = DetectedFaces.objects.all()
            for detected_face in existing_faces:
                if detected_face.features:
                    stored_face_encoding = np.frombuffer(detected_face.features, dtype=np.float64)
                    distance = face_recognition.face_distance([stored_face_encoding], uploaded_face_encoding)[0]
                    logger.info(f"Comparing with user {detected_face.user.username}, distance: {distance}")
                    if distance < 0.6:
                        logger.warning("Face already associated with another user")
                        return JsonResponse({"error": "This face is already associated with another user"}, status=403)

            logger.info("Saving new face for the current user")
            detected_face = DetectedFaces(user=user, features=uploaded_face_encoding.tobytes())
            detected_face.image.save(f'{user.username}_{user.id}.jpg', io.BytesIO(image_data_decoded))
            detected_face.save()
            
            return JsonResponse({"message": "CustomUser image updated successfully"})

    except IndexError:
        logger.error("Token not provided")
        return JsonResponse({"error": "Token not provided"}, status=401)
    except AuthenticationFailed:
        logger.error("Authentication failed")
        return JsonResponse({"error": "Authentication failed"}, status=401)
    except Exception as e:
        logger.exception(f"Internal server error: {e}")
        return JsonResponse({"error": str(e)}, status=500)




#<------------------logout------------------->

@api.post("/logout")

def logout_user(request):
    try:
        # Extract token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Authorization header missing"}, status=400)

        try:
            token = auth_header.split()[1]
        except IndexError:
            return JsonResponse({"error": "Invalid token format"}, status=400)

        # Retrieve the user associated with the token
        user = CustomUser.objects.get(auth_token=token)

        print("Logging out user...")
        # Perform user logout
        logout(request)
        print("CustomUser logged out successfully")
        return JsonResponse({"message": "CustomUser logged out successfully"})
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "CustomUser not found"}, status=404)
    except Exception as e:
        print(f"Failed to log out user: {e}")
        return JsonResponse({"error": f"Failed to log out user: {e}"}, status=400)



#<--------------------------Attendance Page----------------------------->


class FaceCheckinSchema(Schema):
    image_data: str

@api.post("/attendance/checkin")

# def check_in(request, data: FaceCheckinSchema):
#     try:
#         token = request.headers.get('Authorization').split()[1]
#         user = CustomUser.objects.get(auth_token=token)

#         print(f"Attempting check-in for user {user.id}")

#         # Perform face matching for the specific user
#         if not face_matches_authenticated_user(user, data.image_data):
#             print(f"Face matching failed for user {user.id}")
#             return JsonResponse({"error": f"Face does not match the registered face for user {user.id}"}, status=400)

#         print(f"Face matched successfully for user {user.id}")

#         current_time = timezone.localtime()

#         day_attendance, created = daywiseAttendance.objects.get_or_create(
#             user=user,
#             username=user.username,
#             check_in__date=current_time.date(),
#             chk_date=current_time.date()
#         )

#         if not day_attendance.check_in:
#             day_attendance.check_in = current_time
#             day_attendance.save()

#         day_attendance.update_status()

#         if current_time.hour == 23 and current_time.minute >= 50:
#             return JsonResponse({"message": "CustomUser automatically checked out at 11:50 PM."})

#         if current_time.hour == 0 and current_time.minute == 0:
#             userAttendance.objects.filter(user=user, check_out__isnull=True).delete()
#             attendance = userAttendance.objects.create(
#                 user=user,
#                 check_in=current_time,
#                 username=user.username,
#                 chk_date=current_time.date()
#             )
#             check_in_time = timezone.localtime(attendance.check_in)
#             print('Check-in successful at:', check_in_time)
#             return JsonResponse({"message": "Check-in successful", "check_in_time": check_in_time})

#         existing_attendance = userAttendance.objects.filter(
#             user=user,
#             check_out__isnull=True,
#             chk_date=current_time.date()
#         ).first()
        
#         if existing_attendance:
#             return JsonResponse({"error": "CustomUser is already checked in. Please check out before checking in again."})

#         attendance = userAttendance.objects.create(
#             user=user,
#             check_in=current_time,
#             username=user.username,
#             chk_date=current_time.date()
#         )
#         check_in_time = timezone.localtime(attendance.check_in).strftime("%H:%M:%S")
#         check_date = attendance.chk_date 
#         return JsonResponse({"message": "Check-in successful", "check_in_time": check_in_time, "check_date": check_date})
            
#     except CustomUser.DoesNotExist:
#         return JsonResponse({"error": "Invalid token"})
#     except IndexError:
#         return JsonResponse({"error": "Token is missing or invalid"})
#     except Exception as e:
#         return JsonResponse({"error": str(e)})

    




# @api.post("/attendance/checkout")
# def check_out(request, data: FaceCheckinSchema):
#     try:
#         token = request.headers.get('Authorization').split()[1]
#         user = CustomUser.objects.get(auth_token=token)

#         print(f"Attempting check-out for user {user.id}")

#         if not face_matches_authenticated_user(user, data.image_data):
#             print(f"Face matching failed for user {user.id}")
#             return JsonResponse({"error": f"Face does not match the authenticated user (ID: {user.id})"}, status=400)

#         print(f"Face matched successfully for user {user.id}")

#         current_time = timezone.localtime()

#         # Verify if the face matches the authenticated user
#         if not face_matches_authenticated_user(user, data.image_data):
#             print("face not matched")
#             return JsonResponse({"error": "Face does not match the authenticated user"}, status=400)

#         # Find the latest attendance record for the user
#         check_ins_today = userAttendance.objects.filter(user=user, chk_date=timezone.localtime().date(), check_in__date=timezone.localtime().date())

#         if not check_ins_today.exists():
#             raise ValidationError("No check-ins found for the user today.")

#         check_ins_without_checkout = check_ins_today.filter(check_out__isnull=True)
#         if check_ins_without_checkout.exists():
#             latest_check_in = check_ins_without_checkout.latest('check_in')
#             current_time = timezone.localtime()
#             latest_check_in.check_out = current_time
#             latest_check_in.save()
            
#             time_difference = current_time - latest_check_in.check_in
#             diff_hours = int(time_difference.total_seconds() // 3600)
#             diff_minutes = int((time_difference.total_seconds() % 3600) // 60)
#             diff_seconds = int(time_difference.total_seconds() % 60)
#             time_hours = f"{diff_hours:02}:{diff_minutes:02}:{diff_seconds:02}"
#             latest_check_in.working_hours = time_hours
            
#             total_duration = sum([(i.check_out - i.check_in).total_seconds() for i in check_ins_today if i.check_out])
#             total_hours = int(total_duration // 3600)
#             total_minutes = int((total_duration % 3600) // 60)
#             total_seconds = int(total_duration % 60)
#             latest_check_in.total_hours = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"
            
           
#             office_working_hours = 9 *3600 # 9 hours in seconds
#             time_difference_seconds = office_working_hours-total_duration

#             # Calculate absolute value of time difference
#             abs_time_difference_seconds = abs(time_difference_seconds)

#             # Calculate hours, minutes, and seconds
#             hours = int(abs_time_difference_seconds // 3600)
#             minutes = int((abs_time_difference_seconds % 3600) // 60)
#             seconds =int(abs_time_difference_seconds % 60)

#             # Determine if the time is shortage or exceed
#             if time_difference_seconds < 0:
#                 # Time shortage
#                 time_shortage_exceed_hours =  f"{hours:02}:{minutes:02}:{seconds:02}"
#             else:
#                 # Time exceed
#                 time_shortage_exceed_hours = f"-{hours}:{minutes}:{seconds}"

            
#             latest_check_in.save()  # Save changes to userAttendance table
            
#             # Update daywiseAttendance table
#             try:
#                 daywise_attendance = daywiseAttendance.objects.get(user=user, chk_date=timezone.localtime().date())
#                 daywise_attendance.check_out = current_time
#                 daywise_attendance.total_hours = latest_check_in.total_hours
#                 daywise_attendance.timeShortageExceed = time_shortage_exceed_hours
#                 daywise_attendance.save()
#             except daywiseAttendance.DoesNotExist:
#                 # If daywiseAttendance record doesn't exist, create a new one
#                 daywise_attendance = daywiseAttendance.objects.create(user=user, check_out=current_time, total_hours=latest_check_in.total_hours, chk_date=timezone.localtime().date())
#                 daywise_attendance.update_status()  # Update status as well
            
#             return {
#                 "message": "Check-out successful",
#                 "checkout_time": current_time.strftime("%H:%M:%S"),
#                 "total_hours": latest_check_in.total_hours,
#                 "working_hours": time_hours,
                
#                 "time_shortage_exceed": time_shortage_exceed_hours,
#             }
#         else:
#             raise ValidationError("No check-in without corresponding check-out found.")

#     except IndexError:
#         return {"error": "Token is missing or invalid"}
#     except AuthenticationFailed:
#         return {"error": "Authentication failed"}
#     except ValidationError as e:
#         return {"error": str(e)}
#     except CustomUser.DoesNotExist:
#         return {"error": "Invalid token"}
#     except Exception as e:
#         return {"error": str(e)}
    
# def face_matches_authenticated_user(user, image_data):
#     try:
#         print(f"Attempting face match for user {user.id}")

#         # Decode base64 image data
#         image_data_decoded = base64.b64decode(image_data)
#         nparr = np.frombuffer(image_data_decoded, np.uint8)
#         image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#         if image is None:
#             print("Invalid image data")
#             return False

#         # Convert BGR to RGB
#         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#         # Detect face locations and encodings
#         face_locations = face_recognition.face_locations(image_rgb)
#         face_encodings = face_recognition.face_encodings(image_rgb, face_locations)

#         if not face_encodings:
#             print("No clear face detected")
#             return False

        
#         detected_face = DetectedFaces.objects.filter(user=user).first()
#         if detected_face is None:
#             print(f"No registered face found")
#             #  print(f"No registered face found for user {user.id}")
#             return False

#         stored_image_path = os.path.join(settings.MEDIA_ROOT, str(detected_face.image))
#         if not os.path.exists(stored_image_path):
#             # print(f"Stored image file not found for user {user.id}")
#             print(f"Stored image file not found")
#             return False

#         stored_image = face_recognition.load_image_file(stored_image_path)
#         stored_face_encodings = face_recognition.face_encodings(stored_image)

#         if not stored_face_encodings:
#             print(f"No face encodings found in stored image")
#             # print(f"No face encodings found in stored image for user {user.id}")
#             return False

#         for face_encoding in face_encodings:
#             matches = face_recognition.compare_faces(stored_face_encodings, face_encoding, tolerance=0.4)
#             face_distances = face_recognition.face_distance(stored_face_encodings, face_encoding)
#             best_match_index = np.argmin(face_distances)

#             if matches[best_match_index] and face_distances[best_match_index] < 0.4:
#                 if verify_face_landmarks(image_rgb, face_locations[0]):
#                     print(f"Image comparison successful")
#                     # print(f"Image comparison successful for user {user.id}")
#                     return True
#                 else:
#                     print("Face landmarks do not match")
#                     return False

#         print("No matching face found")
#         return False

#     except Exception as e:
#         print(f"Unexpected error during image comparison for user {user.id}: {str(e)}")
#         return False
def check_in(request, data: FaceCheckinSchema):
    try:
        token = request.headers.get('Authorization').split()[1]
        user = CustomUser.objects.get(auth_token=token)

        print(f"Attempting check-in for user {user.id}")

        # Perform face matching for the specific user
        if not face_matches_authenticated_user(user, data.image_data):
            print(f"Face matching failed for user {user.id}")
            return JsonResponse({"error": f"Face does not match the registered face for user {user.id}"}, status=400)

        print(f"Face matched successfully for user {user.id}")

        current_time = timezone.localtime()

        day_attendance, created = daywiseAttendance.objects.get_or_create(
            user=user,
            username=user.username,
            check_in__date=current_time.date(),
            chk_date=current_time.date()
        )

        if not day_attendance.check_in:
            day_attendance.check_in = current_time
            day_attendance.save()

        day_attendance.update_status()

        if current_time.hour == 23 and current_time.minute >= 50:
            return JsonResponse({"message": "CustomUser automatically checked out at 11:50 PM."})

        if current_time.hour == 0 and current_time.minute == 0:
            userAttendance.objects.filter(user=user, check_out__isnull=True).delete()
            attendance = userAttendance.objects.create(
                user=user,
                check_in=current_time,
                username=user.username,
                chk_date=current_time.date()
            )
            check_in_time = timezone.localtime(attendance.check_in)
            print('Check-in successful at:', check_in_time)
            return JsonResponse({"message": "Check-in successful", "check_in_time": check_in_time})

        existing_attendance = userAttendance.objects.filter(
            user=user,
            check_out__isnull=True,
            chk_date=current_time.date()
        ).first()
        
        if existing_attendance:
            return JsonResponse({"error": "CustomUser is already checked in. Please check out before checking in again."})

        attendance = userAttendance.objects.create(
            user=user,
            check_in=current_time,
            username=user.username,
            chk_date=current_time.date()
        )
        check_in_time = timezone.localtime(attendance.check_in).strftime("%H:%M:%S")
        check_date = attendance.chk_date 
        return JsonResponse({"message": "Check-in successful", "check_in_time": check_in_time, "check_date": check_date})
            
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "Invalid token"})
    except IndexError:
        return JsonResponse({"error": "Token is missing or invalid"})
    except Exception as e:
        return JsonResponse({"error": str(e)})

    




@api.post("/attendance/checkout")
def check_out(request, data: FaceCheckinSchema):
    try:
        token = request.headers.get('Authorization').split()[1]
        user = CustomUser.objects.get(auth_token=token)

        print(f"Attempting check-out for user {user.id}")

        if not face_matches_authenticated_user(user, data.image_data):
            print(f"Face matching failed for user {user.id}")
            return JsonResponse({"error": f"Face does not match the authenticated user (ID: {user.id})"}, status=400)

        print(f"Face matched successfully for user {user.id}")

        current_time = timezone.localtime()

        # Verify if the face matches the authenticated user
        if not face_matches_authenticated_user(user, data.image_data):
            print("face not matched")
            return JsonResponse({"error": "Face does not match the authenticated user"}, status=400)

        # Find the latest attendance record for the user
        check_ins_today = userAttendance.objects.filter(user=user, chk_date=timezone.localtime().date(), check_in__date=timezone.localtime().date())

        if not check_ins_today.exists():
            raise ValidationError("No check-ins found for the user today.")

        check_ins_without_checkout = check_ins_today.filter(check_out__isnull=True)
        if check_ins_without_checkout.exists():
            latest_check_in = check_ins_without_checkout.latest('check_in')
            current_time = timezone.localtime()
            latest_check_in.check_out = current_time
            latest_check_in.save()
            
            time_difference = current_time - latest_check_in.check_in
            diff_hours = int(time_difference.total_seconds() // 3600)
            diff_minutes = int((time_difference.total_seconds() % 3600) // 60)
            diff_seconds = int(time_difference.total_seconds() % 60)
            time_hours = f"{diff_hours:02}:{diff_minutes:02}:{diff_seconds:02}"
            latest_check_in.working_hours = time_hours
            
            total_duration = sum([(i.check_out - i.check_in).total_seconds() for i in check_ins_today if i.check_out])
            total_hours = int(total_duration // 3600)
            total_minutes = int((total_duration % 3600) // 60)
            total_seconds = int(total_duration % 60)
            latest_check_in.total_hours = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"
            
           
            office_working_hours = 9 *3600 # 9 hours in seconds
            time_difference_seconds = office_working_hours-total_duration

            # Calculate absolute value of time difference
            abs_time_difference_seconds = abs(time_difference_seconds)

            # Calculate hours, minutes, and seconds
            hours = int(abs_time_difference_seconds // 3600)
            minutes = int((abs_time_difference_seconds % 3600) // 60)
            seconds =int(abs_time_difference_seconds % 60)

            # Determine if the time is shortage or exceed
            if time_difference_seconds < 0:
                # Time shortage
                time_shortage_exceed_hours =  f"{hours:02}:{minutes:02}:{seconds:02}"
            else:
                # Time exceed
                time_shortage_exceed_hours = f"-{hours}:{minutes}:{seconds}"

            
            latest_check_in.save()  # Save changes to userAttendance table
            
            # Update daywiseAttendance table
            try:
                daywise_attendance = daywiseAttendance.objects.get(user=user, chk_date=timezone.localtime().date())
                daywise_attendance.check_out = current_time
                daywise_attendance.total_hours = latest_check_in.total_hours
                daywise_attendance.timeShortageExceed = time_shortage_exceed_hours
                daywise_attendance.save()
            except daywiseAttendance.DoesNotExist:
                # If daywiseAttendance record doesn't exist, create a new one
                daywise_attendance = daywiseAttendance.objects.create(user=user, check_out=current_time, total_hours=latest_check_in.total_hours, chk_date=timezone.localtime().date())
                daywise_attendance.update_status()  # Update status as well
            
            return {
                "message": "Check-out successful",
                "checkout_time": current_time.strftime("%H:%M:%S"),
                "total_hours": latest_check_in.total_hours,
                "working_hours": time_hours,
                
                "time_shortage_exceed": time_shortage_exceed_hours,
            }
        else:
            raise ValidationError("No check-in without corresponding check-out found.")

    except IndexError:
        return {"error": "Token is missing or invalid"}
    except AuthenticationFailed:
        return {"error": "Authentication failed"}
    except ValidationError as e:
        return {"error": str(e)}
    except CustomUser.DoesNotExist:
        return {"error": "Invalid token"}
    except Exception as e:
        return {"error": str(e)}
    
def face_matches_authenticated_user(user, image_data):
    try:
        print(f"Attempting face match for user {user.id}")

        # Decode base64 image data
        image_data_decoded = base64.b64decode(image_data)
        nparr = np.frombuffer(image_data_decoded, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            print("Invalid image data")
            return False

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect face locations and encodings
        face_locations = face_recognition.face_locations(image_rgb)
        face_encodings = face_recognition.face_encodings(image_rgb, face_locations)

        if not face_encodings:
            print("No clear face detected")
            return False

        # Perform eye detection
        # eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # min_eye_size = (20, 20)
        # eyes = eye_cascade.detectMultiScale(gray_image, 1.3, 5, minSize=min_eye_size)

        # if len(eyes) < 2:
        #     print("Both eyes must be clearly visible")
        #     return False

        # if not verify_eye_positions(eyes):
        #     print("Eye positions are not correct")
        #     return False

        # Retrieve the registered face for the specific user
        detected_face = DetectedFaces.objects.filter(user=user).first()
        if detected_face is None:
            print(f"No registered face found for user {user.id}")
            return False

        stored_image_path = os.path.join(settings.MEDIA_ROOT, str(detected_face.image))
        if not os.path.exists(stored_image_path):
            print(f"Stored image file not found for user {user.id}")
            return False

        stored_image = face_recognition.load_image_file(stored_image_path)
        stored_face_encodings = face_recognition.face_encodings(stored_image)

        if not stored_face_encodings:
            print(f"No face encodings found in stored image for user {user.id}")
            return False

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(stored_face_encodings, face_encoding, tolerance=0.4)
            face_distances = face_recognition.face_distance(stored_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index] and face_distances[best_match_index] < 0.4:
                if verify_face_landmarks(image_rgb, face_locations[0]):
                    print(f"Image comparison successful for user {user.id}")
                    return True
                else:
                    print("Face landmarks do not match")
                    return False

        print("No matching face found")
        return False

    except Exception as e:
        print(f"Unexpected error during image comparison for user {user.id}: {str(e)}")
        return False





#<-----------------------------SERVICE FORMS------------------------------>



#<---------------medical-reimbursement------------->



class MedicalReimbursementSchema(Schema):
    username: str
    emp_id: str
    email: str
    group: str
    department: str
    medicalreimbursement_reason: str
    type_of_claim: str
    amount_aed: float
    medicalReimbursement_comments: str


@api.post("/medical-reimbursement")
def create_labour_contract(request, data: MedicalReimbursementSchema):
    # Extract token from Authorization header
    token = request.headers.get('Authorization')
    if not token:
        return 401, {"error": "Authorization header missing"}
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return 401, {"error": "Invalid token"}
    
    
    attached_file: InMemoryUploadedFile = request.FILES.get('attachment')

    # Create Medical Reimbursement object
    reimbursement_data = MedicalReimbursement.objects.create(
        user=user,
        username=data.username,
        emp_id=data.emp_id,
        email=data.email,
        group=data.group,
        department=data.department,
        medicalreimbursement_reason=data.medicalreimbursement_reason,
        type_of_claim=data.type_of_claim,
        amount_aed=data.amount_aed,
        medicalReimbursement_comments=data.medicalReimbursement_comments,
        medicalReimbursement_status="pending",
        medicalReimbursement_applied_date=timezone.now(),
    )
    return JsonResponse({"message": "CustomUser medical apply request"})

@api.get("/medical-data")
def get_leave_applications(request):
    try:
        # Extract the token from the Authorization header
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return JsonResponse({"error": "Authorization header is missing"}, status=401)

        # Split the Authorization header to extract the token
        token_parts = authorization_header.split()

        if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
            return JsonResponse({"error": "Invalid Authorization header format"}, status=401)

        # Extract the token
        token = token_parts[1]

        # Authenticate the user using the token
        auth = TokenAuthentication()
        user, _ = auth.authenticate_credentials(token)

        # Retrieve leave applications associated with the authenticated user
        user_medical_applications = MedicalReimbursement.objects.filter(user=user)

        # Serialize the leave applications data
        leave_applications_data = []
        for application in user_medical_applications:
            application_data = {
                "id": application.id,
                "username": application.user.username,
                "emp_id":application.user.emp_id,
                "department":application.department,
                "group":application.group,
                "email": application.email,
                "medicalreimbursement_reason": application.medicalreimbursement_reason,
                "type_of_claim": application.type_of_claim,
                "medicalReimbursement_status": application.medicalReimbursement_status,
                "amount_aed":application.amount_aed,
                "medicalReimbursement_comments":application.medicalReimbursement_comments,
                "medicalReimbursement_applied_date": application.medicalReimbursement_applied_date.strftime('%d-%m-%Y'),
           
                
            }
            leave_applications_data.append(application_data)

        # Return the leave applications data as JSON response
        return JsonResponse(leave_applications_data, safe=False)

    except AuthenticationFailed:
        return JsonResponse({"error": "Authentication failed"}, status=401)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api.put("/medical-reimbursement/{id}")
def update_labour_contract(request, id, data: MedicalReimbursementSchema):
    # Extract token from Authorization header
    token = request.headers.get('Authorization')
    if not token:
        return 401, {"error": "Authorization header missing"}
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return 401, {"error": "Invalid token"}

    # Retrieve the medical reimbursement object
    try:
        reimbursement = MedicalReimbursement.objects.get(id=id, user=user)
    except MedicalReimbursement.DoesNotExist:
        return 404, {"error": "Medical reimbursement not found"}

    # Update the medical reimbursement object with the provided data
    
    reimbursement.username = data.username
    reimbursement.emp_id = data.emp_id
    reimbursement.email = data.email
    reimbursement.group = data.group
    reimbursement.department = data.department
    reimbursement.medicalreimbursement_reason = data.medicalreimbursement_reason
    reimbursement.type_of_claim = data.type_of_claim
    reimbursement.amount_aed = data.amount_aed
    reimbursement.medicalReimbursement_comments = data.medicalReimbursement_comments
    reimbursement.save()

    return JsonResponse({"message": "Medical reimbursement updated successfully"})

@api.get("/data-medical-reimbursement/{id}")
def get_labour_contract(request, id: int):
    
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)
    if user:
        try:
            
            
            labour_contract = MedicalReimbursement.objects.get(id=id,user=user)
            medical_data={
                "id":labour_contract.id,
                "username":labour_contract.username,
                "emp_id":labour_contract.emp_id,
                "email":labour_contract.email,
                "group":labour_contract.group,
                "department":labour_contract.department,
                "medicalreimbursement_reason": labour_contract.medicalreimbursement_reason,
                "type_of_claim":labour_contract.type_of_claim,
                "amount_aed":float(labour_contract.amount_aed),
                "medicalReimbursement_comments":labour_contract.medicalReimbursement_comments,
                "medicalReimbursement_status":labour_contract.medicalReimbursement_status
            }

            return JsonResponse(medical_data)
        except LabourContract.DoesNotExist:
            return JsonResponse({"error": "Medical Reimbursement not found"}, status=404)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)
@api.delete("/delete-medical-reimbursement/{id}")
def delete_labour_contract(request, id):
    # Extract token from Authorization header
    token = request.headers.get('Authorization')
    if not token:
        return JsonResponse({"error": "Authorization header missing"}, status=401)
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return JsonResponse({"error": "Invalid token"}, status=401)

    # Retrieve the medical reimbursement object
    try:
        reimbursement = MedicalReimbursement.objects.get(id=id, user=user)
        reimbursement.delete()
        return JsonResponse({"message": "Medical reimbursement deleted successfully"})
    except MedicalReimbursement.DoesNotExist:
        return JsonResponse({"error": "Medical reimbursement not found"}, status=404)



#<---------------labour-contract------------>

    
class LabourContractSchema(Schema):
    emp_id: str
    username: str
    department: str
    email: str
    group: str
    labourcontract_reason: str
    amendment_date: str
    labourContract_comments: str

@api.post("/labour-contract")
def create_labour_contract(request, data: LabourContractSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, proceed with creating the labour contract
        labour_contract_instance = LabourContract.objects.create(
            user=user,
            emp_id=data.emp_id,
            username=data.username,
            department=data.department,
            email=data.email,
            group=data.group,
            labourcontract_reason=data.labourcontract_reason,
            amendment_date=data.amendment_date,
            labourContract_comments=data.labourContract_comments,
            labourContract_status="pending",
            labourContract_applied_date=timezone.now()

            # Set status to "pending" by default
        )
        return {
            "id": labour_contract_instance.id,
            "labourContract_status": "pending",
        }
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)
    
@api.get("/labour-contract-get")
def get_labour_contracts(request):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, retrieve all labour contracts associated with the user
        labour_contracts = LabourContract.objects.filter(user=user)
        contracts_data = []
        for contract in labour_contracts:
            contract_data = {
                "id": contract.id,
                "emp_id": contract.emp_id,
                "username": contract.username,
                "department": contract.department,
                "email": contract.email,
                "group": contract.group,
                "labourcontract_reason": contract.labourcontract_reason,
                "amendment_date": contract.amendment_date,
                "labourContract_comments": contract.labourContract_comments,
                "labourContract_status": contract.labourContract_status,
                "labourContract_applied_date":contract.labourContract_applied_date.strftime('%d-%m-%Y')
            }
            contracts_data.append(contract_data)
        return JsonResponse(contracts_data, safe=False)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)
    
@api.get("/labour-contract-get/{contract_id}")
def get_labour_contract(request, contract_id: int):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        try:
            # If user is authenticated, retrieve the specific labour contract by ID
            contract = LabourContract.objects.get(id=contract_id, user=user)
            contract_data = {
                "id": contract.id,
                "emp_id": contract.emp_id,
                "username": contract.username,
                "department": contract.department,
                "email": contract.email,
                "group": contract.group,
                "labourcontract_reason": contract.labourcontract_reason,
                "amendment_date": contract.amendment_date,
                "labourContract_comments": contract.labourContract_comments,
                "labourContract_status": contract.labourContract_status,
                "labourContract_applied_date":contract.labourContract_applied_date.strftime('%d-%m-%Y')
            }
            return JsonResponse(contract_data)
        except LabourContract.DoesNotExist:
            return JsonResponse({"error": "Labour contract not found"}, status=404)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.put("/labour-contract/{contract_id}")
def update_labour_contract(request, contract_id, data: LabourContractSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    user = token_bearer(request)

    if user:
        try:
            labour_contract_instance = LabourContract.objects.get(id=contract_id)
        except LabourContract.DoesNotExist:
            return JsonResponse({"error": "Labour contract not found"}, status=404)

        if labour_contract_instance.user != user:
            return JsonResponse({"error": "Unauthorized access to update contract"}, status=403)

        labour_contract_instance.emp_id = data.emp_id
        labour_contract_instance.username = data.username
        labour_contract_instance.department = data.department
        labour_contract_instance.email = data.email
        labour_contract_instance.group = data.group
        labour_contract_instance.labourcontract_reason = data.labourcontract_reason
        labour_contract_instance.amendment_date = data.amendment_date
        labour_contract_instance.labourContract_comments = data.labourContract_comments
        labour_contract_instance.save()

        return {
            "id": labour_contract_instance.id,
            "labourContract_status": labour_contract_instance.labourContract_status,
        }
    else:
        return JsonResponse({"error": "Invalid token"}, status=401)
    
@api.delete("/labour-contract-delete/{contract_id}")
def delete_labour_contract(request, contract_id):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        try:
            # Attempt to retrieve the labour contract
            labour_contract = LabourContract.objects.get(id=contract_id)

            # Check if the user has permission to delete this contract
            if labour_contract.user == user:
                # Delete the contract
                labour_contract.delete()
                return JsonResponse({"message": "Labour contract deleted successfully"})
            else:
                # Return an error if the user does not have permission
                return JsonResponse({"error": "You do not have permission to delete this contract"}, status=403)
        except ObjectDoesNotExist:
            # Return an error if the contract does not exist
            return JsonResponse({"error": "Labour contract not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid token"}, status=401)
    

    
    
#<---------------Employee-reimbursement------------>
    
class EmployeeReimbursementSchema(BaseModel):
    username: str
    emp_id: str
    email: str
    group: str
    department: str
    reimbursement_type: str
    enter_amount: float
    employeereimbursement_comment: str  
    note: str

@api.post("/employee-reimbursement")
def create_employee_reimbursement(request, data: EmployeeReimbursementSchema):
    token = request.headers.get('Authorization')
    if not token:
        return JsonResponse({"error": "Authorization header missing"}, status=401)
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return JsonResponse({"error": "Invalid token"}, status=401)

    try:
        reimbursement_data = EmployeeReimbursement.objects.create(
            user=user,
            username=data.username,
            emp_id=data.emp_id,
            email=data.email,
            group=data.group,
            department=data.department,
            reimbursement_type=data.reimbursement_type,
            enter_amount=data.enter_amount,
            employeereimbursement_comment=data.employeereimbursement_comment,
            note=data.note,
            employeereimbursement_status="pending"
        )
        return JsonResponse({"id": reimbursement_data.id, "status": "pending"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api.get("/employee_reimbursement")
def get_employee_reimbursment(request):
    try:
        # Extract the token from the Authorization header
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return JsonResponse({"error": "Authorization header is missing"}, status=401)

        # Split the Authorization header to extract the token
        token_parts = authorization_header.split()

        if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
            return JsonResponse({"error": "Invalid Authorization header format"}, status=401)

        # Extract the token
        token = token_parts[1]

        # Authenticate the user using the token
        auth = TokenAuthentication()
        user, _ = auth.authenticate_credentials(token)

        # Retrieve leave applications associated with the authenticated user
        user_employee_reimbursement = EmployeeReimbursement.objects.filter(user=user)

        # Serialize the leave applications data
        employee_reimbursement_data = []
        for application in user_employee_reimbursement:
            application_data = {
                "id": application.id,
                "username": application.user.username,
                "emp_id":application.user.emp_id,
                "department":application.department,
                "group":application.group,
                "email": application.email,
                "reimbursement_type": application.reimbursement_type,
                "enter_amount":application.enter_amount,
                "employeereimbursement_comment":application.employeereimbursement_comment,
                "note": application.note,
                "employeereimbursement_applied_date": application.employeereimbursement_applied_date.strftime('%d-%m-%Y'),
                "employeereimbursement_status":application.employeereimbursement_status
           
                
            }
            employee_reimbursement_data.append(application_data)

        # Return the leave applications data as JSON response
        return JsonResponse(employee_reimbursement_data, safe=False)

    except AuthenticationFailed:
        return JsonResponse({"error": "Authentication failed"}, status=401)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api.put("/employee_reimbursement/{id}")
def update_employee_reimbursement(request, id, data: EmployeeReimbursementSchema):
    # Extract token from Authorization header
    token = request.headers.get('Authorization')
    if not token:
        return 401, {"error": "Authorization header missing"}
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return 401, {"error": "Invalid token"}

    # Retrieve the medical reimbursement object
    try:
        reimbursement = EmployeeReimbursement.objects.get(id=id, user=user)
    except EmployeeReimbursement.DoesNotExist:
        return 404, {"error": "Employee reimbursement not found"}

    # Update the medical reimbursement object with the provided data
    reimbursement.username = data.username
    reimbursement.emp_id = data.emp_id
    reimbursement.email = data.email
    reimbursement.group = data.group
    reimbursement.department = data.department
    reimbursement.reimbursement_type = data.reimbursement_type
    reimbursement.enter_amount = data.enter_amount
    reimbursement.employeereimbursement_comment = data.employeereimbursement_comment
    reimbursement.note = data.note
    reimbursement.save()

    return JsonResponse({"message": "Employee reimbursement updated successfully"})

class EmployeeReimbursementGetSchema(Schema):
    id: int
    username: str
    emp_id: str
    email: str
    group: str
    department: str
    reimbursement_type: str
    enter_amount: float
    employeereimbursement_comment: str 
    note: str

@api.get("/data-employee-reimbursement/{id}")
def get_employee_reimbursement(request, id: int):
    token = request.headers.get('Authorization')
    if not token:
        return JsonResponse({"error": "Authorization header missing"}, status=401)
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return JsonResponse({"error": "Invalid token"}, status=401)
    
    employee_reimbursement = get_object_or_404(EmployeeReimbursement, id=id)

    employee_reimbursement_schema = EmployeeReimbursementGetSchema(
        id=employee_reimbursement.id,
        username=employee_reimbursement.username,
        emp_id=employee_reimbursement.emp_id,
        email=employee_reimbursement.email,
        group=employee_reimbursement.group,
        department=employee_reimbursement.department,
        reimbursement_type=employee_reimbursement.reimbursement_type,
        enter_amount=employee_reimbursement.enter_amount,
        employeereimbursement_comment=employee_reimbursement.employeereimbursement_comment,
        note=employee_reimbursement.note
    )

    return JsonResponse(employee_reimbursement_schema.dict())


@api.delete("/delete-employee_reimbursement/{id}")
def delete_employee_reimbursement(request, id):
    # Extract token from Authorization header
    token = request.headers.get('Authorization')
    if not token:
        return JsonResponse({"error": "Authorization header missing"}, status=401)
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return JsonResponse({"error": "Invalid token"}, status=401)

    # Retrieve the medical reimbursement object
    try:
        reimbursement = EmployeeReimbursement.objects.get(id=id, user=user)
        reimbursement.delete()
        return JsonResponse({"message": "Employee reimbursement deleted successfully"})
    except EmployeeReimbursement.DoesNotExist:
        return JsonResponse({"error": "Employee reimbursement not found"}, status=404)


   
#<---------------leave-applications------------>


class LeaveApplicationSchema(Schema):
    username: str
    emp_id: str
    email: str
    department: str
    group: str
    start_date: str
    end_date: str
    replaced_by: str
    leave_reason:str
    leave_type: str
    category: str
    duration:int
    passport_withdrawal_date: str = None
    request_for_airticket: str = None
    leaves_comments: str = None
    # leaves_status : str 

@api.post("/leave-applications")
def create_leave_application(request, application: LeaveApplicationSchema):

    try:
        token = request.headers.get('Authorization')
        if not token:
            return 401, {"error": "Authorization header missing"}
        
        try:
            token = token.split()[1]
            user = Token.objects.get(key=token).user
        except (Token.DoesNotExist, IndexError):
            return 401, {"error": "Invalid token"}
    
        # Convert date strings to datetime objects
        start_date = datetime.strptime(application.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(application.end_date, "%Y-%m-%d")

        # Create the leave application
        application_instance = Leaves.objects.create(
            user=user,
            username=application.username,
            emp_id=application.emp_id,
            email=application.email,
            department=application.department,
            group=application.group,
            start_date=start_date,
            end_date=end_date,
            replaced_by=application.replaced_by,
            leave_type=application.leave_type,
            category=application.category,
            passport_withdrawal_date=application.passport_withdrawal_date,
            request_for_airticket=application.request_for_airticket,
            leaves_applied_date=timezone.now(),
            leave_reason=application.leave_reason,
            leaves_comments=application.leaves_comments,
            duration=application.duration,
            leaves_status="pending"  # Set leaves_status to "pending" by default
        )

        # Return the response if creation is successful
        return {
            "id": application_instance.id,
            "status": application_instance.leaves_status,
        }
    except Exception as e:
        # Return error response if an exception occurs
        return {
            "error": str(e)
        }

@api.get("/leave-data")
def get_labour_contracts(request):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, retrieve all labour contracts associated with the user
        labour_contracts = Leaves.objects.filter(user=user)
        contracts_data = []
        for application in labour_contracts:
            contract_data = {
                "id": application.id,
                "username": application.user.username,
                "emp_id":application.user.emp_id,
                "department":application.department,
                "email": application.email,
                "group": application.group,
                "start_date": application.start_date,
                "end_date": application.end_date,
                "leaves_status": application.leaves_status,
                "replaced_by":application.replaced_by,
                "leave_type":application.leave_type,
                "category":application.category,
                "duration":application.duration,
                "leave_reason":application.leave_reason,
                "leave_balance":application.leave_balance,
                "leaves_comments":application.leaves_comments,
                "leaves_applied_date": application.leaves_applied_date.strftime('%d-%m-%Y'),
           
            }
            contracts_data.append(contract_data)
        return JsonResponse(contracts_data, safe=False)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.put("/leave-reimbursement/{leave_id}")
def update_labour_contract(request, leave_id, data: LeaveApplicationSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        try:
            # Attempt to retrieve the labour contract by ID
            reimbursement = Leaves.objects.get(id=leave_id)
        except Leaves.DoesNotExist:
            return JsonResponse({"error": "Leaves not found"}, status=404)

        # Check if the authenticated user is the owner of the labour contract
        if reimbursement.user != user:
            return JsonResponse({"error": "Unauthorized access to update leaves reimbursement"}, status=403)

        # Update the labour contract fields
        reimbursement.username = data.username
        reimbursement.emp_id = data.emp_id
        reimbursement.email = data.email
        reimbursement.group = data.group
        reimbursement.department = data.department
        reimbursement.replaced_by = data.replaced_by
        reimbursement.start_date = data.start_date
        reimbursement.end_date = data.end_date
        reimbursement.leave_type = data.leave_type
        reimbursement.category = data.category
        reimbursement.passport_withdrawal_date = data.passport_withdrawal_date
        reimbursement.request_for_airticket = data.request_for_airticket
        reimbursement.leaves_comments = data.leaves_comments
        reimbursement.leave_reason=data.leave_reason
        reimbursement.duration=data.duration
        # Save the updated labour contract
        reimbursement.save()

        # Return success response
        return {
            "id": reimbursement.id,
            "status": reimbursement.leaves_status,
        }
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)
    
class LeaveApplicationSchema(Schema):
    id: int
    username: str
    emp_id: str
    email: str
    department: str
    group: str
    start_date: str
    end_date: str
    replaced_by: str
    leave_type: str
    category: str
    leave_reason:str
    passport_withdrawal_date: str = None
    request_for_airticket: str = None
    leaves_comments: str = None
    leaves_status: str = None
    duration:str

@api.get("/data-leave-reimbursement/{id}")
def get_labour_contract(request, id: int):
    
    token = request.headers.get('Authorization')
    if not token:
        return 401, {"error": "Authorization header missing"}
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return 401, {"error": "Invalid token"}
    
    labour_contract = get_object_or_404(Leaves, id=id)

    labour_contract_schema = LeaveApplicationSchema(
    id=labour_contract.id,
    username=labour_contract.username,
    emp_id=labour_contract.emp_id,
    email=labour_contract.email,
    group=labour_contract.group,
    department=labour_contract.department,
    replaced_by=labour_contract.replaced_by,
    start_date=str(labour_contract.start_date),  # Convert to string
    end_date=str(labour_contract.end_date),      # Convert to string
    leave_type=labour_contract.leave_type,
    leave_reason=labour_contract.leave_reason,
    category=labour_contract.category,
    passport_withdrawal_date=str(labour_contract.passport_withdrawal_date),  # Convert to string
    leaves_comments=labour_contract.leaves_comments,
    request_for_airticket=labour_contract.request_for_airticket,
    leaves_status=labour_contract.leaves_status,
    duration=str(labour_contract.duration),
)


    return labour_contract_schema.dict()

@api.delete("/delete-leave_record/{id}")
def delete_leave_record(request, id):
    # Extract token from Authorization header
    token = request.headers.get('Authorization')
    if not token:
        return JsonResponse({"error": "Authorization header missing"}, status=401)
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return JsonResponse({"error": "Invalid token"}, status=401)

    # Retrieve the medical reimbursement object
    try:
        reimbursement = Leaves.objects.get(id=id, user=user)
        reimbursement.delete()
        return JsonResponse({"message": "Employee reimbursement deleted successfully"})
    except EmployeeReimbursement.DoesNotExist:
        return JsonResponse({"error": "Employee reimbursement not found"}, status=404)



#<---------------business-trip------------>

class BusinessTripSchema(Schema):
   
    emp_id: str
    username: str
    department: str
    email: str
    group: str
    
    employee_name: str
    country_travel_to: str
    businesstrip_reason: str
    reimbursement_amount: float
    travel_request: str
    
    mode_of_payment: str
    amount_to_be_paid_back: float
    effective_date: str
    businessTrip_comments: str

@api.post("/business-trip")
def create_Business_Trip(request, data: BusinessTripSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, proceed with creating the labour contract
        business_trip_instance = BusinessTrip.objects.create(
            user=user,
            emp_id=data.emp_id,
            username=data.username,
            department=data.department,
            email=data.email,
            group=data.group,
            employee_name=data.employee_name,
            country_travel_to=data.country_travel_to,
            businesstrip_reason=data.businesstrip_reason,
            reimbursement_amount=data.reimbursement_amount,
            travel_request=data.travel_request,
            mode_of_payment=data.mode_of_payment,
            amount_to_be_paid_back=data.amount_to_be_paid_back,
            effective_date=data.effective_date,
            businessTrip_comments=data.businessTrip_comments,
            businessTrip_status="pending", # Default status is "Pending",
            businessTrip_applied_date=timezone.now()

            # Set status to "pending" by default
        )
        return {
            "id": business_trip_instance.id,
            "status": "pending",
        }
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)
    
class businessTripSchema(Schema):
    id:int
    emp_id: str
    username: str
    department: str
    email: str
    group: str
    employee_name: str
    country_travel_to: str
    businesstrip_reason: str
    reimbursement_amount: float
    travel_request: str
    mode_of_payment: str
    amount_to_be_paid_back: float
    effective_date: str
    businessTrip_comments: str

@api.get("/business-data")
def get_business_applications(request):


    try:
        # Extract the token from the Authorization header
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return JsonResponse({"error": "Authorization header is missing"}, status=401)

        # Split the Authorization header to extract the token
        token_parts = authorization_header.split()

        if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
            return JsonResponse({"error": "Invalid Authorization header format"}, status=401)

        # Extract the token
        token = token_parts[1]

        # Authenticate the user using the token
        auth = TokenAuthentication()
        user, _ = auth.authenticate_credentials(token)

        # Retrieve leave applications associated with the authenticated user
        user_business_applications = BusinessTrip.objects.filter(user=user)

        # Serialize the leave applications data
        business_applications_data = []
        for trip in user_business_applications:
            business_application_data = {
                "id": trip.id,
                "emp_id": trip.emp_id,
                "username": trip.username,
                "department": trip.department,
                "email": trip.email,
                "group": trip.group,
                "employee_name": trip.employee_name,
                "country_travel_to": trip.country_travel_to,
                "businesstrip_reason": trip.businesstrip_reason,
                "reimbursement_amount": trip.reimbursement_amount,
                "travel_request": trip.travel_request,
                "mode_of_payment": trip.mode_of_payment,
                "amount_to_be_paid_back": trip.amount_to_be_paid_back,
                "effective_date": trip.effective_date,
                "businessTrip_comments": trip.businessTrip_comments,
                "businessTrip_status": trip.businessTrip_status,
                "businessTrip_applied_date":trip.businessTrip_applied_date.strftime('%d-%m-%Y')
            }
            business_applications_data.append(business_application_data)

        # Return the leave applications data as JSON response
        return JsonResponse(business_applications_data, safe=False)

    except AuthenticationFailed:
        return JsonResponse({"error": "Authentication failed"}, status=401)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
        
@api.get("/data-business-trip/{id}")
def get_Employee_attendance_schema(request, id: int):
    token = request.headers.get('Authorization')
    if not token:
        return 401, {"error": "Authorization header missing"}
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return 401, {"error": "Invalid token"}
    
    business_trip_data= get_object_or_404(BusinessTrip, id=id)

    business_trip_schema= BusinessTripSchema(
        id=business_trip_data.id,
        emp_id=business_trip_data.emp_id,
        username=business_trip_data.username,
        department=business_trip_data.department,
        email=business_trip_data.email,
        group=business_trip_data.group,
        employee_name=business_trip_data.employee_name,
        country_travel_to=business_trip_data.country_travel_to,
        businesstrip_reason=business_trip_data.businesstrip_reason,
        reimbursement_amount=business_trip_data.reimbursement_amount,
        travel_request=business_trip_data.travel_request,
        mode_of_payment=business_trip_data.mode_of_payment,
        amount_to_be_paid_back=business_trip_data.amount_to_be_paid_back,
        effective_date=str(business_trip_data.effective_date),
        businessTrip_comments=business_trip_data.businessTrip_comments,
    )

    return business_trip_schema.dict()

@api.delete("/delete-business-trip/{business_id}")
def delete_business_trip(request, business_id):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        try:
            # Attempt to retrieve the labour contract
            business_trip = BusinessTrip.objects.get(id=business_id)

            # Check if the user has permission to delete this contract
            if business_trip.user == user:
                # Delete the contract
                business_trip.delete()
                return JsonResponse({"message": "Labour contract deleted successfully"})
            else:
                # Return an error if the user does not have permission
                return JsonResponse({"error": "You do not have permission to delete this contract"}, status=403)
        except ObjectDoesNotExist:
            # Return an error if the contract does not exist
            return JsonResponse({"error": "Labour contract not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid token"}, status=401)
    
@api.put("/Business-trip-edit/{business_id}")
def update_labour_contract(request, business_id, data: BusinessTripSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    user = token_bearer(request)

    if user:
        try:
            business_trip_instance = BusinessTrip.objects.get(id=business_id)
        except BusinessTrip.DoesNotExist:
            return JsonResponse({"error": "Labour contract not found"}, status=404)

        if business_trip_instance.user != user:
            return JsonResponse({"error": "Unauthorized access to update contract"}, status=403)

    # Update the medical reimbursement object with the provided data
        business_trip_instance.emp_id = data.emp_id
        business_trip_instance.username = data.username
        business_trip_instance.department = data.department
        business_trip_instance.email = data.email
        business_trip_instance.group = data.group
        business_trip_instance.businesstrip_reason = data.businesstrip_reason
        business_trip_instance.employee_name = data.employee_name
        business_trip_instance.country_travel_to = data.country_travel_to
        business_trip_instance.reimbursement_amount = data.reimbursement_amount
        business_trip_instance.travel_request = data.travel_request
        business_trip_instance.mode_of_payment = data.mode_of_payment
        business_trip_instance.amount_to_be_paid_back = data.amount_to_be_paid_back
        business_trip_instance.effective_date = data.effective_date
        business_trip_instance.businessTrip_comments = data.businessTrip_comments
        
        business_trip_instance.save()

        return {
            "id": business_trip_instance.id,
            "status": business_trip_instance.status,
        }
    else:
        return JsonResponse({"error": "Invalid token"}, status=401)



#<---------------ATTENDANCE EXCEPTION------------>

class EmployeeAttendanceExceptionSchema(Schema):
    username: str
    emp_id: str
    email: str
    group: str

    department: str
    date_of_exception: str
    hours_late_in : str
    minutes_late_in : str

    hours_early_out : str
    minutes_early_out : str
    reason_category : str
    attendanceException_reason: str  



@api.post("/post-attendace-exception-data")
def attendace_exception(request, data: EmployeeAttendanceExceptionSchema):
    # Extract token from Authorization header
    token = request.headers.get('Authorization')
    if not token:
        return 401, {"error": "Authorization header missing"}
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return 401, {"error": "Invalid token"}
    
    
    
    # Create Medical Reimbursement object
    reimbursement_data = EmployeeAttendanceException.objects.create(
        user=user,
        username=data.username,
        emp_id=data.emp_id,
        email=data.email,
        group=data.group,
        department=data.department,

        reason_category=data.reason_category,
        date_of_exception=data.date_of_exception,

        hours_late_in = data.hours_late_in,
        minutes_late_in = data.minutes_late_in,
        hours_early_out = data.hours_early_out,
        minutes_early_out = data.minutes_early_out,

        attendanceException_reason = data.attendanceException_reason,

        attendanceException_status="pending",
        attendanceExceptionApplied_date=timezone.now(),
       
       
    )
    return JsonResponse({"message": "CustomUser medical apply request"})

class EmployeeAttendanceExceptionalSchema(Schema):
    username: str
    emp_id: str
    email: str
    group: str

    department: str
    date_of_exception: str
    hours_late_in : str
    minutes_late_in : str

    hours_early_out : str
    minutes_early_out : str
    reason_category : str
    attendanceException_reason: str  
    id:int



@api.get("/history-attendace-exception-data")
def get_employeeattendace_exception(request):
    try:
        # Extract the token from the Authorization header
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return JsonResponse({"error": "Authorization header is missing"}, status=401)

        # Split the Authorization header to extract the token
        token_parts = authorization_header.split()

        if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
            return JsonResponse({"error": "Invalid Authorization header format"}, status=401)

        # Extract the token
        token = token_parts[1]

        # Authenticate the user using the token
        auth = TokenAuthentication()
        user, _ = auth.authenticate_credentials(token)

        # Retrieve leave applications associated with the authenticated user
        user_employeeattendace_exception = EmployeeAttendanceException.objects.filter(user=user)

        # Serialize the leave applications data
        employeeattendace_exception_data = []
        for application in user_employeeattendace_exception:
            application_data = {
                "id": application.id,
                "username": application.username,
                "emp_id":application.emp_id,
                "department":application.department,
                "email": application.email,
                "group":application.group,
                "date_of_exception": application.date_of_exception,
                "hours_late_in": application.hours_late_in,
                "minutes_late_in": application.minutes_late_in,
                "hours_early_out": application.hours_early_out,
                "minutes_early_out":application.minutes_early_out,
                "reason_category":application.reason_category,
                "attendanceException_reason":application.attendanceException_reason,
                "attendanceExceptionApplied_date": application.attendanceExceptionApplied_date.strftime('%d-%m-%Y'),
                "attendanceException_status":application.attendanceException_status
           
                
            }
            employeeattendace_exception_data.append(application_data)

        # Return the leave applications data as JSON response
        return JsonResponse(employeeattendace_exception_data, safe=False)

    except AuthenticationFailed:
        return JsonResponse({"error": "Authentication failed"}, status=401)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api.get("/data-attendace-exception/{id}")
def get_Employee_attendance_schema(request, id: int):
    token = request.headers.get('Authorization')
    if not token:
        return 401, {"error": "Authorization header missing"}
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return 401, {"error": "Invalid token"}
    
    attendance_exception = get_object_or_404(EmployeeAttendanceException, id=id)

    employee_attendance_schema = EmployeeAttendanceExceptionSchema(
        id=attendance_exception.id,
        username=attendance_exception.username,
        emp_id=attendance_exception.emp_id,
        email=attendance_exception.email,
        group=attendance_exception.group,
        department=attendance_exception.department,
        attendanceException_reason=attendance_exception.attendanceException_reason,
        reason_category=attendance_exception.reason_category,
        date_of_exception=str(attendance_exception.date_of_exception),
        hours_late_in=str(attendance_exception.hours_late_in),
        minutes_late_in=str(attendance_exception.minutes_late_in),
        hours_early_out=str(attendance_exception.hours_early_out),
        minutes_early_out=str(attendance_exception.minutes_early_out),
    )

    return employee_attendance_schema.dict()

@api.put("/put-attendace-exception-data/{id}")
def update_attendance_exception(request, id, data: EmployeeAttendanceExceptionSchema):
    # Extract token from Authorization header
    token = request.headers.get('Authorization')
    if not token:
        return 401, {"error": "Authorization header missing"}
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return 401, {"error": "Invalid token"}

    # Retrieve the medical reimbursement object
    try:
        reimbursement = EmployeeAttendanceException.objects.get(id=id, user=user)
    except EmployeeAttendanceException.DoesNotExist:
        return 404, {"error": "Employee reimbursement not found"}

    # Update the medical reimbursement object with the provided data
    reimbursement.username = data.username
    reimbursement.emp_id = data.emp_id
    reimbursement.email = data.email
    reimbursement.group = data.group
    reimbursement.department = data.department
    reimbursement.attendanceException_reason = data.attendanceException_reason
    reimbursement.date_of_exception=data.date_of_exception
    reimbursement.hours_late_in = data.hours_late_in
    reimbursement.hours_early_out = data.hours_early_out
    reimbursement.minutes_early_out = data.minutes_early_out
    reimbursement.minutes_late_in = data.minutes_late_in
    reimbursement.reason_category = data.reason_category
    reimbursement.hours_early_out = data.hours_early_out

    reimbursement.save()

    return JsonResponse({"message": "Medical reimbursement updated successfully"})


@api.delete("/delete-attendace-exception-data/{id}")
def delete_attendance_exception(request, id):
    # Extract token from Authorization header
    token = request.headers.get('Authorization')
    if not token:
        return JsonResponse({"error": "Authorization header missing"}, status=401)
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return JsonResponse({"error": "Invalid token"}, status=401)

    # Retrieve the medical reimbursement object
    try:
        reimbursement = EmployeeAttendanceException.objects.get(id=id, user=user)
        reimbursement.delete()
        return JsonResponse({"message": "Employee Attendance Exception deleted successfully"})
    except EmployeeAttendanceException.DoesNotExist:
        return JsonResponse({"error": "Employee Attendance Exception not found"}, status=404)
    
    
#<---------------DOCUMENT VIISA------------>
    
class DocumentVisaSchema(Schema):
    emp_id: str
    username: str
    department: str
    email: str
    group: str
    Visacountry_name: str
    Visadocument_type:str
    Visacategory:str
    Visasub_category:str
    Visadocument_number: str
    Visaissued_by:str
    Visaissued_at:str
    Visaissued_date:str
    Visaissuing_authority: str
    Visavalid_from:str
    Visavalid_to:str
    Visaverified_by:str
    Visaverified_date: str
    visa_number:str
    visa_type:str
    sponsor_type:str
    sponsor_name: str
    sponsor_relationship:str
    sponsor_number:str
    sponsor_nationality:str
    emirate:str
    
@api.post("/document-visa")
def document_visa_application(request, data: DocumentVisaSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, proceed with creating the labour contract
        document_visa_instance = DocumentForVisa.objects.create(
            user=user,
            emp_id=data.emp_id,
            username=data.username,
            department=data.department,
            email=data.email,
            group=data.group,
            Visacountry_name=data.Visacountry_name,
            Visadocument_type=data.Visadocument_type,
            Visacategory=data.Visacategory,
            Visasub_category=data.Visasub_category,
            Visadocument_number=data.Visadocument_number,
            Visaissued_by=data.Visaissued_by,
            Visaissued_at=data.Visaissued_at,
            Visaissued_date=data.Visaissued_date,
            Visaissuing_authority=data.Visaissuing_authority,
            Visavalid_from=data.Visavalid_from,
            Visavalid_to=data.Visavalid_to,
            Visaverified_by=data.Visaverified_by,
            Visaverified_date=data.Visaverified_date,
            visa_number=data.visa_number,
            visa_type=data.visa_type,
            sponsor_type=data.sponsor_type,
            sponsor_name=data.sponsor_name,
            sponsor_relationship=data.sponsor_relationship,
            sponsor_number=data.sponsor_number,
            sponsor_nationality=data.sponsor_nationality,
            emirate=data.emirate,
            documentforvisa_status="pending",
            documentforvisaApplie_date=timezone.now()

            # Set status to "pending" by default
        )
        return {
            "id": document_visa_instance.id,
            "documentforvisa_status": "pending",
        }
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.get("/Document-visa-get")
def get_document_visa(request):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, retrieve all document visa instances associated with the user
        document_visa_instances = DocumentForVisa.objects.filter(user=user)
        visa_data = []
        for visa in document_visa_instances:
            visa_data.append({
                "id": visa.id,
                "emp_id": visa.emp_id,
                "username": visa.username,
                "department": visa.department,
                "email": visa.email,
                "group": visa.group,
                "Visacountry_name": visa.Visacountry_name,
                "Visadocument_type": visa.Visadocument_type,
                "Visacategory": visa.Visacategory,
                "Visasub_category": visa.Visasub_category,
                "Visadocument_number": visa.Visadocument_number,
                "Visaissued_by": visa.Visaissued_by,
                "Visaissued_at": visa.Visaissued_at,
                "Visaissued_date": visa.Visaissued_date,
                "Visaissuing_authority": visa.Visaissuing_authority,
                "Visavalid_from": visa.Visavalid_from,
                "Visavalid_to": visa.Visavalid_to,
                "Visaverified_by": visa.Visaverified_by,
                "Visaverified_date": visa.Visaverified_date,
                "visa_number": visa.visa_number,
                "visa_type": visa.visa_type,
                "sponsor_type": visa.sponsor_type,
                "sponsor_name": visa.sponsor_name,
                "sponsor_relationship": visa.sponsor_relationship,
                "sponsor_number": visa.sponsor_number,
                "sponsor_nationality": visa.sponsor_nationality,
                "emirate": visa.emirate,
                "documentforvisa_status": visa.documentforvisa_status,
                "documentforvisaApplie_date": visa.documentforvisaApplie_date.strftime('%d-%m-%Y')
            })
        return JsonResponse(visa_data, safe=False)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.get("/Document-visa-get-id/{visa_id}")
def get_document_visa_by_id(request, visa_id):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, retrieve the document visa instance by ID
        try:
            visa_instance = DocumentForVisa.objects.get(id=visa_id, user=user)
            visa_data = {
                "id": visa_instance.id,
                "emp_id": visa_instance.emp_id,
                "username": visa_instance.username,
                "department": visa_instance.department,
                "email": visa_instance.email,
                "group": visa_instance.group,
                "Visacountry_name": visa_instance.Visacountry_name,
                "Visadocument_type": visa_instance.Visadocument_type,
                "Visacategory": visa_instance.Visacategory,
                "Visasub_category": visa_instance.Visasub_category,
                "Visadocument_number": visa_instance.Visadocument_number,
                "Visaissued_by": visa_instance.Visaissued_by,
                "Visaissued_at": visa_instance.Visaissued_at,
                "Visaissued_date": visa_instance.Visaissued_date,
                "Visaissuing_authority": visa_instance.Visaissuing_authority,
                "Visavalid_from": visa_instance.Visavalid_from,
                "Visavalid_to": visa_instance.Visavalid_to,
                "Visaverified_by": visa_instance.Visaverified_by,
                "Visaverified_date": visa_instance.Visaverified_date,
                "visa_number": visa_instance.visa_number,
                "visa_type": visa_instance.visa_type,
                "sponsor_type": visa_instance.sponsor_type,
                "sponsor_name": visa_instance.sponsor_name,
                "sponsor_relationship": visa_instance.sponsor_relationship,
                "sponsor_number": visa_instance.sponsor_number,
                "sponsor_nationality": visa_instance.sponsor_nationality,
                "emirate": visa_instance.emirate,
                "documentforvisa_status": visa_instance.documentforvisa_status,
                "documentforvisaApplie_date": visa_instance.documentforvisaApplie_date.strftime('%d-%m-%Y')
            }
            return JsonResponse(visa_data)
        except DocumentForVisa.DoesNotExist:
            return JsonResponse({"error": "Document visa not found"}, status=404)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.put("/Document-visa/{visa_id}")
def update_document_visa(request, visa_id, data: DocumentVisaSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    user = token_bearer(request)

    if user:
        try:
            document_visa_instance = DocumentForVisa.objects.get(id=visa_id)
        except DocumentForVisa.DoesNotExist:
            return JsonResponse({"error": "Document visa not found"}, status=404)

        if document_visa_instance.user != user:
            return JsonResponse({"error": "Unauthorized access to update Document visa"}, status=403)

        document_visa_instance.emp_id = data.emp_id
        document_visa_instance.username = data.username
        document_visa_instance.department = data.department
        document_visa_instance.email = data.email
        document_visa_instance.group = data.group

        document_visa_instance.Visacountry_name = data.Visacountry_name
        document_visa_instance.Visadocument_type = data.Visadocument_type
        document_visa_instance.Visacategory = data.Visacategory

        document_visa_instance.Visasub_category = data.Visasub_category
        document_visa_instance.Visadocument_number = data.Visadocument_number
        document_visa_instance.Visaissued_by = data.Visaissued_by

        document_visa_instance.Visaissued_at = data.Visaissued_at
        document_visa_instance.Visaissued_date = data.Visaissued_date
        document_visa_instance.Visaissuing_authority = data.Visaissuing_authority

        document_visa_instance.Visavalid_from = data.Visavalid_from
        document_visa_instance.Visavalid_to = data.Visavalid_to
        document_visa_instance.Visaverified_by = data.Visaverified_by

        document_visa_instance.Visaverified_date = data.Visaverified_date
        document_visa_instance.visa_number = data.visa_number
        document_visa_instance.visa_type = data.visa_type

        document_visa_instance.sponsor_type = data.sponsor_type
        document_visa_instance.sponsor_name = data.sponsor_name
        document_visa_instance.sponsor_relationship = data.sponsor_relationship

        document_visa_instance.sponsor_number = data.sponsor_number
        document_visa_instance.sponsor_nationality = data.sponsor_nationality
        document_visa_instance.emirate = data.emirate


        document_visa_instance.save()

        return {
            "id": document_visa_instance.id,
            "documentforvisa_status": document_visa_instance.documentforvisa_status,
        }
    else:
        return JsonResponse({"error": "Invalid token"}, status=401)
    
@api.delete("/document-visa-delete/{visa_id}")
def delete_document_visa(request, visa_id):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        try:
            # Attempt to retrieve the labour contract
            document_visa_instance = DocumentForVisa.objects.get(id=visa_id)

            # Check if the user has permission to delete this contract
            if document_visa_instance.user == user:
                # Delete the contract
                document_visa_instance.delete()
                return JsonResponse({"message": "Document Visa deleted successfully"})
            else:
                # Return an error if the user does not have permission
                return JsonResponse({"error": "You do not have permission to delete this visa"}, status=403)
        except ObjectDoesNotExist:
            # Return an error if the contract does not exist
            return JsonResponse({"error": "visa not found"}, status=404)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)


#<---------------DOCUMENT PASSPORT------------>


class  DocumentPassportSchema(Schema):
    emp_id: str
    username: str
    department: str
    email: str
    group: str
    Passport_country_name: str
    Passport_document_type:str
    Passport_category:str
    Passport_sub_category:str
    Passport_document_number: str
    Passport_issued_by:str
    Passport_issued_at:str
    Passport_issued_date:str
    Passport_issuing_authority: str
    Passport_valid_from:str
    Passport_valid_to:str
    Passport_verified_by:str
    Passport_verified_date: str
    passport_number:str
    passport_type:str
    country_of_issue:str
    place_of_issue: str
    number_of_accompanying_person:str
    previous_passport_number:str
    
@api.post("/document-passport")
def employee_exception_application(request, data: DocumentPassportSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, proceed with creating the labour contract
        employee_exception_instance = DocumentForPassport.objects.create(
            user=user,
            emp_id=data.emp_id,
            username=data.username,
            department=data.department,
            email=data.email,
            group=data.group,
            Passport_country_name=data.Passport_country_name,
            Passport_document_type=data.Passport_document_type,
            Passport_category=data.Passport_category,
            Passport_sub_category=data.Passport_sub_category,
            Passport_document_number=data.Passport_document_number,
            Passport_issued_by=data.Passport_issued_by,
            Passport_issued_at=data.Passport_issued_at,
            Passport_issued_date=data.Passport_issued_date,
            Passport_issuing_authority=data.Passport_issuing_authority,
            Passport_valid_from=data.Passport_valid_from,
            Passport_valid_to=data.Passport_valid_to,
            Passport_verified_by=data.Passport_verified_by,
            Passport_verified_date=data.Passport_verified_date,
            passport_number=data.passport_number,
            passport_type=data.passport_type,
            country_of_issue=data.country_of_issue,
            place_of_issue=data.place_of_issue,
            number_of_accompanying_person=data.number_of_accompanying_person,
            previous_passport_number=data.previous_passport_number,
            
            documentforpassport_status="pending",
            documentforpassportApplied_date=timezone.now()

            # Set status to "pending" by default
        )
        return {
            "id": employee_exception_instance.id,
            "documentforpassport_status": "pending",
        }
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.get("/Document-passport-get")
def get_employee_exception(request):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, retrieve all document passport instances associated with the user
        employee_exception_instances = DocumentForPassport.objects.filter(user=user)
        exception_data = []
        for passport in employee_exception_instances:
            exception_data.append({
                "id": passport.id,
                "emp_id": passport.emp_id,
                "username": passport.username,
                "department": passport.department,
                "email": passport.email,
                "group": passport.group,
                "Passport_country_name": passport.Passport_country_name,
                "Passport_document_type": passport.Passport_document_type,
                "Passport_category": passport.Passport_category,
                "Passport_sub_category": passport.Passport_sub_category,
                "Passport_document_number": passport.Passport_document_number,
                "Passport_issued_by": passport.Passport_issued_by,
                "Passport_issued_at": passport.Passport_issued_at,
                "Passport_issued_date": passport.Passport_issued_date,
                "Passport_issuing_authority": passport.Passport_issuing_authority,
                "Passport_valid_from": passport.Passport_valid_from,
                "Passport_valid_to": passport.Passport_valid_to,
                "Passport_verified_by": passport.Passport_verified_by,
                "Passport_verified_date": passport.Passport_verified_date,
                "passport_number": passport.passport_number,
                "passport_type": passport.passport_type,
                "country_of_issue": passport.country_of_issue,
                "place_of_issue": passport.place_of_issue,
                "number_of_accompanying_person": passport.number_of_accompanying_person,
                "previous_passport_number": passport.previous_passport_number,
                "documentforpassport_status": passport.documentforpassport_status,
                "documentforpassportApplied_date": passport.documentforpassportApplied_date.strftime('%d-%m-%Y')
            })
        return JsonResponse(exception_data, safe=False)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.get("/Document-passport-get-id/{passport_id}")
def get_document_passport_by_id(request, passport_id):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, retrieve the document passport instance by ID
        try:
            passport_instance = DocumentForPassport.objects.get(id=passport_id, user=user)
            passport_data = {
                "id": passport_instance.id,
                "emp_id": passport_instance.emp_id,
                "username": passport_instance.username,
                "department": passport_instance.department,
                "email": passport_instance.email,
                "group": passport_instance.group,
                "Passport_country_name": passport_instance.Passport_country_name,
                "Passport_document_type": passport_instance.Passport_document_type,
                "Passport_category": passport_instance.Passport_category,
                "Passport_sub_category": passport_instance.Passport_sub_category,
                "Passport_document_number": passport_instance.Passport_document_number,
                "Passport_issued_by": passport_instance.Passport_issued_by,
                "Passport_issued_at": passport_instance.Passport_issued_at,
                "Passport_issued_date": passport_instance.Passport_issued_date,
                "Passport_issuing_authority": passport_instance.Passport_issuing_authority,
                "Passport_valid_from": passport_instance.Passport_valid_from,
                "Passport_valid_to": passport_instance.Passport_valid_to,
                "Passport_verified_by": passport_instance.Passport_verified_by,
                "Passport_verified_date": passport_instance.Passport_verified_date,
                "passport_number": passport_instance.passport_number,
                "passport_type": passport_instance.passport_type,
                "country_of_issue": passport_instance.country_of_issue,
                "place_of_issue": passport_instance.place_of_issue,
                "number_of_accompanying_person": passport_instance.number_of_accompanying_person,
                "previous_passport_number": passport_instance.previous_passport_number,
                "documentforpassport_status": passport_instance.documentforpassport_status,
                "documentforpassportApplied_date": passport_instance.documentforpassportApplied_date.strftime('%d-%m-%Y')
            }
            return JsonResponse(passport_data)
        except DocumentForPassport.DoesNotExist:
            return JsonResponse({"error": "Document passport not found"}, status=404)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.delete("/document-passport-delete/{passport_id}")
def delete_employee_exception(request, passport_id):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        try:
            # Attempt to retrieve the labour contract
            employee_exception_instance = DocumentForPassport.objects.get(id=passport_id)

            # Check if the user has permission to delete this contract
            if employee_exception_instance.user == user:
                # Delete the contract
                employee_exception_instance.delete()
                return JsonResponse({"message": "Document passport deleted successfully"})
            else:
                # Return an error if the user does not have permission
                return JsonResponse({"error": "You do not have permission to delete this passport"}, status=403)
        except ObjectDoesNotExist:
            # Return an error if the contract does not exist
            return JsonResponse({"error": "passport not found"}, status=404)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.put("/Document-passport/{contract_id}")
def update_employee_exception(request, contract_id, data: DocumentPassportSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    user = token_bearer(request)

    if user:
        try:
            employee_exception_instance = DocumentForPassport.objects.get(id=contract_id)
        except DocumentForPassport.DoesNotExist:
            return JsonResponse({"error": "Document passport not found"}, status=404)

        if employee_exception_instance.user != user:
            return JsonResponse({"error": "Unauthorized access to update Document passport"}, status=403)

        employee_exception_instance.emp_id = data.emp_id
        employee_exception_instance.username = data.username
        employee_exception_instance.department = data.department
        employee_exception_instance.email = data.email
        employee_exception_instance.group = data.group

        employee_exception_instance.Passport_country_name = data.Passport_country_name
        employee_exception_instance.Passport_document_type = data.Passport_document_type
        employee_exception_instance.Passport_category = data.Passport_category

        employee_exception_instance.Passport_sub_category = data.Passport_sub_category
        employee_exception_instance.Passport_document_number = data.Passport_document_number
        employee_exception_instance.Passport_issued_by = data.Passport_issued_by

        employee_exception_instance.Passport_issued_at = data.Passport_issued_at
        employee_exception_instance.Passport_issued_date = data.Passport_issued_date
        employee_exception_instance.Passport_issuing_authority = data.Passport_issuing_authority

        employee_exception_instance.Passport_valid_from = data.Passport_valid_from
        employee_exception_instance.Passport_valid_to = data.Passport_valid_to
        employee_exception_instance.Passport_verified_by = data.Passport_verified_by

        employee_exception_instance.Passport_verified_date = data.Passport_verified_date
        employee_exception_instance.passport_number = data.passport_number
        employee_exception_instance.passport_type = data.passport_type

        employee_exception_instance.country_of_issue = data.country_of_issue
        employee_exception_instance.place_of_issue = data.place_of_issue
        employee_exception_instance.number_of_accompanying_person = data.number_of_accompanying_person

        employee_exception_instance.previous_passport_number = data.previous_passport_number
        


        employee_exception_instance.save()

        return {
            "id": employee_exception_instance.id,
            "status": employee_exception_instance.status,
        }
    else:
        return JsonResponse({"error": "Invalid token"}, status=401)
    
    
#<---------------DOCUMENT LABOURCARD------------>

class DocumentLabourcardSchema(Schema):
    emp_id: str
    username: str
    department: str
    email: str
    group: str
    LabourCardcountry_name: str
    LabourCarddocument_type:str
    LabourCardcategory:str
    LabourCardsub_category:str
    LabourCarddocument_number: str
    LabourCardissued_by:str
    LabourCardissued_at:str
    LabourCardissued_date:str
    LabourCardissuing_authority: str
    LabourCardvalid_from:str
    LabourCardvalid_to:str
    LabourCardverified_by:str
    LabourCardverified_date: str

    aly_personal_id_number:str
    aly_work_permit_number:str
    aly_place_of_issue:str
     
@api.post("/post-document-labourcard")
def document_labourcard_application(request, data: DocumentLabourcardSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, proceed with creating the labour card
        document_labourcard_instance = DocumentForLabourCard.objects.create(
            user=user,
            emp_id=data.emp_id,
            username=data.username,
            department=data.department,
            email=data.email,
            group=data.group,
            LabourCardcountry_name=data.LabourCardcountry_name,
            LabourCarddocument_type=data.LabourCarddocument_type,
            LabourCardcategory=data.LabourCardcategory,
            LabourCardsub_category=data.LabourCardsub_category,
            LabourCarddocument_number=data.LabourCarddocument_number,
            LabourCardissued_by=data.LabourCardissued_by,
            LabourCardissued_at=data.LabourCardissued_at,
            LabourCardissued_date=data.LabourCardissued_date,
            LabourCardissuing_authority=data.LabourCardissuing_authority,
            LabourCardvalid_from=data.LabourCardvalid_from,
            LabourCardvalid_to=data.LabourCardvalid_to,
            LabourCardverified_by=data.LabourCardverified_by,
            LabourCardverified_date=data.LabourCardverified_date,

            aly_personal_id_number=data.aly_personal_id_number,
            aly_work_permit_number=data.aly_work_permit_number,
            aly_place_of_issue=data.aly_place_of_issue,
            
            
            documentForlabourcard_status="pending",
            documentForlabourcardApplied_date=timezone.now()

            # Set status to "pending" by default
        )
        return {
            "id": document_labourcard_instance.id,
            "documentForlabourcard_status": "pending",
        }
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)
    
@api.get("/labour-card-get")
def get_labour_card(request):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, retrieve all labour contracts associated with the user
        labour_card = DocumentForLabourCard.objects.filter(user=user)
        labour_data = []  # Initialize as a list
        for card in labour_card:
            labour_data.append({  # Append each labour card as a dictionary to the list
                "id": card.id,
                "emp_id": card.emp_id,
                "username": card.username,
                "department": card.department,
                "email": card.email,
                "group": card.group,
                "LabourCardcountry_name": card.LabourCardcountry_name,
                "LabourCarddocument_type": card.LabourCarddocument_type,
                "LabourCardcategory": card.LabourCardcategory,
                "LabourCardsub_category": card.LabourCardsub_category,
                "LabourCarddocument_number": card.LabourCarddocument_number,
                "LabourCardissued_by": card.LabourCardissued_by,
                "LabourCardissued_at": card.LabourCardissued_at,
                "LabourCardissued_date": card.LabourCardissued_date,
                "issuing_authority": card.LabourCardissuing_authority,
                "LabourCardvalid_from": card.LabourCardvalid_from,
                "LabourCardvalid_to": card.LabourCardvalid_to,
                "LabourCardverified_by": card.LabourCardverified_by,
                "LabourCardverified_date": card.LabourCardverified_date,
                "aly_personal_id_number": card.aly_personal_id_number,
                "aly_work_permit_number": card.aly_work_permit_number,
                "aly_place_of_issue": card.aly_place_of_issue,
                "documentForlabourcard_status": card.documentForlabourcard_status,
                "documentForlabourcardApplied_date": card.documentForlabourcardApplied_date.strftime('%d-%m-%Y')
            })
        return JsonResponse(labour_data, safe=False)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.get("/labour-card-get/{labour_card_id}")
def get_labour_card_by_id(request, labour_card_id):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, retrieve the labour card instance by ID
        try:
            labour_card_instance = DocumentForLabourCard.objects.get(id=labour_card_id, user=user)
            labour_card_data = {
                "id": labour_card_instance.id,
                "emp_id": labour_card_instance.emp_id,
                "username": labour_card_instance.username,
                "department": labour_card_instance.department,
                "email": labour_card_instance.email,
                "group": labour_card_instance.group,
                "LabourCardcountry_name": labour_card_instance.LabourCardcountry_name,
                "LabourCarddocument_type": labour_card_instance.LabourCarddocument_type,
                "LabourCardcategory": labour_card_instance.LabourCardcategory,
                "LabourCardsub_category": labour_card_instance.LabourCardsub_category,
                "LabourCarddocument_number": labour_card_instance.LabourCarddocument_number,
                "LabourCardissued_by": labour_card_instance.LabourCardissued_by,
                "LabourCardissued_at": labour_card_instance.LabourCardissued_at,
                "LabourCardissued_date": labour_card_instance.LabourCardissued_date,
                "LabourCardissuing_authority": labour_card_instance.LabourCardissuing_authority,
                "LabourCardvalid_from": labour_card_instance.LabourCardvalid_from,
                "LabourCardvalid_to": labour_card_instance.LabourCardvalid_to,
                "LabourCardverified_by": labour_card_instance.LabourCardverified_by,
                "LabourCardverified_date": labour_card_instance.LabourCardverified_date,
                "aly_personal_id_number": labour_card_instance.aly_personal_id_number,
                "aly_work_permit_number": labour_card_instance.aly_work_permit_number,
                "aly_place_of_issue": labour_card_instance.aly_place_of_issue,
                "documentForlabourcard_status": labour_card_instance.documentForlabourcard_status,
                "documentForlabourcardApplied_date": labour_card_instance.documentForlabourcardApplied_date.strftime('%d-%m-%Y')
            }
            return JsonResponse(labour_card_data)
        except DocumentForLabourCard.DoesNotExist:
            return JsonResponse({"error": "Labour card not found"}, status=404)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)
 
@api.put("/labour-card-update/{contract_id}")
def update_employee_exception(request, contract_id, data: DocumentLabourcardSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    user = token_bearer(request)

    if user:
        try:
            labour_contract_instance = DocumentForLabourCard.objects.get(id=contract_id)
        except DocumentForLabourCard.DoesNotExist:
            return JsonResponse({"error": "Labour card not found"}, status=404)

        if labour_contract_instance.user != user:
            return JsonResponse({"error": "Unauthorized access to update labour"}, status=403)

        
        labour_contract_instance.emp_id = data.emp_id
        labour_contract_instance.username = data.username
        labour_contract_instance.department = data.department
        labour_contract_instance.email = data.email
        labour_contract_instance.group = data.group

        labour_contract_instance.LabourCardcountry_name = data.LabourCardcountry_name
        labour_contract_instance.LabourCarddocument_type = data.LabourCarddocument_type
        labour_contract_instance.LabourCardcategory = data.LabourCardcategory

        labour_contract_instance.LabourCardsub_category = data.LabourCardsub_category
        labour_contract_instance.LabourCarddocument_number = data.LabourCarddocument_number
        labour_contract_instance.LabourCardissued_by = data.LabourCardissued_by

        labour_contract_instance.LabourCardissued_at = data.LabourCardissued_at
        labour_contract_instance.LabourCardissued_date = data.LabourCardissued_date
        labour_contract_instance.LabourCardissuing_authority = data.LabourCardissuing_authority

        labour_contract_instance.LabourCardvalid_from = data.LabourCardvalid_from
        labour_contract_instance.LabourCardvalid_to = data.LabourCardvalid_to
        labour_contract_instance.LabourCardverified_by = data.LabourCardverified_by
        labour_contract_instance.LabourCardverified_date = data.LabourCardverified_date

        labour_contract_instance.aly_personal_id_number = data.aly_personal_id_number
        labour_contract_instance.aly_work_permit_number = data.aly_work_permit_number
        labour_contract_instance.aly_place_of_issue = data.aly_place_of_issue


        labour_contract_instance.save()        

        return {
            "id": labour_contract_instance.id,
            "documentForlabourcard_status": labour_contract_instance.documentForlabourcard_status,
        }
    else:
        return JsonResponse({"error": "Invalid token"}, status=401)
        
@api.delete("/delete-document-labourcard/{card_id}")
def delete_document_labourcard(request, card_id):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        try:
            # Attempt to retrieve the labour card
            labour_card = DocumentForLabourCard.objects.get(id=card_id)

            # Check if the user has permission to delete this card
            if labour_card.user == user:
                # Delete the card
                labour_card.delete()
                return JsonResponse({"message": "Document Labour card deleted successfully"})
            else:
                # Return an error if the user does not have permission
                return JsonResponse({"error": "You do not have permission to delete this Labour card"}, status=403)
        except ObjectDoesNotExist:
            # Return an error if the card does not exist
            return JsonResponse({"error": "Labour card not found"}, status=404)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)
    
    
#<---------------Employee-Resumption------------>
    
class EmployeeResumptionSchema(Schema):
    username: str
    emp_id: str
    email: str
    group: str
    department: str
    enter_date: str
    other: str
    resumption_status: str  
    days_overstayed: str
    resumption_comment: str

@api.post("/Employee-Resumption")
def create_employee_resumption(request, data: EmployeeResumptionSchema):
    token = request.headers.get('Authorization')
    if not token:
        return JsonResponse({"error": "Authorization header missing"}, status=401)
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return JsonResponse({"error": "Invalid token"}, status=401)

    try:
        resumption_data = EmployeeResumption.objects.create(
            user=user,
            username=data.username,
            emp_id=data.emp_id,
            email=data.email,
            group=data.group,
            department=data.department,
            enter_date=data.enter_date,
            other=data.other,
            resumption_status=data.resumption_status,
            days_overstayed=data.days_overstayed,
            resumption_comment=data.resumption_comment,
            resumption_Status="pending",
            resumptionApplied_date=timezone.now(),
        )
        return JsonResponse({"id": resumption_data.id, "status": "pending"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@api.get("/employee_resumption")
def get_employee_resumption(request):
    try:
        # Extract the token from the Authorization header
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return JsonResponse({"error": "Authorization header is missing"}, status=401)

        # Split the Authorization header to extract the token
        token_parts = authorization_header.split()

        if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
            return JsonResponse({"error": "Invalid Authorization header format"}, status=401)

        # Extract the token
        token = token_parts[1]

        # Authenticate the user using the token
        auth = TokenAuthentication()
        user, _ = auth.authenticate_credentials(token)

        # Retrieve leave applications associated with the authenticated user
        user_employee_resumption = EmployeeResumption.objects.filter(user=user)

        # Serialize the leave applications data
        employee_resumption_data = []
        for application in user_employee_resumption:  # Fixed the iteration
            application_data = {
                "id": application.id,
                "username": application.user.username,
                "emp_id": application.user.emp_id,
                "email": application.email,  # Corrected the key name
                "department": application.department,
                "group":application.group,
                "enter_date": application.enter_date,
                "resumption_status": application.resumption_status,  # Changed key name to snake_case
                "other": application.other,
                "days_overstayed": application.days_overstayed,
                "resumption_comment": application.resumption_comment,
                "resumption_Status": application.resumption_Status,
                "resumptionApplied_date":application.resumptionApplied_date.strftime('%d-%m-%Y')
              
                
            }
            employee_resumption_data.append(application_data)

        # Return the leave applications data as JSON response
        return JsonResponse(employee_resumption_data, safe=False)

    except AuthenticationFailed:
        return JsonResponse({"error": "Authentication failed"}, status=401)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
   
class EmployeeResumptionGetSchema(Schema):
    id: int
    username: str
    emp_id: str
    email: str
    group: str
    department: str
    enter_date: str
    resumption_status: str
    other : str
    resumption_Status:str
    days_overstayed :int
    resumption_comment: str  

@api.get("/data-employee-resumption/{id}")
def get_employee_resumption(request, id: int):
    token = request.headers.get('Authorization')
    if not token:
        return JsonResponse({"error": "Authorization header missing"}, status=401)
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return JsonResponse({"error": "Invalid token"}, status=401)
    
    employee_resumption = get_object_or_404(EmployeeResumption, id=id)



    
    employee_resumption_schema = EmployeeResumptionGetSchema(
        id=employee_resumption.id,
        username=employee_resumption.username,
        emp_id=employee_resumption.emp_id,
        email=employee_resumption.email,
        group=employee_resumption.group,
        department=employee_resumption.department,
        enter_date=str(employee_resumption.enter_date),
        other=employee_resumption.other,
        resumption_status=employee_resumption.resumption_status,
        days_overstayed=employee_resumption.days_overstayed,
        resumption_comment=employee_resumption.resumption_comment,
        resumption_Status=employee_resumption.resumption_Status,
       
    )

    return JsonResponse(employee_resumption_schema.dict())

@api.put("/employee_resumption-update/{id}")
def update_employee_resumption(request, id, data: EmployeeResumptionSchema):
    # Extract token from Authorization header
    token = request.headers.get('Authorization')
    if not token:
        return 401, {"error": "Authorization header missing"}
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return 401, {"error": "Invalid token"}

    # Retrieve the medical reimbursement object
    try:
        resumption = EmployeeResumption.objects.get(id=id, user=user)
    except EmployeeResumption.DoesNotExist:
        return 404, {"error": "Employee resumption not found"}

    # Update the medical reimbursement object with the provided data
    resumption.username = data.username
    resumption.emp_id = data.emp_id
    resumption.email = data.email
    resumption.group = data.group
    resumption.department = data.department
    resumption.enter_date = data.enter_date
    resumption.resumption_status = data.resumption_status
    resumption.other = data.other
    resumption.days_overstayed = data.days_overstayed
    resumption.resumption_comment=data.resumption_comment
    resumption.save()

    return JsonResponse({"message": "Employee resumption updated successfully"})

@api.delete("/delete-employee_resumption/{id}")
def delete_employee_resumption(request, id):
    # Extract token from Authorization header
    token = request.headers.get('Authorization')
    if not token:
        return JsonResponse({"error": "Authorization header missing"}, status=401)
    
    try:
        token = token.split()[1]
        user = Token.objects.get(key=token).user
    except (Token.DoesNotExist, IndexError):
        return JsonResponse({"error": "Invalid token"}, status=401)

    # Retrieve the medical reimbursement object
    try:
        resumption = EmployeeResumption.objects.get(id=id, user=user)
        resumption.delete()
        return JsonResponse({"message": "Employee resumption deleted successfully"})
    except EmployeeReimbursement.DoesNotExist:
        return JsonResponse({"error": "Employee resumption not found"}, status=404)
    


#<---------------Employee-Travel------------>


class EmployeeTravelSchema(Schema):
    username: str
    emp_id: str
    email: str
    group: str
    department: str
    
    request_type: str
    purpose_of_visit: str
    travel_start_date: str
    travel_end_date: str
    country_of_travel: str
    
    entity_company_traveling_for: str
    advance_amount_required: str
    currency: str
    visa_to_be_processed: str
    book_hotel_accommodation: str
    
    flight_ticket_required: str
    visa_letter_required: str
    employeetravel_comments: str
    
   
@api.post("/employee-travel")
def create_employee_travel(request, travel: EmployeeTravelSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, proceed with creating the labour contract
        employee_travel_instance = EmployeeTravel.objects.create(
            user=user,
            username=travel.username,
            emp_id=travel.emp_id,
            email=travel.email,
            group=travel.group,
            department=travel.department,
            request_type=travel.request_type,
            purpose_of_visit=travel.purpose_of_visit,
            travel_start_date=travel.travel_start_date,
            travel_end_date=travel.travel_end_date,
            country_of_travel=travel.country_of_travel,
            entity_company_traveling_for=travel.entity_company_traveling_for,
            advance_amount_required=travel.advance_amount_required,
            currency=travel.currency,
            visa_to_be_processed=travel.visa_to_be_processed,
            book_hotel_accommodation=travel.book_hotel_accommodation,
            flight_ticket_required=travel.flight_ticket_required,
            visa_letter_required=travel.visa_letter_required,
            employeetravel_comments=travel.employeetravel_comments,
            employeetravel_status="pending",
            employeetravel_applied_date=timezone.now()
            # Set status to "pending" by default
        )
        return {
            "id": employee_travel_instance.id,
            "status": "pending",
        }
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)
    
@api.get("/employee-travel-get")
def get_labour_contracts(request):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, retrieve all labour contracts associated with the user
        employee_travels =  EmployeeTravel.objects.filter(user=user)
        travels_data = []
        for travel in  employee_travels:
            travel_data = {
            "id": travel.id,
            "username": travel.username,
            "emp_id": travel.emp_id,
            "email" :travel.email,
            "group":travel.group,
            "department":travel.department,
            "request_type":travel.request_type,
            "purpose_of_visit":travel.purpose_of_visit,
            "travel_start_date":travel.travel_start_date,
            "travel_end_date":travel.travel_end_date,
            "country_of_travel":travel.country_of_travel,
            "entity_company_traveling_for":travel.entity_company_traveling_for,
            "advance_amount_required":travel.advance_amount_required,
            "currency":travel.currency,
            "visa_to_be_processed":travel.visa_to_be_processed,
            "book_hotel_accommodation":travel.book_hotel_accommodation,
            "flight_ticket_required":travel.flight_ticket_required,
            "visa_letter_required":travel.visa_letter_required,
            "employeetravel_comments":travel.employeetravel_comments,
            "employeetravel_status":travel.employeetravel_status,
            "employeetravel_applied_date":travel.employeetravel_applied_date.strftime('%d-%m-%Y')
            }
            travels_data.append(travel_data)
        return JsonResponse(travels_data, safe=False)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)
    
@api.get("/travel-get/{travel_id}")
def get_employee_travel_id(request, travel_id):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, retrieve the labour card instance by ID
        try:
            employee_travel = EmployeeTravel.objects.get(id=travel_id, user=user)
            travel_data = {
            "id": employee_travel.id,
            "username": employee_travel.username,
            "emp_id": employee_travel.emp_id,
            "email" :employee_travel.email,
            "group":employee_travel.group,
            "department":employee_travel.department,
            "request_type":employee_travel.request_type,
            "purpose_of_visit":employee_travel.purpose_of_visit,
            "travel_start_date":employee_travel.travel_start_date,
            "travel_end_date":employee_travel.travel_end_date,
            "country_of_travel":employee_travel.country_of_travel,
            "entity_company_traveling_for":employee_travel.entity_company_traveling_for,
            "advance_amount_required":employee_travel.advance_amount_required,
            "currency":employee_travel.currency,
            "visa_to_be_processed":employee_travel.visa_to_be_processed,
            "book_hotel_accommodation":employee_travel.book_hotel_accommodation,
            "flight_ticket_required":employee_travel.flight_ticket_required,
            "visa_letter_required":employee_travel.visa_letter_required,
            "employeetravel_comments":employee_travel.employeetravel_comments,
            "employeetravel_status":employee_travel.employeetravel_status,
            "employeetravel_applied_date":employee_travel.employeetravel_applied_date.strftime('%d-%m-%Y')
            }
            return JsonResponse(travel_data)
        except EmployeeTravel.DoesNotExist:
            return JsonResponse({"error": "employee travel not found"}, status=404)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.delete("/delete-employee-travel/{travel_id}")
def delete_employee_travel(request, travel_id):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        try:
            # Attempt to retrieve the labour card
            employee_travel = EmployeeTravel.objects.get(id=travel_id)

            # Check if the user has permission to delete this card
            if employee_travel.user == user:
                # Delete the card
                employee_travel.delete()
                return JsonResponse({"message": "Employee Travel deleted successfully"})
            else:
                # Return an error if the user does not have permission
                return JsonResponse({"error": "You do not have permission to delete this Employee Travel"}, status=403)
        except ObjectDoesNotExist:
            # Return an error if the card does not exist
            return JsonResponse({"error": "Employee Travel not found"}, status=404)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)
    

@api.put("/update-employee-travel/{travel_id}")
def update_employee_travel(request, travel_id, data: EmployeeTravelSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    user = token_bearer(request)

    if user:
        try:
            employee_travel_instance = EmployeeTravel.objects.get(id=travel_id)
        except EmployeeTravel.DoesNotExist:
            return JsonResponse({"error": "Employee Travel not found"}, status=404)

        if employee_travel_instance.user != user:
            return JsonResponse({"error": "Unauthorized access to update Employee Travel"}, status=403)

        employee_travel_instance.emp_id = data.emp_id
        employee_travel_instance.username = data.username
        employee_travel_instance.department = data.department
        employee_travel_instance.email = data.email
        employee_travel_instance.group = data.group

        employee_travel_instance.request_type = data.request_type
        employee_travel_instance.purpose_of_visit = data.purpose_of_visit
        employee_travel_instance.travel_start_date = data.travel_start_date

        employee_travel_instance.travel_end_date = data.travel_end_date
        employee_travel_instance.country_of_travel = data.country_of_travel
        employee_travel_instance.entity_company_traveling_for = data.entity_company_traveling_for

        employee_travel_instance.advance_amount_required = data.advance_amount_required
        employee_travel_instance.currency = data.currency
        employee_travel_instance.visa_to_be_processed = data.visa_to_be_processed

        employee_travel_instance.book_hotel_accommodation = data.book_hotel_accommodation
        employee_travel_instance.flight_ticket_required = data.flight_ticket_required
        employee_travel_instance.visa_letter_required = data.visa_letter_required

        employee_travel_instance.employeetravel_comments = data.employeetravel_comments


        employee_travel_instance.save()

        return {
            "id": employee_travel_instance.id,
            "employeetravel_status": employee_travel_instance.employeetravel_status,
        }
    else:
        return JsonResponse({"error": "Invalid token"}, status=401)



#<---------------Bank-Accounts------------>

class BankAccountSchema(Schema):
    username: str
    emp_id: str
    email: str
    group: str
    department: str
    bank_name: str
    branch: str
    iban_number: str
    Bankstart_date: str
    bank_code: str
    bankaccount_comment: str   

@api.post("/bank-accounts")
def post_bank_account(request, account: BankAccountSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, proceed with creating the labour contract
        bank_account_instance = BankAccount.objects.create(
            user=user,
            username=account.username,
            emp_id=account.emp_id,
            email=account.email,
            group=account.group,
            department=account.department,
            bank_name=account.bank_name,
            branch=account.branch,
            iban_number=account.iban_number,
            Bankstart_date=account.Bankstart_date,
            bank_code=account.bank_code,
            bankaccount_comment=account.bankaccount_comment,
            bankaccount_status="pending",
            bankaccount_applied_date=timezone.now()
            

            # Set status to "pending" by default
        )
        return {
            "id": bank_account_instance.id,
            "status": "pending",
        }
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)
     
@api.get("/bank-accounts")
def get_bank_account(request):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, retrieve all document visa instances associated with the user
        bank_account_instances = BankAccount.objects.filter(user=user)
        account_data = []
        for bank in bank_account_instances:
            account_data.append({
                "id": bank.id,
                "username": bank.username,
                "emp_id": bank.emp_id,
                "email": bank.email,
                "group": bank.group,
                "department": bank.department,
                "bank_name": bank.bank_name,
                "branch": bank.branch,
                "iban_number": bank.iban_number,
                "Bankstart_date": bank.Bankstart_date,
                "bank_code": bank.bank_code,
                "bankaccount_comment": bank.bankaccount_comment,
                "bankaccount_status": bank.bankaccount_status,
                "bankaccount_applied_date": bank.bankaccount_applied_date.strftime('%d-%m-%Y')
            })
        return JsonResponse(account_data, safe=False)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.get("/bank-accounts/{bank_id}")
def get_bank_account_id(request, bank_id):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, retrieve the document visa instance by ID
        try:
            bank_instance = BankAccount.objects.get(id=bank_id, user=user)
            bank_data = {
                "id": bank_instance.id,
                "username": bank_instance.username,
                "emp_id": bank_instance.emp_id,
                "email": bank_instance.email,
                "group": bank_instance.group,
                "department": bank_instance.department,
                "bank_name": bank_instance.bank_name,
                "branch": bank_instance.branch,
                "iban_number": bank_instance.iban_number,
                "Bankstart_date": bank_instance.Bankstart_date,
                "bank_code": bank_instance.bank_code,
                "bankaccount_comment": bank_instance.bankaccount_comment,
                "bankaccount_status": bank_instance.bankaccount_status,
                "bankaccount_applied_date": bank_instance.bankaccount_applied_date.strftime('%d-%m-%Y')
            }
            return JsonResponse(bank_data)
        except DocumentForVisa.DoesNotExist:
            return JsonResponse({"error": "Bank account not found"}, status=404)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.delete("/bank-accounts/{bank_id}")
def delete_bank_account(request, bank_id):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        try:
            # Attempt to retrieve the labour contract
            bank_account_instance = BankAccount.objects.get(id=bank_id)

            # Check if the user has permission to delete this contract
            if bank_account_instance.user == user:
                # Delete the contract
                bank_account_instance.delete()
                return JsonResponse({"message": "Bank account deleted successfully"})
            else:
                # Return an error if the user does not have permission
                return JsonResponse({"error": "You do not have permission to delete this Bank account"}, status=403)
        except ObjectDoesNotExist:
            # Return an error if the contract does not exist
            return JsonResponse({"error": "Bank account not found"}, status=404)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.put("/bank-accounts/{bank_id}")
def update_bank_account(request, bank_id, data: BankAccountSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    user = token_bearer(request)

    if user:
        try:
            bank_account_instance = BankAccount.objects.get(id=bank_id)
        except BankAccount.DoesNotExist:
            return JsonResponse({"error": "Bank account not found"}, status=404)

        if bank_account_instance.user != user:
            return JsonResponse({"error": "Unauthorized access to update Bank account"}, status=403)

        bank_account_instance.username = data.username
        bank_account_instance.emp_id = data.emp_id
        bank_account_instance.email = data.email
        bank_account_instance.group = data.group
        bank_account_instance.department = data.department

        bank_account_instance.bank_name = data.bank_name
        bank_account_instance.branch = data.branch
        bank_account_instance.iban_number = data.iban_number

        bank_account_instance.Bankstart_date = data.Bankstart_date
        bank_account_instance.bank_code = data.bank_code
        bank_account_instance.bankaccount_comment = data.bankaccount_comment

        

        bank_account_instance.save()

        return {
            "id": bank_account_instance.id,
            "bankaccount_status": bank_account_instance.bankaccount_status,
        }
    else:
        return JsonResponse({"error": "Invalid token"}, status=401)
    
#<-------------visitingCardSchema------------>    
    
class visitingCardSchema(BaseModel):
    username: str
    email:str
    designation:str
    mobilenum:str
    poBox:str
    unitedstate:str
    Visitingcountry:str
    telphone:str
    extnum:str
    faxnum:str

@api.post("/visiting-card-post")
def visiting_card_post(request, data:visitingCardSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        # If user is authenticated, proceed with creating the labour contract
        visiting_card_instance = visitingCard.objects.create(
            user = user,
            username = data.username,
            email = data.email,
            designation= data.designation,
            mobilenum = data.mobilenum,
            poBox = data.poBox,
            Visitingcountry= data.Visitingcountry,
            unitedstate = data.unitedstate,
            telphone = data.telphone,
            extnum = data.extnum,
            faxnum = data.faxnum,

            # Set status to "pending" by default
        )
        return {
            "id": visiting_card_instance.id,
            
        }
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.get("/visiting-card-get/{visitingId}")
def visiting_card_get(request , visitingId:int):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        try:
            # If user is authenticated, retrieve the specific visiting card by user
            visiting_card_instance = visitingCard.objects.get(id = visitingId ,user=user)
            visiting_card_data = {
                "id": visiting_card_instance.id,
                "username": visiting_card_instance.username,
                "email": visiting_card_instance.email,
                "designation": visiting_card_instance.designation,
                "mobilenum": visiting_card_instance.mobilenum,
                "poBox": visiting_card_instance.poBox,
                "Visitingcountry": visiting_card_instance.Visitingcountry,
                "unitedstate": visiting_card_instance.unitedstate,
                "telphone": visiting_card_instance.telphone,
                "extnum": visiting_card_instance.extnum,
                "faxnum": visiting_card_instance.faxnum,
            }
            return JsonResponse(visiting_card_data)
        except visitingCard.DoesNotExist:
            return JsonResponse({"error": "Visiting card not found for this user"}, status=404)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.get("/visiting-card-get")
def visiting_card_get(request):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                # Assuming token is associated with a user in your database.
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    # Perform token-based authentication
    user = token_bearer(request)

    if user:
        try:
            # If user is authenticated, retrieve the specific visiting card by user
            visiting_card_instance = visitingCard.objects.get(user=user)
            visiting_card_data = {
                "id": visiting_card_instance.id,
                "username": visiting_card_instance.username,
                "email": visiting_card_instance.email,
                "designation": visiting_card_instance.designation,
                "mobilenum": visiting_card_instance.mobilenum,
                "poBox": visiting_card_instance.poBox,
                "Visitingcountry": visiting_card_instance.Visitingcountry,
                "unitedstate": visiting_card_instance.unitedstate,
                "telphone": visiting_card_instance.telphone,
                "extnum": visiting_card_instance.extnum,
                "faxnum": visiting_card_instance.faxnum,
            }
            return JsonResponse(visiting_card_data)
        except visitingCard.DoesNotExist:
            return JsonResponse({"error": "Visiting card not found for this user"}, status=404)
    else:
        # If authentication fails, return an error response
        return JsonResponse({"error": "Invalid token"}, status=401)

@api.put("/visiting-card-update/{visiting_id}")
def update_visiting_card(request, visiting_id, data: visitingCardSchema):
    class TokenBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                user = CustomUser.objects.get(auth_token=token)
                return user
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Invalid token")

    token_bearer = TokenBearer()

    user = token_bearer(request)

    if user:
        try:
            visiting_card_instance = visitingCard.objects.get(id=visiting_id)
        except visitingCard.DoesNotExist:
            return JsonResponse({"error": "Visiting card not found"}, status=404)

        if visiting_card_instance.user != user:
            return JsonResponse({"error": "Unauthorized access to update visiting card"}, status=403)

        visiting_card_instance.username = data.username
        visiting_card_instance.designation = data.designation
        visiting_card_instance.email = data.email
        visiting_card_instance.mobilenum = data.mobilenum
        visiting_card_instance.poBox = data.poBox
        visiting_card_instance.Visitingcountry = data.Visitingcountry
        visiting_card_instance.unitedstate = data.unitedstate
        visiting_card_instance.telphone = data.telphone
        visiting_card_instance.extnum = data.extnum
        visiting_card_instance.faxnum = data.faxnum
        visiting_card_instance.save()

        return {
            "id": visiting_card_instance.id,
            
        }
    else:
        return JsonResponse({"error": "Invalid token"}, status=401)


#<-------------send_otp_email------------>

@api.post("/send_otp_email")
def send_otp_email(request, notification: EmailOTPSchema):
    subject = notification.subject
    recipient_email = notification.recipients
    message = notification.message

    # Generate OTP (e.g., a random 6-digit number)
    otp = ''.join(random.choices('0123456789', k=6))

    # Update the user's OTP field in the database
    try:
        user = CustomUser.objects.get(email=recipient_email)
        user.otp = otp  # Save the generated OTP
        user.save()
    except CustomUser.DoesNotExist:
        # Handle the case where the user does not exist
        return {"message": "CustomUser not found"}

    # Send OTP email
    send_mail(subject, f'{message} Your OTP is {otp}', settings.DEFAULT_FROM_EMAIL, [recipient_email])

    return {"message": "OTP email sent successfully"}

from ninja import NinjaAPI, Schema

from typing import Any
from .models import CustomUser  # Import your CustomUser model

# Define the schema
class OTPValidationSchema(Schema):
    email: str
    otp: str

@api.post("/validate_otp")
def validate_otp(request: Any, payload: OTPValidationSchema):
    try:
        print(f"Received payload: {payload.dict()}")  # Debug print
        user = CustomUser.objects.get(email=payload.email)
        
        # Check if the provided OTP matches the one stored in the user's record
        if user.otp == payload.otp:
            # Clear the OTP field in the user's record
            user.otp = None
            user.save()
            return JsonResponse({"message": "OTP validated successfully"}, status=200)
        else:
            return JsonResponse({"error": "Invalid OTP"}, status=400)
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "CustomUser not found"}, status=404)
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print
        return JsonResponse({"error": "Internal server error"}, status=500)



#<-------------update-password------------>
class PasswordUpdateSchema(Schema):
    email: str
    new_password: str

@api.post("/update-password")
def update_password(request, data: PasswordUpdateSchema):
    try:
        # Find the user by email
        user = CustomUser.objects.get(email=data.email)

        new_password = data.new_password

        # Update the password
        user.password = make_password(new_password)
        user.save()

        return JsonResponse({"message": "Password updated successfully"}, status=200)

    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "CustomUser not found"}, status=404)
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print
        return JsonResponse({"error": "Internal server error"}, status=500)

@api.get("/public_user_details")
def get_public_user_details(request, username: str):
    try:
        user = get_object_or_404(CustomUser, username=username)
        
        email = user.email
        phone_number = user.phone_number
        whatsapp_number = user.whats_up_number

        return JsonResponse({
            "email": email,
            "phone_number": phone_number,
            "whatsapp_number": whatsapp_number,
        }, status=200)
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "CustomUser not found"}, status=404)


#<-------------send_otp_sms----------->
def generate_otp():
    return str(random.randint(100000, 999999))
@api.post("/send_otp_sms")
def send_otp_sms(request):
    try:
        data = json.loads(request.body)
        phone_number = data.get('phone_number', None)
        if phone_number is None:
            return JsonResponse({'success': False, 'error': 'Phone number is required'}, status=400)

        otp = generate_otp()
        message = f"Your OTP is: {otp}"

        # Use Textbelt API to send SMS
        response = requests.post('https://textbelt.com/text', {
            'phone': phone_number,
            'message': message,
            'key': 'textbelt',
        })

        result = response.json()
        if result['success']:
            return JsonResponse({'success': True, 'otp': otp})
        else:
            return JsonResponse({'success': False, 'error': result['error']})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data in request body'}, status=400)


#<-------------update-password----------->
class UpdatePasswordSchema(BaseModel):
    old_password: str
    new_password: str

@api.put("/update-password")
def update_password(request, data: UpdatePasswordSchema):
    token = request.headers.get('Authorization')
    if not token:
        return JsonResponse({"error": "Token not provided"}, status=401)

    try:
        token_obj = Token.objects.get(key=token.split()[1])
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=401)

    try:
        user = CustomUser.objects.get(auth_token=token_obj)
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "CustomUser not found"}, status=404)

    if not user.check_password(data.old_password):
        return JsonResponse({"error": "Invalid old password"}, status=400)

    user.set_password(data.new_password)
    user.save()
    update_session_auth_hash(request, user)

    return JsonResponse({"message": "Password updated successfully"})




from django.conf import settings
import os
import vobject

class VCardSchema(Schema):
    username: str
    contact: str
    email: str

@api.post("/generate-vcard")
def generate_vcard(request, payload: VCardSchema):
    try:
        stored_upload_dir = os.path.join(settings.MEDIA_ROOT, 'stored_upload')
        if not os.path.exists(stored_upload_dir):
            os.makedirs(stored_upload_dir)

        file_path = os.path.join(stored_upload_dir, f"{payload.username}.vcf")

        vcard = vobject.vCard()
        vcard.add('fn').value = payload.username
        vcard.add('email').value = payload.email
        vcard.add('tel').value = payload.contact
        vcard.tel.type_param = 'CELL'

        with open(file_path, 'w') as vcard_file:
            vcard_file.write(vcard.serialize())

        return JsonResponse({
            'message': 'vCard generated successfully',
            'file_path': file_path,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    
    
from django.http import FileResponse, Http404  

  

@api.get("/vcf/{filename}", by_alias=False, response=None)

# def get_vcf_file(request, filename: str):
#     file_path = os.path.join('media', 'stored_upload', filename)
#     logging.info(f"Attempting to serve file from: {file_path}")
    
#     if os.path.exists(file_path):
#         logging.info(f"File found: {file_path}")
#         try:
#             with open(file_path, 'rb') as file:
#                 file_content = file.read()
#                 logging.info(f"File size: {len(file_content)} bytes")
#                 response = HttpResponse(file_content, content_type='text/vcard')
#                 response['Content-Disposition'] = f'attachment; filename="{filename}"'
#                 return response
#         except Exception as e:
#             logging.error(f"Error reading file: {e}")
#             raise Http404('Error reading file')
#     else:
#         logging.error(f"File not found: {file_path}")
#         raise Http404('File not found')



def get_vcf_file(request, filename: str):
    file_path = os.path.join('media', 'stored_upload', filename)
    logging.info(f"Attempting to serve file from: {file_path}")

    if os.path.exists(file_path):
        logging.info(f"File found: {file_path}")
        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()
                logging.info(f"File size: {len(file_content)} bytes")
                response = HttpResponse(file_content, content_type='text/vcard')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
        except Exception as e:
            logging.error(f"Error reading file: {e}")
            raise Http404('Error reading file')
    else:
        logging.error(f"File not found: {file_path}")
        raise Http404('File not found')