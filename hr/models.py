# from datetime import timedelta, timezone
# import datetime
# from enum import Enum
# from django.db import models

# from django.utils import timezone
# from django.contrib.auth.models import User


# from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from enum import Enum
# from django.apps import AppConfig, apps

# class CustomUser(AbstractUser):
#     department = models.CharField(max_length=100, blank=True, null=True)
#     emp_id = models.CharField(max_length=200)
#     phone_number = models.CharField(max_length=200, blank=True, null=True)
#     designation = models.CharField(max_length=200, blank=True, null=True)
#     group = models.CharField(max_length=200, blank=True, null=True)
#     address = models.CharField(max_length=500, blank=True, null=True)
#     country = models.CharField(max_length=100, blank=True, null=True)
#     state = models.CharField(max_length=200, blank=True, null=True)
#     whats_up_number = models.CharField(max_length=200, blank=True, null=True)
#     date_of_birth = models.DateField(blank=True, null=True)
#     date_joined = models.DateField(blank=True, null=True)
#     otp = models.CharField(max_length=6, null=True, blank=True)

#     def __str__(self):
#         return self.username


# class MasterTable(models.Model):
#     CLAIM_TYPES = [
#         ('Normal', 'Normal Medical Fees'),
#         ('Urgent', 'Urgent Medical Fees'),
#     ]

#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]

#     department = models.CharField(max_length=100, blank=True, null=True)
#     emp_id = models.CharField(max_length=200)
    
#     phone_number = models.CharField(max_length=200, blank=True, null=True)
#     designation = models.CharField(max_length=200, blank=True, null=True)
#     group = models.CharField(max_length=200, blank=True, null=True)
#     address = models.CharField(max_length=500, blank=True, null=True)
#     country = models.CharField(max_length=100, blank=True, null=True)
#     state = models.CharField(max_length=200, blank=True, null=True)
#     whats_up_number = models.CharField(max_length=200, blank=True, null=True)
#     date_of_birth = models.DateField(blank=True, null=True)
#     date_joined = models.DateField(blank=True, null=True)
#     otp = models.CharField(max_length=6, null=True, blank=True)

#     username = models.CharField(max_length=150)
#     password = models.CharField(max_length=128, blank=True, null=True)
#     first_name = models.CharField(max_length=150, blank=True)
#     last_name = models.CharField(max_length=150, blank=True)
#     email = models.EmailField(blank=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#     last_login = models.DateTimeField(blank=True, null=True)
#     reason = models.CharField(max_length=255, choices=CLAIM_TYPES, blank=True, null=True)
#     type_of_claim = models.CharField(max_length=255, blank=True, null=True)
#     amount_aed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     comments = models.TextField(blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
#     leave_balance = models.IntegerField(default=100)
#     duration = models.IntegerField(default=0,null=True,blank=True)
#     applied_date = models.DateField(auto_now_add=True, blank=True, null=True)
#     start_date = models.DateField(blank=True, null=True)
#     end_date = models.DateField(blank=True, null=True)
#     replaced_by = models.CharField(max_length=200, blank=True, null=True)
#     leave_reason = models.CharField(max_length=50,default=True,null=True, choices=[
#         ("1 Hour Exam Paper","1 Hour Exam Paper"),
#         ("2 Hour Exam Paper","2 Hour Exam Paper"),
#         ("3 Hour Exam Paper","3 Hour Exam Paper"),
#         ("Accident","Accident"),
#         ("Accomodation Shifting","Accomodation Shifting"),
#         ("Annual Leave Extension","Annual Leave Extension"),
#         ("Annual Vacation","Annual Vacation"),
#         ("Funeral","Funeral"),
#         ("Hajj","Hajj"),
#         ("Hospitalized","Hospitalized"),
#         ("Others","Others"),
#         ("Rest / Break","Rest / Break"),
#         ("Umrah","Umrah"),
#         ("Work Stress","Work Stress"),

#     ])
    
#     leave_type = models.CharField(max_length=50,  blank=True, null=True,choices=[
#         ("Annual Leave", "Annual Leave"),
#         ("Sick Leave", "Sick Leave"),
#         ("Maternity Leave", "Maternity Leave"),
#         ("Personal Leave", "Personal Leave"),
        
#         ("UnPaid Leave", "UnPaid Leave"),
#     ])
#     category = models.CharField(max_length=50, null=True,choices=[
     
#         ("Vacation", "Vacation"),
#         ("Maternity", "Maternity"),
#         ("Unpaid", "Unpaid"),
#         ("Personal", "Personal"),
#         ("Sickness", "Sickness"),
#     ])

#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]
   
    
#     passport_withdrawal_date = models.DateField(null=True, blank=True)
#     request_for_airticket = models.CharField(max_length=50, choices=[
#         ("Book Airticket","Book Airticket"),
#         ("Not Aplicable","Not Aplicable"),
#         ("Reimburse Airticket","Reimburse Airticket",)
#         ], null=True, blank=True)

#     def __str__(self):
#         return f"MasterTable Entry: {self.emp_id}"


# class Leaves(models.Model):
   
    
#     user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
#     master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
#     employee_name = models.CharField(max_length=255)
#     emp_id = models.CharField(max_length=100)
#     email = models.EmailField()
#     department = models.CharField(max_length=255)
#     business_group = models.CharField(max_length=255)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     replaced_by=models.CharField(max_length=200,blank=True,null=True)
#     leave_reason = models.CharField(max_length=50,default=True,null=True, choices=[
#         ("1 Hour Exam Paper","1 Hour Exam Paper"),
#         ("2 Hour Exam Paper","2 Hour Exam Paper"),
#         ("3 Hour Exam Paper","3 Hour Exam Paper"),
#         ("Accident","Accident"),
#         ("Accomodation Shifting","Accomodation Shifting"),
#         ("Annual Leave Extension","Annual Leave Extension"),
#         ("Annual Vacation","Annual Vacation"),
#         ("Funeral","Funeral"),
#         ("Hajj","Hajj"),
#         ("Hospitalized","Hospitalized"),
#         ("Others","Others"),
#         ("Rest / Break","Rest / Break"),
#         ("Umrah","Umrah"),
#         ("Work Stress","Work Stress"),

#     ])
    
#     leave_type = models.CharField(max_length=50, choices=[
#         ("Annual Leave", "Annual Leave"),
#         ("Sick Leave", "Sick Leave"),
#         ("Maternity Leave", "Maternity Leave"),
#         ("Personal Leave", "Personal Leave"),
        
#         ("UnPaid Leave", "UnPaid Leave"),
#     ])
#     category = models.CharField(max_length=50, choices=[
     
#         ("Vacation", "Vacation"),
#         ("Maternity", "Maternity"),
#         ("Unpaid", "Unpaid"),
#         ("Personal", "Personal"),
#         ("Sickness", "Sickness"),
#     ])

#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]
#     passport_withdrawal_date = models.DateField(null=True, blank=True)
#     request_for_airticket = models.CharField(max_length=50, choices=[
#         ("Book Airticket","Book Airticket"),
#         ("Not Aplicable","Not Aplicable"),
#         ("Reimburse Airticket","Reimburse Airticket",)
#         ], null=True, blank=True)
#     comments = models.TextField(blank=True)
  

#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
#     leave_balance = models.IntegerField(default=100)  # Total leaves per year
#     duration = models.IntegerField(default=0,null=True,blank=True)
#     applied_date = models.DateField(auto_now_add=True, blank=True, null=True)

#     def save(self, *args, **kwargs):
#         if self.pk is None:
#             # This is a new leave application, fetch previous remaining leaves
#             previous_leave = Leaves.objects.filter(
#                 emp_id=self.emp_id,
#                 status='approved'
#             ).order_by('-end_date').first()

#             if previous_leave:
#                 self.leave_balance = previous_leave.leave_balance

#         if self.status == 'approved':
#             # Calculate the duration of the leave application
#             self.duration = (self.end_date - self.start_date).days + 1

#             # Check if the user has previously applied for the same leave type
#             previous_leave = Leaves.objects.filter(
#                 emp_id=self.emp_id,
#                 leave_type=self.leave_type,
#                 status='approved'
#             ).exclude(pk=self.pk).order_by('-end_date').first()

#             if previous_leave:
#                 # Deduct duration from remaining leaves based on the previous count
#                 self.leave_balance = previous_leave.leave_balance - self.duration
#             else:
#                 # Deduct duration from default remaining leaves
#                 self.leave_balance -= self.duration

#             # Update leave balance based on the number of times leave has been applied
#             previous_leaves_count = Leaves.objects.filter(
#                 emp_id=self.emp_id,
#                 status='approved',
#                 leave_type=self.leave_type,
#                 start_date__lte=self.start_date,
#                 end_date__gte=self.end_date
#             ).exclude(pk=self.pk).count()

#             # Update leave balance based on the number of times leave has been applied
#             self.leave_balance -= previous_leaves_count

#         super().save(*args, **kwargs)

#     def str(self):
#         return f"{self.employee_name} - {self.start_date} to {self.end_date}"
    
    










# class visitingCard(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
#     username = models.CharField(max_length=100, default=True, blank=True, null=True)
#     mobilenum = models.CharField(max_length=50, default=True, blank=True, null=True)
#     email = models.EmailField(default=True, blank=True, null=True)
#     poBox = models.CharField(max_length=100, default=True, blank=True, null=True)
#     unitedstate = models.CharField(max_length=100, default=True, blank=True, null=True)
#     designation = models.CharField(max_length=100, default=True, blank=True, null=True)
#     country = models.CharField(max_length=100, default=True, blank=True, null=True)
#     telphone = models.CharField(max_length=100, default=True, blank=True, null=True)
#     extnum = models.CharField(max_length=100, default=True, blank=True, null=True)
#     faxnum = models.CharField(max_length=100, default=True, blank=True, null=True)

#     def __str__(self):
#         return f"{self.username}'s visiting card"

# class AttendanceStatus(Enum):
#     CHECKIN = "Check-in"
#     MISSPUNCH = "Miss-punch"
#     CHECKOUT = "Check-out"

# class userAttendance(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     check_in = models.DateTimeField(null=True, blank=True)
#     check_out = models.DateTimeField(null=True, blank=True)
#     username = models.CharField(max_length=200, null=True, blank=True)
#     chk_date = models.DateField(null=True, blank=True)
#     status = models.CharField(max_length=50, null=True, blank=True)
#     total_hours = models.CharField(max_length=50, blank=True, null=True, default='')
#     working_hours = models.CharField(max_length=50, blank=True, null=True, default='')

#     def save(self, *args, **kwargs):
#         if self.check_in and self.check_out:
#             self.status = AttendanceStatus.CHECKOUT.value
#         super().save(*args, **kwargs)

#     class Meta:
#         verbose_name = "User Daily Attendance"
#         verbose_name_plural = "User Daily Attendance"

# class DaywiseStatus(Enum):
#     PENDING = "Pending"
#     PRESENT = "Present"
#     ABSENT = "Absent"

# class daywiseAttendance(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     check_in = models.DateTimeField(null=True, blank=True)
#     check_out = models.DateTimeField(null=True, blank=True)
#     status = models.CharField(max_length=50, null=True, blank=True)
#     username = models.CharField(max_length=200, blank=True)
#     timeShortageExceed = models.CharField(max_length=200, blank=True)
#     total_hours = models.CharField(max_length=50, blank=True, null=True, default='')
#     chk_date = models.DateField(null=True, blank=True)

#     def update_status(self):
#         if self.check_in:
#             self.status = DaywiseStatus.PRESENT.value
#         else:
#             self.status = DaywiseStatus.ABSENT.value
#         super().save()

#     class Meta:
#         verbose_name = "Daywise Attendance"
#         verbose_name_plural = "Daywise Attendance"







# class Log(models.Model):
#     Profile=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     photo=models.ImageField(upload_to="logs")
#     is_correct=models.BooleanField(default=False)
    
#     def __str__(self):
#         return f"Log of {self.profile.id}"
    
    
# class DetectedFaces(models.Model):
#     # user = models.ForeignKey(User, on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser, related_name='detected_faces', on_delete=models.CASCADE)
    
#     image = models.ImageField(upload_to='profile_images/')
#     x = models.IntegerField(default=0)
#     y = models.IntegerField(default=0)
#     width = models.IntegerField(default=0)
#     height = models.IntegerField(default=0)
    
#     features = models.BinaryField(null=True,blank=True)  # Field to store facial features as binary data

#     def save_features(self, features):
#         self.features = features
#         self.save()
        
#     class Meta:
#         verbose_name = "Detected Faces"
#         verbose_name_plural = "Detected Faces"
        
# class EmployeeList(models.Model):
#     name = models.CharField(max_length=200)
#     email_address = models.EmailField()
#     customer_status = (('active', 'active',),('inactive','inactive'))
#     status = models.CharField(max_length=50,choices=customer_status,default='active')
    
#     def __str__(self):
#         return self.name
    
#     class Meta:
#         verbose_name = "Employee List"
#         verbose_name_plural = "Employee List"



# class EmailLog(models.Model):
#     subject = models.CharField(max_length=255)
#     sent_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.subject


# class LeaveApplication(models.Model):
#     LEAVE_TYPES = (
#         ('casual', 'Casual Leave'),
#         ('sick', 'Sick Leave'),
#         ('excuse', 'Excuse Leave'),
#     )
#     STATUS_CHOICES = (
#         ('Pending', 'Pending'),
#         ('Approved', 'Approved'),
#         ('Rejected', 'Rejected'),
#     )
#     username = models.CharField(max_length=100,blank=True,null=True)
#     email = models.EmailField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     reason = models.TextField()
#     leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES, null=True, blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
#     created_at = models.DateTimeField(default=timezone.now)

#     def _str_(self):
#         return f"{self.username}'s {self.get_leave_type_display()} Application ({self.status})"


# class MedicalReimbursement(models.Model):
#     CLAIM_TYPES = [
#         ('Normal', 'Normal Medical Fees'),
#         ('Urgent', 'Urgent Medical Fees'),
#     ]

#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]

#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     employee_name = models.CharField(max_length=255, verbose_name='Employee Name')
#     employee_id = models.CharField(max_length=10, verbose_name='Employee Id')
#     email = models.EmailField(verbose_name='Email Address')
#     business_group = models.CharField(max_length=255, verbose_name='Business Group')
#     department = models.CharField(max_length=255, verbose_name='Department')
#     reason = models.CharField(max_length=255, verbose_name='Reason', choices=CLAIM_TYPES)
#     type_of_claim = models.CharField(max_length=255, verbose_name='Type of Medical Claim')
#     amount_aed = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount (AED)')
#     comments = models.TextField(blank=True, verbose_name='Comments')
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
#     date = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Date')

#     attachments = models.ManyToManyField('Attachment', related_name='medical_reimbursements', blank=True, verbose_name='Attachments')

#     def _str_(self):
#         return f"Medical Reimbursement Request - {self.reason} - {self.employee_name}"

# class Attachment(models.Model):
#     file = models.FileField(upload_to='medical_reimbursement_attachments/')


   
# class LabourContract(models.Model):
#     PENDING = 'Pending'
#     CONFIRMED = 'Confirmed'
    
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]
    
    
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     emp_id = models.CharField(max_length=200, blank=True, null=True)
#     username = models.CharField(max_length=200,blank=True, null=True)
#     department = models.CharField(max_length=100,blank=True, null=True)
#     email = models.EmailField(max_length=100, blank=True, null=True)
#     group = models.CharField(max_length=100, blank=True, null=True)
#     reason = models.CharField(max_length=100, blank=True, null=True,choices=[
#         ("Name Change","Name Change"),
#         ("Position Change","Position Change"),
#         ("Position and Salary Change","Position and Salary Change"),
        
#         ("Salary Change","Salary Change")
#         ],)
#     amendment_date = models.DateField(blank=True, null=True)
#     comments = models.CharField(max_length=500, blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True)
#     Applied_on=models.DateTimeField(auto_now_add=True,blank=True,null=True)

#     def _str_(self):
#         return f"{self.user.username}'s LabourContract"
    
    
# class EmployeeReimbursement(models.Model):
#     user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
#     employee_name = models.CharField(max_length=200)
#     employee_id = models.CharField(max_length=200)
#     email = models.EmailField(max_length=100)
#     group = models.CharField(max_length=100)
#     department = models.CharField(max_length=100)
    
#     enter_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     note=models.CharField(max_length=300,blank=True,null=True,choices=[("Supporting bills should be scanned and attached in request form, originals should be submitted in HRD.Any claims without receipts will not be paid","Supporting bills should be scanned and attached in request form, originals should be submitted in HRD.Any claims without receipts will not be paid")])
#     Comment = models.CharField(max_length=100,blank=True,null=True)
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]
    
#     REIMBURSEMENT_CHOICES = [
#         ('Air Passage Recruitment', 'Air Passage Recruitment'),
#         ('Airticket Reimbursement', 'Airticket Reimbursement'),
#         ('Examination Reimbursement', 'Examination Reimbursement'),
#         ('Food Reimbursement', 'Food Reimbursement'),
#         ('Insurance Claim', 'Insurance Claim'),
#         ('Medical Fee Recruitment', 'Medical Fee Recruitment'),
#         ('Parking Fees', 'Parking Fees'),
#         ('Petrol Charges', 'Petrol Charges'),
#         ('Postal Charges', 'Postal Charges'),
#         ('Salik Fee', 'Salik Fee'),
#         ('School Fees', 'School Fees'),
#         ('Telephone Bill Claim', 'Telephone Bill Claim'),
#         ('Transportation Fee', 'Transportation Fee'),
#         ('Vehicle Repair Charges', 'Vehicle Repair Charges'),
#         ('Vehicle related reimbursement', 'Vehicle related reimbursement'),
#     ]

#     reimbursement_type = models.CharField(max_length=300,choices=REIMBURSEMENT_CHOICES)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True)
#     applied_date = models.DateField(auto_now_add=True,blank=True,null=True)

#     def __str__(self):
#         return f"{self.employee_name} - {self.reimbursement_type} - {self.employee_id}"


# class BusinessTrip(models.Model):

#     PENDING = 'Pending'
#     CONFIRMED = 'Confirmed'
    
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]
#     NAME_CHOICES = [
#         ('Abdul Wahed Asad Hassan Abdulla', 'Abdul Wahed Asad Hassan Abdulla'),
#         ('Abid Moosa Ali', 'Abid Moosa Ali'),
#         ('Adham Fuddah Hakam Hakam', 'Adham Fuddah Hakam Hakam'),
#         ('Ahammed Noufal Muhammed Kunhi', 'Ahammed Noufal Muhammed Kunhi'),
#         ('Anil Kumar Paliekkara', 'Anil Kumar Paliekkara'),
#         ('Diaa Aldeen Kamel Mohd Sadaqa', 'Diaa Aldeen Kamel Mohd Sadaqa'),
#         ('Dileep Purushothaman Sri Kala Purushothaman', 'Dileep Purushothaman Sri Kala Purushothaman'),
#         ('Elshafie Abdelbaset Abdelsalam Mohamed Youssef', 'Elshafie Abdelbaset Abdelsalam Mohamed Youssef'),
#         ('Hardip Singh Gurnam Singh', 'Hardip Singh Gurnam Singh'),
#         ('Hasen Mohamed Samsudeen', 'Hasen Mohamed Samsudeen'),
#         ('Isarafil Nadaf', 'Isarafil Nadaf'),
#         ('Jabir Ali', 'Jabir Ali'),
#         ('Jashim Uddin', 'Jashim Uddin'),
#         ('Mohammad Shakeer Noor Nayak Mohammad Haneef Noor Nayak', 'Mohammad Shakeer Noor Nayak Mohammad Haneef Noor Nayak'),
#         ('Sandhya Akella Akella Somappa Somayajulu', 'Sandhya Akella Akella Somappa Somayajulu'),
#         ('Sumitra Adhikari Ghimire', 'Sumitra Adhikari Ghimire'),
#         ('Syed Ali Abbas Rizvi Syed Nusrat Ali Rizvi', 'Syed Ali Abbas Rizvi Syed Nusrat Ali Rizvi'),
#     ]
    
#     COUNTRY_CHOICES = [
#         ('Afghanistan', 'Afghanistan'),
#         ('Algeria', 'Algeria'),
#         ('Bahrain', 'Bahrain'),
#         ('Bangladesh', 'Bangladesh'),
#         ('Bhutan', 'Bhutan'),
#         ('Burma Union Myanmar', 'Burma Union Myanmar'),
#         ('China', 'China'),
#         ('Djibouti', 'Djibouti'),
#         ('Egypt', 'Egypt'),
#         ('Hong Kong', 'Hong Kong'),
#         ('India', 'India'),
#         ('Indonesia', 'Indonesia'),
#         ('Iran', 'Iran'),
#         ('Iraq', 'Iraq'),
#         ('Japan', 'Japan'),
#         ('Jordan', 'Jordan'),
#         ('Kampuchea', 'Kampuchea'),
#         ('Kuwait', 'Kuwait'),
#         ('Lebanon', 'Lebanon'),
#         ('Libya', 'Libya'),
#         ('Malaysia', 'Malaysia'),
#         ('Mauritania', 'Mauritania'),
#         ('Morocco', 'Morocco'),
#         ('Nepal', 'Nepal'),
#         ('North Korea', 'North Korea'),
#         ('Pakistan', 'Pakistan'),
#         ('Palestine', 'Palestine'),
#         ('Philippines', 'Philippines'),
#         ('Qatar', 'Qatar'),
#         ('Saudi Arabia', 'Saudi Arabia'),
#         ('Singapore', 'Singapore'),
#         ('Somalia', 'Somalia'),
#         ('South Korea', 'South Korea'),
#         ('Sri Lanka', 'Sri Lanka'),
#         ('Sudan', 'Sudan'),
#         ('Sultanate Of Oman', 'Sultanate Of Oman'),
#         ('Syria', 'Syria'),
#         ('Taiwan', 'Taiwan'),
#         ('Thailand', 'Thailand'),
#         ('Tunisia', 'Tunisia'),
#         ('United Arab Emirates', 'United Arab Emirates'),
#         ('Vietnam', 'Vietnam'),
#         ('Yemen', 'Yemen'),
#     ]
    
#     PAYMENT_CHOICES = [
#         ('Cash', 'Cash'),
#         ('Salary Deduction', 'Salary Deduction'),
#     ]
    
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
#     emp_id = models.CharField(max_length=200, blank=True, null=True)
#     username = models.CharField(max_length=200,blank=True, null=True)
#     department = models.CharField(max_length=100,blank=True, null=True)
#     email = models.EmailField(max_length=100, blank=True, null=True)
#     group = models.CharField(max_length=100, blank=True, null=True)
    
#     employee_name=models.CharField(max_length=200, blank=True, null=True,choices=NAME_CHOICES)
    
#     country_travel_to = models.CharField(max_length=200,choices=COUNTRY_CHOICES)
    
#     reason = models.TextField(max_length=100, blank=True, null=True,
#     choices=[("Business Trip Other Expenses","Business Trip Other Expenses")])
#     reimbursement_amount = models.FloatField()
#     travel_request = models.CharField(max_length=100)
#     mode_of_payment = models.CharField(max_length=100,choices=PAYMENT_CHOICES)
#     amount_to_be_paid_back = models.FloatField()
#     effective_date = models.DateField()
#     comments = models.TextField(blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True)
#     Applied_on=models.DateField(auto_now_add=True,blank=True,null=True)

#     def __str__(self):
#         return f"{self.user.username}'s BusinessTrip"
    
  
# class EmployeeAttendanceException(models.Model):
    
#     user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
#     employee_name = models.CharField(max_length=255,default=True,null=True, verbose_name='Employee Name')
#     employee_id = models.CharField(max_length=10)
#     email = models.EmailField()
#     business_group = models.CharField(max_length=100)
#     department = models.CharField(max_length=100)
#     date_of_exception = models.DateField()
#     hours_late_in = models.IntegerField()
#     minutes_late_in = models.IntegerField()
#     hours_early_out = models.IntegerField()
#     minutes_early_out = models.IntegerField()
#     reason = models.CharField(max_length=255,default=True,null=True, verbose_name='Reason')

#     REASON_CHOICES = [ 
#         ('Arrived late night from vacation', 'Arrived late night from vacation'),
#         ('Bank work', 'Bank work'),
#         ('COMP OFF', 'COMP Off'),
#         ('Doctor Appointment', 'Doctor Appointment'),
#         ('Due to Doctor Visit Self', 'Due to Doctor Visit Self'),
#         ('Due to Doctor Visit with Family', 'Due to Doctor Visit with Family'),
#         ('Due to annual leave', 'Due to annual leave'),
#         ('Due to delay Metro', 'Due to delay Metro'),
#         ('Due to headache' ,'Due to headache'),
#         ('Due to personal work', 'Due to personal work'),
#         ('Forget to Punch in','Forget to Punch in'),
#         ('Forgot to Punch out','Forgot to Punch out'),
#         ('Missed Punch In','Missed Punch In'),
#         ('Missed Punch Out','Missed Punch Out'),
#         ('Not well so late to office','Not well so late to office'),
#         ('On Customer Site','On Customer Site'),
#         ('On Siite','On Siite'),
#         ('Others','Others'),
#         ('Traffic','Traffic'),
#         ('Went to kid school','Went to kid school'),
#         ('Worked extra hours', 'Worked extra hours')

#     ]

#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
#     reason_category = models.CharField(max_length=200, choices=REASON_CHOICES)
#     applied_date = models.DateField(auto_now_add=True, blank=True, null=True)

#     def _str_(self):
#         return f"{self.employee_id} - {self.date_of_exception}"


# class DocumentForVisa(models.Model):

#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]
#     DOCUMENT_TYPE =[
#         ('AE_VISA','AE_VISA')
#     ]

#     COUNTRY_CHOICES = [
#         ('Afghanistan', 'Afghanistan'),
#         ('Algeria', 'Algeria'),
#         ('Bahrain', 'Bahrain'),
#         ('Bangladesh', 'Bangladesh'),
#         ('Bhutan', 'Bhutan'),
#         ('Burma Union Myanmar', 'Burma Union Myanmar'),
#         ('China', 'China'),
#         ('Djibouti', 'Djibouti'),
#         ('Egypt', 'Egypt'),
#         ('Hong Kong', 'Hong Kong'),
#         ('India', 'India'),
#         ('Indonesia', 'Indonesia'),
#         ('Iran', 'Iran'),
#         ('Iraq', 'Iraq'),
#         ('Japan', 'Japan'),
#         ('Jordan', 'Jordan'),
#         ('Kampuchea', 'Kampuchea'),
#         ('Kuwait', 'Kuwait'),
#         ('Lebanon', 'Lebanon'),
#         ('Libya', 'Libya'),
#         ('Malaysia', 'Malaysia'),
#         ('Mauritania', 'Mauritania'),
#         ('Morocco', 'Morocco'),
#         ('Nepal', 'Nepal'),
#         ('North Korea', 'North Korea'),
#         ('Pakistan', 'Pakistan'),
#         ('Palestine', 'Palestine'),
#         ('Philippines', 'Philippines'),
#         ('Qatar', 'Qatar'),
#         ('Saudi Arabia', 'Saudi Arabia'),
#         ('Singapore', 'Singapore'),
#         ('Somalia', 'Somalia'),
#         ('South Korea', 'South Korea'),
#         ('Sri Lanka', 'Sri Lanka'),
#         ('Sudan', 'Sudan'),
#         ('Sultanate Of Oman', 'Sultanate Of Oman'),
#         ('Syria', 'Syria'),
#         ('Taiwan', 'Taiwan'),
#         ('Thailand', 'Thailand'),
#         ('Tunisia', 'Tunisia'),
#         ('United Arab Emirates', 'United Arab Emirates'),
#         ('Vietnam', 'Vietnam'),
#         ('Yemen', 'Yemen'),
#     ]

#     VISA_TYPE_CHOICES = [
#         ('Family Visa', 'Family Visa'),
#         ('Residence Permit', 'Residence Permit'),
#         ('Visit Visa', 'Visit Visa'),
#     ]

#     SPONSOR_TYPE_CHOICES = [
#         ('Company Sponsored', 'Company Sponsored'),
#         ('Family Sponsored', 'Family Sponsored'),
#     ]
#     VISA_TYPE_CHOICES = [
#         ('Family Visa', 'Family Visa'),
#         ('Residence Permit', 'Residence Permit'),
#         ('Visit Visa', 'Visit Visa'),
#     ]

#     SPONSOR_NAME_CHOICES = [
#         ('A Y C O BUILDING BR OF AL YOUSUF LLC', 'A Y C O BUILDING BR OF AL YOUSUF LLC'),
#         ('AL YOUSUF ELEVATORS & ESCALATORS-BR-AL YOUSUF LLC', 'AL YOUSUF ELEVATORS & ESCALATORS-BR-AL YOUSUF LLC'),
#         ('AL YOUSUF MEDICAL CENTER L.L.C.', 'AL YOUSUF MEDICAL CENTER L.L.C.'),
#         ('AL YOUSUF PHARMACY L.L.C.', 'AL YOUSUF PHARMACY L.L.C.'),
#         ('AL YOUSUF PROPERTY BR OF AL YOUSUF LLC', 'AL YOUSUF PROPERTY BR OF AL YOUSUF LLC'),
#         ('AL YOUSUF ROBOTICS L.L.C.', 'AL YOUSUF ROBOTICS L.L.C.'),
#         ('ALYOUSUF MEDICAL PROJECT CONTRACTING SOLUTIONS L.L.C.', 'ALYOUSUF MEDICAL PROJECT CONTRACTING SOLUTIONS L.L.C.'),
#         ('AUTOSPORT (L.L.C.)', 'AUTOSPORT (L.L.C.)'),
#         ('Advantage Limousine LLC', 'Advantage Limousine LLC'),
#         ('Advantage Limousine-Dubai', 'Advantage Limousine-Dubai'),
#         ('Advantage Taxi LLC', 'Advantage Taxi LLC'),
#         ('Al Yousuf Agricultural and Landscaping LLC', 'Al Yousuf Agricultural and Landscaping LLC'),
#         ('Al Yousuf Computer & Telecommunications (L.L.C.)', 'Al Yousuf Computer & Telecommunications (L.L.C.)'),
#         ('Al Yousuf Computers & Telecommunications Abu Dhabi', 'Al Yousuf Computers & Telecommunications Abu Dhabi'),
#         ('Al Yousuf Electronics LLC', 'Al Yousuf Electronics LLC'),
#         ('Al Yousuf Electronics LLC - Abu Dhabi', 'Al Yousuf Electronics LLC - Abu Dhabi'),
#         ('Al Yousuf International Construction LLC', 'Al Yousuf International Construction LLC'),
#         ('Al Yousuf LLC', 'Al Yousuf LLC'),
#         ('Al Yousuf LLC - Abu Dhabi', 'Al Yousuf LLC - Abu Dhabi'),
#         ('Al Yousuf Motors LLC', 'Al Yousuf Motors LLC'),
#         ('Al Yousuf Motors LLC - Abu Dhabi', 'Al Yousuf Motors LLC - Abu Dhabi'),
#         ('Al Yousuf Real Estate LLC', 'Al Yousuf Real Estate LLC'),
#         ('Al Yousuf Security Controls and Alarms LLC', 'Al Yousuf Security Controls and Alarms LLC'),
#         ('Al Yousuf Sports Equipment LLC', 'Al Yousuf Sports Equipment LLC'),
#         ('Al Yousuf Sports Equipment LLC - Abu Dhabi', 'Al Yousuf Sports Equipment LLC - Abu Dhabi'),
#         ('Alyousuf Technical Solutions L.L.C.', 'Alyousuf Technical Solutions L.L.C.'),
#         ('BIG BLUE MARINE EQUIPMENTS LLC', 'BIG BLUE MARINE EQUIPMENTS LLC'),
#         ('Back on Track LLC', 'Back on Track LLC'),
#         ('Delux Limousine LLC', 'Delux Limousine LLC'),
#         ('Fujitech Co Ltd Dubai BR', 'Fujitech Co Ltd Dubai BR'),
#         ('Future Technology (L.L.C.)', 'Future Technology (L.L.C.)'),
#         ('Future Technology - LLC - Abu Dhabi', 'Future Technology - LLC - Abu Dhabi'),
#         ('Imperbit Menmbrane Industries LLC', 'Imperbit Menmbrane Industries LLC'),
#         ('Jebel Ali Free Zone', 'Jebel Ali Free Zone'),
#         ('Nipon Kaiji Kyokai Dubai', 'Nipon Kaiji Kyokai Dubai'),
#         ('Others', 'Others'),
#         ('Sharjah Airport', 'Sharjah Airport'),
#         ('Yamaha Motors Company', 'Yamaha Motors Company'),
#     ]

#     SPONSOR_RELATIONSHIP_CHOICES = [
#         ('Brother', 'Brother'),
#         ('Daughter', 'Daughter'),
#         ('Father', 'Father'),
#         ('Husband', 'Husband'),
#         ('Mom Husband', 'Mom Husband'),
#         ('Mother', 'Mother'),
#         ('Not Related', 'Not Related'),
#         ('Sister', 'Sister'),
#         ('Son', 'Son'),
#         ('Wife', 'Wife'),
#     ]

#     SPONSOR_NATIONALITY_CHOICES = [
#         ('Afghanistan', 'Afghanistan'),
#         ('Aland Islands', 'Aland Islands'),
#         ('Albania', 'Albania'),
#         ('Algeria', 'Algeria'),
#         ('American Samoa', 'American Samoa'),
#         ('Andorra', 'Andorra'),
#         ('Angola', 'Angola'),
#         ('Anguilla', 'Anguilla'),
#         ('Antarctica', 'Antarctica'),
#         ('Antigua', 'Antigua'),
#         ('Antigua and Barbuda', 'Antigua and Barbuda'),
#         ('Argentina', 'Argentina'),
#         ('Armenia', 'Armenia'),
#         ('Aruba', 'Aruba'),
#         ('Australia', 'Australia'),
#         ('Austria', 'Austria'),
#         ('Azerbaijan', 'Azerbaijan'),
#         ('Bahamas', 'Bahamas'),
#         ('Bahrain', 'Bahrain'),
#         ('Bangladesh', 'Bangladesh'),
#         ('Barbados', 'Barbados'),
#         ('Belgium', 'Belgium'),
#         ('Belize', 'Belize'),
#         ('Benin', 'Benin'),
#         ('Bermuda', 'Bermuda'),
#         ('Bhutan', 'Bhutan'),
#         ('Bolivia', 'Bolivia'),
#         ('Bosnia And Herzegovina', 'Bosnia And Herzegovina'),
#         ('Botswana', 'Botswana'),
#         ('Bouvet Island', 'Bouvet Island'),
#         ('Brazil', 'Brazil'),
#         ('British Indian Ocean Territory', 'British Indian Ocean Territory'),
#         ('Brunei', 'Brunei'),
#         ('Bulgaria', 'Bulgaria'),
#         ('Burkina Faso', 'Burkina Faso'),
#         ('Burma Union Myanmar', 'Burma Union Myanmar'),
#         ('Burundi', 'Burundi'),
#         ('Cambodia', 'Cambodia'),
#         ('Cameroon', 'Cameroon'),
#         ('Canada', 'Canada'),
#         ('Cape Verde', 'Cape Verde'),
#         ('Cayman Island', 'Cayman Island'),
#         ('Central Africa Republic', 'Central Africa Republic'),
#         ('Chad', 'Chad'),
#         ('Chile', 'Chile'),
#         ('China', 'China'),
#         ('Christmas Island', 'Christmas Island'),
#         ('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands'),
#         ('Colombia', 'Colombia'),
#         ('Commonwealth of Dominica', 'Commonwealth of Dominica'),
#         ('Comoros', 'Comoros'),
#         ('Congo', 'Congo'),
#         ('Cook Islands', 'Cook Islands'),
#         ('Costa Rica', 'Costa Rica'),
#         ("Cote d'Ivoire'", "Cote d'Ivoire'"),
#         ('Croatia', 'Croatia'),
#         ('Cuba', 'Cuba'),
#         ('Cyprus', 'Cyprus'),
#         ('Czech', 'Czech'),
#         ('Czechoslovakia', 'Czechoslovakia'),
#         ('Dagestan', 'Dagestan'),
#         ('Dahomey', 'Dahomey'),
#         ('Denmark', 'Denmark'),
#         ('Djibouti', 'Djibouti'),
#         ('Dominican', 'Dominican'),
#         ('East Timor', 'East Timor'),
#         ('Ecuador', 'Ecuador'),
#         ('Egypt', 'Egypt'),
#         ('El Salvador', 'El Salvador'),
#         ('Eritrea', 'Eritrea'),
#         ('Estonia', 'Estonia'),
#         ('Ethiopia', 'Ethiopia'),
#         ('Falkland Islands (Malvinas)', 'Falkland Islands (Malvinas)'),
#         ('Faroe Islands', 'Faroe Islands'),
#         ('Fiji', 'Fiji'),
#         ('Finland', 'Finland'),
#         ('France', 'France'),
#         ('French Guiana', 'French Guiana'),
#         ('French Polynesia', 'French Polynesia'),
#         ('French Southern Territories', 'French Southern Territories'),
#         ('Gabon', 'Gabon'),
#         ('Gambia', 'Gambia'),
#         ('Georgia', 'Georgia'),
#         ('Germany', 'Germany'),
#         ('Ghana', 'Ghana'),
#         ('Gibraltar', 'Gibraltar'),
#         ('Greece', 'Greece'),
#         ('Greenland', 'Greenland'),
#         ('Grenada', 'Grenada'),
#         ('Guadeloupe', 'Guadeloupe'),
#         ('Guam', 'Guam'),
#         ('Guatemala', 'Guatemala'),
#         ('Guernsey', 'Guernsey'),
#         ('Guinea', 'Guinea'),
#         ('Guinea-Bissau', 'Guinea-Bissau'),
#         ('Guyana', 'Guyana'),
#         ('Haiti', 'Haiti'),
#         ('Heard Island and McDonald Islands', 'Heard Island and McDonald Islands'),
#         ('Honduras', 'Honduras'),
#         ('Hong Kong', 'Hong Kong'),
#         ('Hungary', 'Hungary'),
#         ('Iceland', 'Iceland'),
#         ('India', 'India'),
#         ('Indonesia', 'Indonesia'),
#         ('Iran', 'Iran'),
#         ('Iraq', 'Iraq'),
#         ('Ireland', 'Ireland'),
#         ('Isle of Man', 'Isle of Man'),
#         ('Israel', 'Israel'),
#         ('Italy', 'Italy'),
#         ('Jamaica', 'Jamaica'),
#         ('Japan', 'Japan'),
#         ('Jersey', 'Jersey'),
#         ('Jordan', 'Jordan'),
#         ('Kampuchea', 'Kampuchea'),
#         ('Kazakhstan', 'Kazakhstan'),
#         ('Kenya', 'Kenya'),
#         ('Kingston', 'Kingston'),
#         ('Kiribati', 'Kiribati'),
#         ('Kosovo', 'Kosovo'),
#         ('Kuwait', 'Kuwait'),
#         ('Kyrgyz', 'Kyrgyz'),
#         ('Kyrgyz Republic', 'Kyrgyz Republic'),
#         ('Kyrgyzstan', 'Kyrgyzstan'),
#         ('Laos', 'Laos'),
#         ('Latvia', 'Latvia'),
#         ('Lebanon', 'Lebanon'),
#         ('Lesotho', 'Lesotho'),
#         ('Liberia', 'Liberia'),
#         ('Libya', 'Libya'),
#         ('Liechtenstein', 'Liechtenstein'),
#         ('Lithuania', 'Lithuania'),
#         ('Luxembourg', 'Luxembourg'),
#         ('Macau', 'Macau'),
#         ('Madagascar', 'Madagascar'),
#         ('Magnolia', 'Magnolia'),
#         ('Malawi', 'Malawi'),
#         ('Malaysia', 'Malaysia'),
#         ('Maldives', 'Maldives'),
#         ('Mali', 'Mali'),
#         ('Malta', 'Malta'),
#         ('Marshall Island', 'Marshall Island'),
#         ('Martinez Islands', 'Martinez Islands'),
#         ('Martinique', 'Martinique'),
#         ('Maryanne Island', 'Maryanne Island'),
#         ('Mauritania', 'Mauritania'),
#         ('Mauritius', 'Mauritius'),
#         ('Mayotte', 'Mayotte'),
#         ('Mexico', 'Mexico'),
#         ('Micronesia', 'Micronesia'),
#         ('Moldavia', 'Moldavia'),
#         ('Monaco', 'Monaco'),
#         ('Mongolia', 'Mongolia'),
#         ('Montenegro', 'Montenegro'),
#         ('Montserrat', 'Montserrat'),
#         ('Morocco', 'Morocco'),
#         ('Mozambique', 'Mozambique'),
#         ('Namibia', 'Namibia'),
#         ('Nauru', 'Nauru'),
#         ('Nepal', 'Nepal'),
#         ('Netherlands', 'Netherlands'),
#         ('Netherlands Antilles', 'Netherlands Antilles'),
#         ('Nevis', 'Nevis'),
#         ('New Caledonia', 'New Caledonia'),
#         ('New Guinea', 'New Guinea'),
#         ('New Zealand', 'New Zealand'),
#         ('Nicaragua', 'Nicaragua'),
#         ('Niger', 'Niger'),
#         ('Nigeria', 'Nigeria'),
#         ('Niue', 'Niue'),
#         ('Norfolk Island', 'Norfolk Island'),
#         ('North Korea', 'North Korea'),
#         ('Northern Mariana Islands', 'Northern Mariana Islands'),
#         ('Norway', 'Norway'),
#         ('Okinawa', 'Okinawa'),
#         ('Other countries', 'Other countries'),
#         ('Pakistan', 'Pakistan'),
#         ('Palau', 'Palau'),
#         ('Palestine', 'Palestine'),
#         ('Panama', 'Panama'),
#         ('Paraguay', 'Paraguay'),
#         ('Peru', 'Peru'),
#         ('Philippines', 'Philippines'),
#         ('Poland', 'Poland'),
#         ('Portugal', 'Portugal'),
#         ('Puerto Rico', 'Puerto Rico'),
#         ('Qatar', 'Qatar'),
#         ('Republic Of Belarus', 'Republic Of Belarus'),
#         ('Republic Of Guinea', 'Republic Of Guinea'),
#         ('Republic Of Macedonia', 'Republic Of Macedonia'),
#         ('Reunion', 'Reunion'),
#         ('Romania', 'Romania'),
#         ('Russia', 'Russia'),
#         ('Rwanda', 'Rwanda'),
#         ('Ryukyu Islands', 'Ryukyu Islands'),
#         ('Saint Kitts And Nevis', 'Saint Kitts And Nevis'),
#         ('Saint Lucia', 'Saint Lucia'),
#         ('Saint Pierre and Miquelon', 'Saint Pierre and Miquelon'),
#         ('Saint Vincent', 'Saint Vincent'),
#         ('San Marino', 'San Marino'),
#         ('Sao Tome', 'Sao Tome'),
#         ('Saudi Arabia', 'Saudi Arabia'),
#         ('Senegal', 'Senegal'),
#         ('Serbia', 'Serbia'),
#         ('Seychelles', 'Seychelles'),
#         ('Sierra Leone', 'Sierra Leone'),
#         ('Singapore', 'Singapore'),
#         ('Slovakia', 'Slovakia'),
#         ('Slovenia', 'Slovenia'),
#         ('Solomon Island', 'Solomon Island'),
#         ('Somalia', 'Somalia'),
#         ('South Africa', 'South Africa'),
#         ('South Georgia and the South Sandwich Islands', 'South Georgia and the South Sandwich Islands'),
#         ('South Korea', 'South Korea'),
#         ('South Sudan', 'South Sudan'),
#         ('Soviet Union', 'Soviet Union'),
#         ('Spain', 'Spain'),
#         ('Sri Lanka', 'Sri Lanka'),
#         ('St Christopher', 'St Christopher'),
#         ('St Helena', 'St Helena'),
#         ('Sudan', 'Sudan'),
#         ('Sultanate Of Oman', 'Sultanate Of Oman'),
#         ('Suriname', 'Suriname'),
#         ('Svalbard and Jan Mayen', 'Svalbard and Jan Mayen'),
#         ('Swaziland', 'Swaziland'),
#         ('Sweden', 'Sweden'),
#         ('Switzerland', 'Switzerland'),
#         ('Syria', 'Syria'),
#         ('Tahiti', 'Tahiti'),
#         ('Taiwan', 'Taiwan'),
#         ('Tajikistan', 'Tajikistan'),
#         ('Tanzania', 'Tanzania'),
#         ('Tasmania', 'Tasmania'),
#         ('Thailand', 'Thailand'),
#         ('The Democratic Republic Of Congo', 'The Democratic Republic Of Congo'),
#         ('The Hellenic Republic', 'The Hellenic Republic'),
#         ('Timor', 'Timor'),
#         ('Togo', 'Togo'),
#         ('Tokelau', 'Tokelau'),
#         ('Tonga', 'Tonga'),
#         ('Tonga Islands', 'Tonga Islands'),
#         ('Trinidad', 'Trinidad'),
#         ('Tunisia', 'Tunisia'),
#         ('Turkey', 'Turkey'),
#         ('Turkmenistan', 'Turkmenistan'),
#         ('Turks and Caicos Islands', 'Turks and Caicos Islands'),
#         ('Tuvalu', 'Tuvalu'),
#         ('U S A', 'U S A'),
#         ('Uganda', 'Uganda'),
#         ('Ukraine', 'Ukraine'),
#         ('United Arab Emirates', 'United Arab Emirates'),
#         ('United Kingdom', 'United Kingdom'),
#         ('United States Minor Outlying Islands', 'United States Minor Outlying Islands'),
#         ('Uruguay', 'Uruguay'),
#         ('Uzbekistan', 'Uzbekistan'),
#         ('Vanuatu', 'Vanuatu'),
#         ('Vatican', 'Vatican'),
#         ('Venezuela', 'Venezuela'),
#         ('Vietnam', 'Vietnam'),
#         ('Virgin Islands, British', 'Virgin Islands, British'),
#         ('Vietnam', 'Vietnam'),
#         ('Virgin Islands, British', 'Virgin Islands, British'),
#         ('Virgin Islands, U.S.', 'Virgin Islands, U.S.'),
#         ('Wallis and Futuna', 'Wallis and Futuna'),
#         ('Western Sahara', 'Western Sahara'),
#         ('Western Samoa', 'Western Samoa'),
#         ('Yemen', 'Yemen'),
#         ('Yugoslavia', 'Yugoslavia'),
#         ('Zambia', 'Zambia'),
#         ('Zimbabwe', 'Zimbabwe'),
#         ]
#     EMIRATE_CHOICES = [
#     ('Abu Dhabi', 'Abu Dhabi'),
#     ('Ajman', 'Ajman'),
#     ('Al Ain', 'Al Ain'),
#     ('Dubai', 'Dubai'),
#     ('Fujairah', 'Fujairah'),
#     ('Ras al-Khaimah', 'Ras al-Khaimah'),
#     ('Sharjah', 'Sharjah'),
#     ('Umm al-Qaiwain', 'Umm al-Qaiwain'),
#     ]

    
#     #DOCCMENT INFORMATION FOR ALL
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     emp_id = models.CharField(max_length=200, blank=True, null=True)
#     username = models.CharField(max_length=200,blank=True, null=True)
#     department = models.CharField(max_length=100,blank=True, null=True)
#     email = models.EmailField(max_length=100, blank=True, null=True)
#     group = models.CharField(max_length=100, blank=True, null=True)

#     #EXTRA INFORMATION FOR VISA
#     country_name = models.CharField(max_length=100,choices=COUNTRY_CHOICES,  blank=True, null=True)
#     document_type = models.CharField(max_length=100,choices=DOCUMENT_TYPE, blank=True, null=True)
#     category = models.CharField(max_length=100, blank=True, null=True)
#     sub_category = models.CharField(max_length=100, blank=True, null=True)
#     document_number = models.CharField(max_length=100, blank=True, null=True)
#     issued_by = models.CharField(max_length=100, blank=True, null=True)
#     issued_at = models.CharField(max_length=100, blank=True, null=True)
#     issued_date = models.DateField(blank=True, null=True)
#     issuing_authority = models.CharField(max_length=100, blank=True, null=True)
#     valid_from = models.DateField(blank=True, null=True)
#     valid_to = models.DateField(blank=True, null=True)
#     verified_by = models.CharField(max_length=100, blank=True, null=True)
#     verified_date = models.DateField(blank=True, null=True)
    
#     #Additional Information For VISA
#     visa_number = models.CharField(max_length=100, blank=True, null=True)
#     visa_type = models.CharField(max_length=100,choices=VISA_TYPE_CHOICES ,blank=True, null=True)
#     sponsor_type = models.CharField(max_length=100,choices=SPONSOR_TYPE_CHOICES, blank=True, null=True)
#     sponsor_name = models.CharField(max_length=100,choices=SPONSOR_NAME_CHOICES, blank=True, null=True)
#     sponsor_relationship = models.CharField(max_length=100,choices=SPONSOR_RELATIONSHIP_CHOICES, blank=True, null=True)
#     sponsor_number = models.CharField(max_length=100, blank=True, null=True)
#     sponsor_nationality = models.CharField(max_length=100,choices=SPONSOR_NATIONALITY_CHOICES, blank=True, null=True)
#     emirate = models.CharField(max_length=100,choices=EMIRATE_CHOICES, blank=True, null=True)

#     #For Status
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True)
    
#     #For applied date
#     Applied_on=models.DateTimeField(auto_now_add=True,blank=True,null=True)
   

#     def _str_(self):
#         return f"{self.user.username}'s Document record of visa"
    

# class DocumentForPassport(models.Model):

#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]

#     DOCUMENT_TYPE =[
#         ('AE_PASSPORT','AE_PASSPORT')
#     ]

#     COUNTRY_CHOICES = [
#         ('Afghanistan', 'Afghanistan'),
#         ('Algeria', 'Algeria'),
#         ('Bahrain', 'Bahrain'),
#         ('Bangladesh', 'Bangladesh'),
#         ('Bhutan', 'Bhutan'),
#         ('Burma Union Myanmar', 'Burma Union Myanmar'),
#         ('China', 'China'),
#         ('Djibouti', 'Djibouti'),
#         ('Egypt', 'Egypt'),
#         ('Hong Kong', 'Hong Kong'),
#         ('India', 'India'),
#         ('Indonesia', 'Indonesia'),
#         ('Iran', 'Iran'),
#         ('Iraq', 'Iraq'),
#         ('Japan', 'Japan'),
#         ('Jordan', 'Jordan'),
#         ('Kampuchea', 'Kampuchea'),
#         ('Kuwait', 'Kuwait'),
#         ('Lebanon', 'Lebanon'),
#         ('Libya', 'Libya'),
#         ('Malaysia', 'Malaysia'),
#         ('Mauritania', 'Mauritania'),
#         ('Morocco', 'Morocco'),
#         ('Nepal', 'Nepal'),
#         ('North Korea', 'North Korea'),
#         ('Pakistan', 'Pakistan'),
#         ('Palestine', 'Palestine'),
#         ('Philippines', 'Philippines'),
#         ('Qatar', 'Qatar'),
#         ('Saudi Arabia', 'Saudi Arabia'),
#         ('Singapore', 'Singapore'),
#         ('Somalia', 'Somalia'),
#         ('South Korea', 'South Korea'),
#         ('Sri Lanka', 'Sri Lanka'),
#         ('Sudan', 'Sudan'),
#         ('Sultanate Of Oman', 'Sultanate Of Oman'),
#         ('Syria', 'Syria'),
#         ('Taiwan', 'Taiwan'),
#         ('Thailand', 'Thailand'),
#         ('Tunisia', 'Tunisia'),
#         ('United Arab Emirates', 'United Arab Emirates'),
#         ('Vietnam', 'Vietnam'),
#         ('Yemen', 'Yemen'),
#     ]

#     PASSPORT_TYPE_CHOICES = [
#         ('Family Visa', 'Family Visa'),
#         ('Residence Permit', 'Residence Permit'),
#         ('Visit Visa', 'Visit Visa'),
#     ]
    
#     #DOCUMENT INFORMATION FOR ALL
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     emp_id = models.CharField(max_length=200, blank=True, null=True)
#     username = models.CharField(max_length=200,blank=True, null=True)
#     department = models.CharField(max_length=100,blank=True, null=True)
#     email = models.EmailField(max_length=100, blank=True, null=True)
#     group = models.CharField(max_length=100, blank=True, null=True)

#     #EXTRA INFORMATION FOR PASSPORT
#     country_name = models.CharField(max_length=100,choices=COUNTRY_CHOICES,  blank=True, null=True)
#     document_type = models.CharField(max_length=100,choices=DOCUMENT_TYPE, blank=True, null=True)
#     category = models.CharField(max_length=100, blank=True, null=True)
#     sub_category = models.CharField(max_length=100, blank=True, null=True)
#     document_number = models.CharField(max_length=100, blank=True, null=True)
#     issued_by = models.CharField(max_length=100, blank=True, null=True)
#     issued_at = models.CharField(max_length=100, blank=True, null=True)
#     issued_date = models.DateField(blank=True, null=True)
#     issuing_authority = models.CharField(max_length=100, blank=True, null=True)
#     valid_from = models.DateField(blank=True, null=True)
#     valid_to = models.DateField(blank=True, null=True)
#     verified_by = models.CharField(max_length=100, blank=True, null=True)
#     verified_date = models.DateField(blank=True, null=True)
    
#     #Additional Information For Passport
#     passport_number = models.CharField(max_length=100, blank=True, null=True)
#     passport_type = models.CharField(max_length=100,choices=PASSPORT_TYPE_CHOICES, blank=True, null=True)
#     country_of_issue = models.CharField(max_length=100, blank=True, null=True)
#     place_of_issue = models.CharField(max_length=100, blank=True, null=True)
#     number_of_accompanying_person = models.CharField(max_length=100, blank=True, null=True)
#     previous_passport_number = models.CharField(max_length=100, blank=True, null=True)


#     #For Status
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True)

#     #For applied date
#     Applied_on=models.DateTimeField(auto_now_add=True,blank=True,null=True)

#     def _str_(self):
#         return f"{self.user.username}'s Document record of Passport"



# class DocumentForLabourCard(models.Model):

#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]


#     DOCUMENT_TYPE =[
#         ('AE_LABOURCARD','AE_LABOURCARD')
#     ]

#     COUNTRY_CHOICES = [
#         ('Afghanistan', 'Afghanistan'),
#         ('Algeria', 'Algeria'),
#         ('Bahrain', 'Bahrain'),
#         ('Bangladesh', 'Bangladesh'),
#         ('Bhutan', 'Bhutan'),
#         ('Burma Union Myanmar', 'Burma Union Myanmar'),
#         ('China', 'China'),
#         ('Djibouti', 'Djibouti'),
#         ('Egypt', 'Egypt'),
#         ('Hong Kong', 'Hong Kong'),
#         ('India', 'India'),
#         ('Indonesia', 'Indonesia'),
#         ('Iran', 'Iran'),
#         ('Iraq', 'Iraq'),
#         ('Japan', 'Japan'),
#         ('Jordan', 'Jordan'),
#         ('Kampuchea', 'Kampuchea'),
#         ('Kuwait', 'Kuwait'),
#         ('Lebanon', 'Lebanon'),
#         ('Libya', 'Libya'),
#         ('Malaysia', 'Malaysia'),
#         ('Mauritania', 'Mauritania'),
#         ('Morocco', 'Morocco'),
#         ('Nepal', 'Nepal'),
#         ('North Korea', 'North Korea'),
#         ('Pakistan', 'Pakistan'),
#         ('Palestine', 'Palestine'),
#         ('Philippines', 'Philippines'),
#         ('Qatar', 'Qatar'),
#         ('Saudi Arabia', 'Saudi Arabia'),
#         ('Singapore', 'Singapore'),
#         ('Somalia', 'Somalia'),
#         ('South Korea', 'South Korea'),
#         ('Sri Lanka', 'Sri Lanka'),
#         ('Sudan', 'Sudan'),
#         ('Sultanate Of Oman', 'Sultanate Of Oman'),
#         ('Syria', 'Syria'),
#         ('Taiwan', 'Taiwan'),
#         ('Thailand', 'Thailand'),
#         ('Tunisia', 'Tunisia'),
#         ('United Arab Emirates', 'United Arab Emirates'),
#         ('Vietnam', 'Vietnam'),
#         ('Yemen', 'Yemen'),
#     ]

#     ALY_PLACE_OF_ISSUE = [
#         ('Abu Dhabi ', 'Abu Dhabi'),
#         ('Ajman', 'Ajman'),
#         ('Al Ain', 'Al Ain'),
#         ('Dubai', 'Dubai'),
#         ('Fujairah', 'Fujairah'),
#         ('Ras al-Khaimah', 'Ras al-Khaimah'),
#         ('Sharjah', 'Sharjah'),
#         ('Umm al-Qaiwain', 'Umm al-Qaiwain'),
#     ]
    
#     #DOCUMENT INFORMATION FOR ALL
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     emp_id = models.CharField(max_length=200, blank=True, null=True)
#     username = models.CharField(max_length=200,blank=True, null=True)
#     department = models.CharField(max_length=100,blank=True, null=True)
#     email = models.EmailField(max_length=100, blank=True, null=True)
#     group = models.CharField(max_length=100, blank=True, null=True)

#     #EXTRA INFORMATION FOR LABOURCARD
#     country_name = models.CharField(max_length=100,choices=COUNTRY_CHOICES,  blank=True, null=True)
#     document_type = models.CharField(max_length=100,choices=DOCUMENT_TYPE, blank=True, null=True)
#     category = models.CharField(max_length=100, blank=True, null=True)
#     sub_category = models.CharField(max_length=100, blank=True, null=True)
#     document_number = models.CharField(max_length=100, blank=True, null=True)
#     issued_by = models.CharField(max_length=100, blank=True, null=True)
#     issued_at = models.CharField(max_length=100, blank=True, null=True)
#     issued_date = models.DateField(blank=True, null=True)
#     issuing_authority = models.CharField(max_length=100, blank=True, null=True)
#     valid_from = models.DateField(blank=True, null=True)
#     valid_to = models.DateField(blank=True, null=True)
#     verified_by = models.CharField(max_length=100, blank=True, null=True)
#     verified_date = models.DateField(blank=True, null=True)
    
#     #Additional Information For Labour Card
#     aly_personal_id_number = models.CharField(max_length=100, blank=True, null=True)
#     aly_work_permit_number = models.CharField(max_length=100, blank=True, null=True)
#     aly_place_of_issue = models.CharField(max_length=100,choices=ALY_PLACE_OF_ISSUE, blank=True, null=True)
    

#     status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True)

#     #For applied date
#     Applied_on=models.DateTimeField(auto_now_add=True,blank=True,null=True)

#     def str(self):
#         return f"{self.user.username}'s Document record of Labour Card"
    

# class EmployeeResumption(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
#     employee_name = models.CharField(max_length=200)
#     employee_id = models.CharField(max_length=200)
#     email = models.EmailField(max_length=100)
#     group = models.CharField(max_length=100)
#     department = models.CharField(max_length=100)
#     # enter_date = models.DateField(auto_now_add=True, blank=True, null=True)
#     enter_date = models.DateField(blank=True, null=True)
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]
#     RESUMPTION_STATUS = [
#         ('Overstayed with prior intimation and separate leave application for extension of overstayed leave period is to be submitted', 'Overstayed with prior intimation and separate leave application for extension of overstayed leave period is to be submitted'),
#         ('Overstayed without prior approval or intimation and is liable for termination', 'Overstayed without prior approval or intimation and is liable for termination'),
#         ('Overstayed without prior approval/intimation', 'Overstayed without prior approval/intimation'),
#         ('Reported for duty prior to expiry of leave', 'Reported for duty prior to expiry of leave'),
#         ('Reported for duty without any overstay', 'Reported for duty without any overstay'),
        
#     ]
#     status = models.CharField(max_length=100, choices=STATUS_CHOICES, blank=True)
#     other = models.CharField(max_length=100, blank=True, null=True)
#     days_overstayed = models.PositiveIntegerField(default=0)
#     comment = models.CharField(max_length=100, blank=True, null=True)
#     resumption_status=models.CharField(max_length=200,choices=RESUMPTION_STATUS, blank=True, null=True)
#     Applied_on = models.DateField(auto_now_add=True, blank=True, null=True)

  

#     def _str_(self):
#         return f"{self.employee_name} - {self.employee_id}"




# class BankAccount(models.Model):
    
#     BANK_CHOICES = [
#         ('ALFA Exchange', 'ALFA Exchange'),
#         ('ARBIFT', 'ARBIFT'),
#         ('Abu Dhabi Commercial Bank', 'Abu Dhabi Commercial Bank'),
#         ('Abu Dhabi Islamic Bank', 'Abu Dhabi Islamic Bank'),
#         ('Ahmed Al Amery Exchange Est - Abu Dhabi', 'Ahmed Al Amery Exchange Est - Abu Dhabi'),
#         ('Ahmed Al Hussain Exchange Est - Dubai', 'Ahmed Al Hussain Exchange Est - Dubai'),
#         ('Ain Al Faydah Exchange - Al Ain', 'Ain Al Faydah Exchange - Al Ain'),
#         ('Ajman Bank', 'Ajman Bank'),
#         ('Al Ahalia Money Exchange Bureau - Abu Dhabi', 'Al Ahalia Money Exchange Bureau - Abu Dhabi'),
#         ('Al Ahli Bank Of Kuwait K.S.C.', 'Al Ahli Bank Of Kuwait K.S.C.'),
#         ('Al Ansari Exchange LLC', 'Al Ansari Exchange LLC'),
#         ('Al Ansari Exchange Services - Al Ain', 'Al Ansari Exchange Services - Al Ain'),
#         ('Al Azhar Exchange - Dubai', 'Al Azhar Exchange - Dubai'),
#         ('Al Bader Exchange - Abu Dhabi', 'Al Bader Exchange - Abu Dhabi'),
#         ('Al Balooch Money Exchange - Al Ain', 'Al Balooch Money Exchange - Al Ain'),
#         ('Al Dahab Exchange Dubai', 'Al Dahab Exchange Dubai'),
#         ('Al Darmaki Exchange Est - Dubai', 'Al Darmaki Exchange Est - Dubai'),
#         ('Al Dhahery Exchange', 'Al Dhahery Exchange'),
#         ('Al Dhahery Money Exchange - Al Ain', 'Al Dhahery Money Exchange - Al Ain'),
#         ('Al Dinar Exchange Company', 'Al Dinar Exchange Company'),
#         ('Al Falah Exchange Company - Abu Dhabi', 'Al Falah Exchange Company - Abu Dhabi'),
#         ('Al Fardan Exchange - Abu Dhabi', 'Al Fardan Exchange - Abu Dhabi'),
#         ('Al Fuad Exchange - Dubai', 'Al Fuad Exchange - Dubai'),
#         ('Al Gergawi Exchange LLC - Dubai', 'Al Gergawi Exchange LLC - Dubai'),
#         ('Al Ghurair Exchange - Dubai', 'Al Ghurair Exchange - Dubai'),
#         ('Al Ghurair International Exchange - Dubai', 'Al Ghurair International Exchange - Dubai'),
#         ('Al Hadha Exchange LLC - Dubai', 'Al Hadha Exchange LLC - Dubai'),
#         ('Al Hamed Exchange - Sharjah', 'Al Hamed Exchange - Sharjah'),
#         ('Al Hamriyah Exchange - Dubai', 'Al Hamriyah Exchange - Dubai'),
#         ('Al Hilal Bank', 'Al Hilal Bank'),
#         ('Al Jarwan Money Exchange - Sharjah', 'Al Jarwan Money Exchange - Sharjah'),
#         ('Al Masood Exchange - Abu Dhabi', 'Al Masood Exchange - Abu Dhabi'),
#         ('Al Mazroui Exchange Est - Abu Dhabi', 'Al Mazroui Exchange Est - Abu Dhabi'),
#         ('Al Modawallah Exchange - Dubai', 'Al Modawallah Exchange - Dubai'),
#         ('Al Mona Exchange CO LLC - Dubai', 'Al Mona Exchange CO LLC - Dubai'),
#         ('Al Mussabah Exchange - Dubai', 'Al Mussabah Exchange - Dubai'),
#         ('Al Nafees Exchange LLC - Dubai', 'Al Nafees Exchange LLC - Dubai'),
#         ('Al Ne\'Emah Exchange CO LLC - Dubai', 'Al Ne\'Emah Exchange CO LLC - Dubai'),
#         ('Al Nibal International Exchange', 'Al Nibal International Exchange'),
#         ('Al Rajihi Exchange Company LLC - Dubai', 'Al Rajihi Exchange Company LLC - Dubai'),
#         ('Al Razouki Int\'L Exchange CO LLC - Dubai', 'Al Razouki Int\'L Exchange CO LLC - Dubai'),
#         ('Al Rostamani Exchange - Dubai', 'Al Rostamani Exchange - Dubai'),
#         ('Al Zari & Al Fardan Exchange LLC - Sharjah', 'Al Zari & Al Fardan Exchange LLC - Sharjah'),
#         ('Al Zarooni Exchange - Dubai', 'Al Zarooni Exchange - Dubai'),
#         ('Alfalah Exchange Company', 'Alfalah Exchange Company'),
#         ('Alukkass Exchange Dubai', 'Alukkass Exchange Dubai'),
#         ('Arab African International Bank', 'Arab African International Bank'),
#         ('Arab Bank - Qatar', 'Arab Bank - Qatar'),
#         ('Arab Bank PLC', 'Arab Bank PLC'),
#         ('Arabian Exchange Co - Abu Dhabi', 'Arabian Exchange Co - Abu Dhabi'),
#         ('Ary International Exchange - Dubai', 'Ary International Exchange - Dubai'),
#         ('Asia Exchange Centre - Dubai', 'Asia Exchange Centre - Dubai'),
#         ('Aziz Exchange CO LLC - Dubai', 'Aziz Exchange CO LLC - Dubai'),
#         # Add your new bank choices here
#         ('Bank MISR', 'Bank MISR'),
#         ('Bank Melli Iran', 'Bank Melli Iran'),
#         ('Bank Of Baroda - Al Ain', 'Bank Of Baroda - Al Ain'),
#         ('Bank Of Baroda - Deira', 'Bank Of Baroda - Deira'),
#         ('Bank Of Baroda - Dubai HO', 'Bank Of Baroda - Dubai HO'),
#         ('Bank Of Baroda - RAK', 'Bank Of Baroda - RAK'),
#         ('Bank Of Baroda - Sharjah', 'Bank Of Baroda - Sharjah'),
#         ('Bank Of Sharjah', 'Bank Of Sharjah'),
#         ('Bank Saderat Iran', 'Bank Saderat Iran'),
#         ('Banque Libanaise(France)', 'Banque Libanaise(France)'),
#         ('Banque Paribas', 'Banque Paribas'),
#         ('Barclays', 'Barclays'),
#         ('Bhagwandas Jethanand And Sons - Sharjah', 'Bhagwandas Jethanand And Sons - Sharjah'),
#         ('Bin Bakheet Exchange Est - Ajman', 'Bin Bakheet Exchange Est - Ajman'),
#         ('Bin Belaila Exchange CO LLC', 'Bin Belaila Exchange CO LLC'),
#         ('Bin Belaila Exchange CO LLC - Dubai', 'Bin Belaila Exchange CO LLC - Dubai'),
#         ('Blom Bank France', 'Blom Bank France'),
#         ('C3', 'C3'),
#         ('Cash Express Exchange Est - Dubai', 'Cash Express Exchange Est - Dubai'),
#         ('Citibank N.A.', 'Citibank N.A.'),
#         ('City Exchange LLC - Dubai', 'City Exchange LLC - Dubai'),
#         ('Commercial Bank Of Dubai', 'Commercial Bank Of Dubai'),
#         ('Commercial Bank-Qatar', 'Commercial Bank-Qatar'),
#         ('Credit Agricole', 'Credit Agricole'),
#         ('Daniba International Exchange - Dubai', 'Daniba International Exchange - Dubai'),
#         ('Day Exchange LLC - Dubai', 'Day Exchange LLC - Dubai'),
#         ('Dinar Exchange - Dubai', 'Dinar Exchange - Dubai'),
#         ('Doha Bank', 'Doha Bank'),
#         ('Dubai Bank PJSC', 'Dubai Bank PJSC'),
#         ('Dubai Exchange Centre LLC - Dubai', 'Dubai Exchange Centre LLC - Dubai'),
#         ('Dubai Express Exchange', 'Dubai Express Exchange'),
#         ('Dubai Islamic Bank', 'Dubai Islamic Bank'),
#         ('Dunia', 'Dunia'),
#         ('Economic Exchange', 'Economic Exchange'),
#         ('Economic Exchange Centre', 'Economic Exchange Centre'),
#         ('El Nilein Bank', 'El Nilein Bank'),
#         ('Emirates & East India Exchange - Sharjah', 'Emirates & East India Exchange - Sharjah'),
#         ('Emirates India International Exchange - Sharjah', 'Emirates India International Exchange - Sharjah'),
#         ('Emirates Islamic Bank', 'Emirates Islamic Bank'),
#         ('Emirates NBD', 'Emirates NBD'),
#         ('Federal Exchange - Dubai', 'Federal Exchange - Dubai'),
#         ('Finance House', 'Finance House'),
#         ('First Gulf Bank', 'First Gulf Bank'),
#         ('First Gulf Exchange Centre - Dubai', 'First Gulf Exchange Centre - Dubai'),
#         ('Future Exchange', 'Future Exchange'),
#         ('GCC Exchange', 'GCC Exchange'),
#         ('Global Exchange', 'Global Exchange'),
#         ('Gomti Exchange LLC - Dubai', 'Gomti Exchange LLC - Dubai'),
#         ('Gulf Express Exchange - Dubai', 'Gulf Express Exchange - Dubai'),
#         ('Gulf Int\'L Exchange CO LLC - Dubai', 'Gulf Int\'L Exchange CO LLC - Dubai'),
#         ('HSBC Financial Services', 'HSBC Financial Services'),
#         ('HSBC Middle East', 'HSBC Middle East'),
#         ('Habib Bank A.G. Zurich', 'Habib Bank A.G. Zurich'),
#         ('Habib Bank Limited', 'Habib Bank Limited'),
#         ('Habib Exchange CO LLC - Sharjah', 'Habib Exchange CO LLC - Sharjah'),
#         ('Hadi Express Exchange - Dubai', 'Hadi Express Exchange - Dubai'),
#         ('Harib Sultan Exchange - Abu Dhabi', 'Harib Sultan Exchange - Abu Dhabi'),
#         ('Horizon Exchange - Dubai', 'Horizon Exchange - Dubai'),
#         ('International Development Exchange - Dubai', 'International Development Exchange - Dubai'),
#         ('Invest Bank', 'Invest Bank'),
#         ('Janata Bank', 'Janata Bank'),
#         ('Jumana Exchange Est - Dubai', 'Jumana Exchange Est - Dubai'),
#         ('Kanoo Exchange - Dubai', 'Kanoo Exchange - Dubai'),
#         ('Khalil Al Fardan Exchange - Dubai', 'Khalil Al Fardan Exchange - Dubai'),
#         ('Khalili Exchange CO LLC - Dubai', 'Khalili Exchange CO LLC - Dubai'),
#         ('Lari Exchange Est - Abu Dhabi', 'Lari Exchange Est - Abu Dhabi'),
#         ('Lee La Megh Exchange LLC - Dubai', 'Lee La Megh Exchange LLC - Dubai'),
#         ('Lloyds Bank', 'Lloyds Bank'),
#         ('Lulu Exchange', 'Lulu Exchange'),
#         ('Malik Exchange - Abu Dhabi', 'Malik Exchange - Abu Dhabi'),
#         ('Mashreq PSC', 'Mashreq PSC'),
#         ('Multinet Trust Exchange LLC - Dubai', 'Multinet Trust Exchange LLC - Dubai'),
#         ('Nanikdas Nathoomal Exchange CO LLC - Dubai', 'Nanikdas Nathoomal Exchange CO LLC - Dubai'),
#         ('Naser Khoory Exchange Est - Abu Dhabi', 'Naser Khoory Exchange Est - Abu Dhabi'),
#         ('Nasim Al Barari Exchange', 'Nasim Al Barari Exchange'),
#         ('National Bank Of Abu Dhabi', 'National Bank Of Abu Dhabi'),
#         ('National Bank Of Bahrain', 'National Bank Of Bahrain'),
#         ('National Bank Of Fujairah', 'National Bank Of Fujairah'),
#         ('National Bank Of Kuwait', 'National Bank Of Kuwait'),
#         ('National Bank Of Oman', 'National Bank Of Oman'),
#         ('National Bank Of Umm Al Qaiwain', 'National Bank Of Umm Al Qaiwain'),
#         ('National Exchange CO - Abu Dhabi', 'National Exchange CO - Abu Dhabi'),
#         ('Noor Islamic Bank', 'Noor Islamic Bank'),
#         ('Oasis Exchange', 'Oasis Exchange'),
#         ('Orient Exchange COLLC - Dubai', 'Orient Exchange COLLC - Dubai'),
#         ('Others', 'Others'),
#         ('Pacific Exchange - Dubai', 'Pacific Exchange - Dubai'),
#         ('Qatar National Bank', 'Qatar National Bank'),
#         ('Rafidain Bank', 'Rafidain Bank'),
#         ('Rak Bank', 'Rak Bank'),
#         ('Redha Al Ansari Exchange Est - Dubai', 'Redha Al Ansari Exchange Est - Dubai'),
#         ('Reems Exchange - Dubai', 'Reems Exchange - Dubai'),
#         ('Royal Bank Of Canada', 'Royal Bank Of Canada'),
#         ('Royal Bank Of Scotland', 'Royal Bank Of Scotland'),
#         ('Royal Exchange CO LLC', 'Royal Exchange CO LLC'),
#         ('Sa\'Ad Exchange - Fujairah', 'Sa\'Ad Exchange - Fujairah'),
#         ('Sabah Exchange - Sharjah', 'Sabah Exchange - Sharjah'),
#         ('Sajwani Exchange - Dubai', 'Sajwani Exchange - Dubai'),
#         ('Salim Exchange - Sharjah', 'Salim Exchange - Sharjah'),
#         ('Samba Financial Group', 'Samba Financial Group'),
#         ('Sana\'A Exchange - Dubai', 'Sana\'A Exchange - Dubai'),
#         ('Sawan Exchange CO LLC - Dubai', 'Sawan Exchange CO LLC - Dubai'),
#         ('Seidco', 'Seidco'),
#         ('Shaheen Money Exchange LLC - Dubai', 'Shaheen Money Exchange LLC - Dubai'),
#         ('Sharaf Exchange', 'Sharaf Exchange'),
#         ('Sharjah International Exchange - Sharjah', 'Sharjah International Exchange - Sharjah'),
#         ('Sharjah Islamic Bank', 'Sharjah Islamic Bank'),
#         ('Standard Chartered Bank', 'Standard Chartered Bank'),
#         ('Tabra & Al Nebal Exchange - Dubai', 'Tabra & Al Nebal Exchange - Dubai'),
#         ('Tahir Exchange Est - Dubai', 'Tahir Exchange Est - Dubai'),
#         ('Taymour & Abou Harb Exchange CO LLC - Sharjah', 'Taymour & Abou Harb Exchange CO LLC - Sharjah'),
#         ('U.A.E. Exchange Centre LLC - Dubai', 'U.A.E. Exchange Centre LLC - Dubai'),
#         ('Union Exchange - Abu Dhabi', 'Union Exchange - Abu Dhabi'),
#         ('Union National Bank', 'Union National Bank'),
#         ('United Arab Bank', 'United Arab Bank'),
#         ('United Bank Ltd', 'United Bank Ltd'),
#         ('Universal Exchange Centre - Dubai', 'Universal Exchange Centre - Dubai'),
#         ('Wall Street Exchange Centre LLC - Dubai', 'Wall Street Exchange Centre LLC - Dubai'),
#         ('Waseela Equity', 'Waseela Equity'),
#         ('Workers Equity Holdings', 'Workers Equity Holdings'),
#         ('Zahra Al Yousuf Exchange - Dubai', 'Zahra Al Yousuf Exchange - Dubai'),
#         ('Zareen Exchange', 'Zareen Exchange'),
#     ]

     
#     # Add a status field
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
#     employee_name = models.CharField(max_length=100,default=True,blank=True,null=True)
#     employee_id = models.CharField(max_length=50,default=True,blank=True,null=True)
#     email = models.EmailField(default=True,blank=True,null=True)
#     business_group = models.CharField(max_length=100,default=True,blank=True,null=True)
#     department = models.CharField(max_length=100,default=True,blank=True,null=True)
#     bank_name = models.CharField(max_length=100, choices=BANK_CHOICES)
#     branch = models.CharField(max_length=100,default=True,blank=True,null=True)
#     iban_number = models.CharField(max_length=100,default=True,blank=True,null=True)
#     start_date = models.DateField(default=True,blank=True,null=True)
#     bank_code = models.CharField(max_length=50,default=True,blank=True,null=True)
#     comment = models.CharField(default=True,blank=True,null=True)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
#     Applied_date = models.DateField(auto_now_add=True, blank=True, null=True)

#     def __str__(self):
#         return f"{self.employee_name}'s Bank Account"

# class EmployeeTravel(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]

#     PURPOSE_OF_VISIT_CHOICES = [
#         ('business_trip', 'Business Trip'),
#         ('work_assignment', 'Work Assignment'),
#     ]

#     COUNTRY_CHOICES = [
#         ('Afghanistan', 'Afghanistan'),
#         ('Aland Islands', 'Aland Islands'),
#         ('Albania', 'Albania'),
#         ('Algeria', 'Algeria'),
#         ('American Samoa', 'American Samoa'),
#         ('Andorra', 'Andorra'),
#         ('Angola', 'Angola'),
#         ('Anguilla', 'Anguilla'),
#         ('Antarctica', 'Antarctica'),
#         ('Antigua', 'Antigua'),
#         ('Antigua and Barbuda', 'Antigua and Barbuda'),
#         ('Argentina', 'Argentina'),
#         ('Armenia', 'Armenia'),
#         ('Aruba', 'Aruba'),
#         ('Australia', 'Australia'),
#         ('Austria', 'Austria'),
#         ('Azerbaijan', 'Azerbaijan'),
#         # Include all other countries here
#     ]

#     CURRENCY_CHOICES = [
#         ('AED', 'AED'),
#         ('BHD', 'BHD'),
#         ('CNY', 'CNY'),
#         ('EUR', 'EUR'),
#         ('GBP', 'GBP'),
#         ('INR', 'INR'),
#         ('JPY', 'JPY'),
#         ('KRW', 'KRW'),
#         ('KWD', 'KWD'),
#         ('OMR', 'OMR'),
#         ('QAR', 'QAR'),
#         ('SAR', 'SAR'),
#         ('SEK', 'SEK'),
#         ('USD', 'USD'),
#     ]

#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
#     employee_name = models.CharField(max_length=255,blank=True, null=True)
#     emp_id = models.CharField(max_length=100, blank=True, null=True )
#     email = models.EmailField(max_length=100 ,blank=True, null=True)
#     business_group = models.CharField(max_length=100,blank=True, null=True )
#     department = models.CharField(max_length=100 ,blank=True, null=True)
#     request_type = models.CharField(max_length=100,blank=True, null=True )
#     purpose_of_visit = models.CharField(max_length=20, choices=PURPOSE_OF_VISIT_CHOICES,blank=True, null=True)
#     travel_start_date = models.DateField(blank=True, null=True)
#     travel_end_date = models.DateField(blank=True, null=True)
#     country_of_travel = models.CharField(max_length=100, choices=COUNTRY_CHOICES,blank=True, null=True)
#     entity_company_traveling_for = models.CharField(max_length=200,blank=True, null=True)
#     advance_amount_required = models.CharField(default=False,blank=True, null=True)
#     currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES,blank=True, null=True)
#     visa_to_be_processed = models.CharField(max_length=3, blank=True, null=True)
#     book_hotel_accommodation = models.CharField(max_length=3, blank=True, null=True)
#     flight_ticket_required = models.CharField( default=False,blank=True, null=True)
#     visa_letter_required = models.CharField( default=False,blank=True, null=True)
#     comments = models.CharField(max_length=500, blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True,null=True)
#     Applied_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)


#     def str(self):
#         return f"{self.employee_name}'s Employee Travel"

# from django.apps import apps








from datetime import timedelta, timezone
import datetime
from enum import Enum
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.apps import apps
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from enum import Enum

class CustomUser(AbstractUser):
    department = models.CharField(max_length=100, blank=True, null=True)
    emp_id=models.CharField(max_length=200,blank=True,null=True)
    phone_number=models.CharField(max_length=200,blank=True,null=True)
    designation=models.CharField(max_length=200,blank=True,null=True)
    group = models.CharField(max_length=200,blank=True,null=True)
    address=models.CharField(max_length=500,blank=True,null=True)
    country=models.CharField(max_length=100,blank=True,null=True)
    state=models.CharField(max_length=200,blank=True,null=True)
    whats_up_number=models.CharField(max_length=200,blank=True,null=True)
    date_of_birth=models.DateField(max_length=200,blank=True,null=True)
    date_joined = models.DateField(max_length=200,blank=True,null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    def str(self):
        return self.username

# # VISITING CARD MODELS:

class MasterTable(models.Model):

    department = models.CharField(max_length=100, blank=True, null=True)
    emp_id=models.CharField(max_length=200,blank=True,null=True)
    phone_number=models.CharField(max_length=200,blank=True,null=True)
    designation=models.CharField(max_length=200,blank=True,null=True)
    group = models.CharField(max_length=200,blank=True,null=True)
    address=models.CharField(max_length=500,blank=True,null=True)
    country=models.CharField(max_length=100,blank=True,null=True)
    state=models.CharField(max_length=200,blank=True,null=True)
    whats_up_number=models.CharField(max_length=200,blank=True,null=True)
    date_of_birth=models.DateField(max_length=200,blank=True,null=True)
    date_joined = models.DateField(max_length=200,blank=True,null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)

    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)

    #leavesModels
    start_date = models.DateField(max_length=200, blank=True, null=True)
    end_date = models.DateField(max_length=200, blank=True, null=True)
    replaced_by = models.CharField(max_length=200, blank=True, null=True)
    leave_balance = models.IntegerField(default=100)  # Total leaves per year
    duration = models.IntegerField(default=0,null=True,blank=True)
    leaves_applied_date = models.DateField(auto_now_add=True, blank=True, null=True)
    replaced_by = models.CharField(max_length=200, blank=True, null=True)
    leave_reason = models.CharField(max_length=50,default=True,null=True,blank=True)
    leaves_status = models.CharField(max_length=20, blank=True)
    leave_type = models.CharField(max_length=50,  blank=True, null=True,)
    category = models.CharField(max_length=50, null=True,)
    leaves_comments = models.TextField(blank=True)
    passport_withdrawal_date = models.DateField(null=True, blank=True)
    request_for_airticket = models.CharField(max_length=50,null=True, blank=True)

  
    # #Daywise Attendance Models
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True) 
    username=models.CharField(max_length=200,blank=True)
    timeShortageExceed=models.CharField(max_length=200,blank=True)
    total_hours = models.CharField(max_length=50, blank=True, null=True, default='') 
    chk_date = models.DateField(null=True, blank=True) 

    #Visiting Card Models
    mobilenum = models.CharField(max_length=50,default=True,blank=True,null=True)
    poBox = models.CharField(max_length=100,default=True,blank=True,null=True)
    Visitingcountry = models.CharField(max_length=100,default=True,blank=True,null=True)
    telphone = models.CharField(max_length=100,default=True,blank=True,null=True)
    extnum = models.CharField(max_length=100,default=True,blank=True,null=True)
    faxnum = models.CharField(max_length=100,default=True,blank=True,null=True)
    

    #Business Trip Models
    employee_name=models.CharField(max_length=200, blank=True, null=True,)
    country_travel_to = models.CharField(max_length=200,blank=True, null=True)
    businesstrip_reason = models.TextField(max_length=100, blank=True, null=True,)
    choices=[("Business Trip Other Expenses","Business Trip Other Expenses")]
    reimbursement_amount = models.FloatField()
    travel_request = models.CharField(max_length=100,blank=True, null=True)
    mode_of_payment = models.CharField(max_length=100,blank=True, null=True)
    amount_to_be_paid_back = models.FloatField()
    effective_date = models.DateField()
    businessTrip_comments = models.TextField(blank=True, null=True)
    businessTrip_status = models.CharField(max_length=20,blank=True, null=True)
    businessTrip_applied_date=models.DateField(auto_now_add=True,blank=True,null=True)

    #Employee Reimbursement Models
    enter_amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    note=models.CharField(max_length=300,blank=True,null=True,choices=[("Supporting bills should be scanned and attached in request form, originals should be submitted in HRD.Any claims without receipts will not be paid","Supporting bills should be scanned and attached in request form, originals should be submitted in HRD.Any claims without receipts will not be paid")])
    employeereimbursement_comment = models.CharField(max_length=100,blank=True,null=True)
    reimbursement_type = models.CharField(max_length=300,blank=True, null=True)
    employeereimbursement_status = models.CharField(max_length=20,blank=True)
    employeereimbursement_applied_date = models.DateField(auto_now_add=True,blank=True,null=True)

    #Labour Contract Models
    labourcontract_reason = models.CharField(max_length=100, blank=True, null=True)
    amendment_date = models.DateField(blank=True, null=True)
    labourContract_comments = models.CharField(max_length=500, blank=True, null=True)
    labourContract_status = models.CharField(max_length=20,blank=True)
    labourContract_applied_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    #Medical Reimbursement Models
    medicalreimbursement_reason = models.CharField(max_length=255, verbose_name='Reason',blank=True, null=True)
    type_of_claim = models.CharField(max_length=255, verbose_name='Type of Medical Claim',blank=True, null=True)
    amount_aed = models.DecimalField(max_digits=10, decimal_places=2,default=True,null=True, verbose_name='Amount (AED)')
    medicalReimbursement_comments = models.TextField(blank=True, null=True, verbose_name='Comments')
    medicalReimbursement_status = models.CharField(max_length=20,blank=True, null=True)
    medicalReimbursement_applied_date = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Date')
  

    #Attendence Models
    date_of_exception = models.DateField(default=True,null=True)
    hours_late_in = models.IntegerField(default=True,null=True)
    minutes_late_in = models.IntegerField(default=True,null=True)
    hours_early_out = models.IntegerField(default=True,null=True)
    minutes_early_out = models.IntegerField(default=True,null=True)
    attendanceException_reason = models.CharField(max_length=255,default=True,null=True, verbose_name='Reason')
    attendanceException_status = models.CharField(max_length=20,  blank=True)
    reason_category = models.CharField(max_length=200, blank=True)
    attendanceExceptionApplied_date = models.DateField(auto_now_add=True, blank=True, null=True)

    #Document For Visa Models
    Visacountry_name = models.CharField(max_length=100,  blank=True, null=True)
    Visadocument_type = models.CharField(max_length=100, blank=True, null=True)
    Visacategory = models.CharField(max_length=100, blank=True, null=True)
    Visasub_category = models.CharField(max_length=100, blank=True, null=True)
    Visadocument_number = models.CharField(max_length=100, blank=True, null=True)
    Visaissued_by = models.CharField(max_length=100, blank=True, null=True)
    Visaissued_at = models.CharField(max_length=100, blank=True, null=True)
    Visaissued_date = models.DateField(blank=True, null=True)
    Visaissuing_authority = models.CharField(max_length=100, blank=True, null=True)
    Visavalid_from = models.DateField(blank=True, null=True)
    Visavalid_to = models.DateField(blank=True, null=True)
    Visaverified_by = models.CharField(max_length=100, blank=True, null=True)
    Visaverified_date = models.DateField(blank=True, null=True)
    #Additional Information For VISA
    visa_number = models.CharField(max_length=100, blank=True, null=True)
    visa_type = models.CharField(max_length=100,blank=True, null=True)
    sponsor_type = models.CharField(max_length=100, blank=True, null=True)
    sponsor_name = models.CharField(max_length=100, blank=True, null=True)
    sponsor_relationship = models.CharField(max_length=100, blank=True, null=True)
    sponsor_number = models.CharField(max_length=100, blank=True, null=True)
    sponsor_nationality = models.CharField(max_length=100, blank=True, null=True)
    emirate = models.CharField(max_length=100, blank=True, null=True)
    documentforvisa_status = models.CharField(max_length=20,blank=True)
    documentforvisaApplie_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    #Document For Passport
    Passport_country_name = models.CharField(max_length=100, blank=True, null=True)
    Passport_document_type = models.CharField(max_length=100, blank=True, null=True)
    Passport_category = models.CharField(max_length=100, blank=True, null=True)
    Passport_sub_category = models.CharField(max_length=100, blank=True, null=True)
    Passport_document_number = models.CharField(max_length=100, blank=True, null=True)
    Passport_issued_by = models.CharField(max_length=100, blank=True, null=True)
    Passport_issued_at = models.CharField(max_length=100, blank=True, null=True)
    Passport_issued_date = models.DateField(blank=True, null=True)
    Passport_issuing_authority = models.CharField(max_length=100, blank=True, null=True)
    Passport_valid_from = models.DateField(blank=True, null=True)
    Passport_valid_to = models.DateField(blank=True, null=True)
    Passport_verified_by = models.CharField(max_length=100, blank=True, null=True)
    Passport_verified_date = models.DateField(blank=True, null=True)
    #Additional Information For Passport
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_type = models.CharField(max_length=100, blank=True, null=True)
    country_of_issue = models.CharField(max_length=100, blank=True, null=True)
    place_of_issue = models.CharField(max_length=100, blank=True, null=True)
    number_of_accompanying_person = models.CharField(max_length=100, blank=True, null=True)
    previous_passport_number = models.CharField(max_length=100, blank=True, null=True)
    documentforpassport_status = models.CharField(max_length=20,blank=True)
    documentforpassportApplied_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    #EXTRA INFORMATION FOR LABOURCARD
    LabourCardcountry_name = models.CharField(max_length=100,  blank=True, null=True)
    LabourCarddocument_type = models.CharField(max_length=100, blank=True, null=True)
    LabourCardcategory = models.CharField(max_length=100, blank=True, null=True)
    LabourCardsub_category = models.CharField(max_length=100, blank=True, null=True)
    LabourCarddocument_number = models.CharField(max_length=100, blank=True, null=True)
    LabourCardissued_by = models.CharField(max_length=100, blank=True, null=True)
    LabourCardissued_at = models.CharField(max_length=100, blank=True, null=True)
    LabourCardissued_date = models.DateField(blank=True, null=True)
    LabourCardissuing_authority = models.CharField(max_length=100, blank=True, null=True)
    LabourCardvalid_from = models.DateField(blank=True, null=True)
    LabourCardvalid_to = models.DateField(blank=True, null=True)
    LabourCardverified_by = models.CharField(max_length=100, blank=True, null=True)
    LabourCardverified_date = models.DateField(blank=True, null=True)
    #Additional Information For LabourCard
    aly_personal_id_number = models.CharField(max_length=100, blank=True, null=True)
    aly_work_permit_number = models.CharField(max_length=100, blank=True, null=True)
    aly_place_of_issue = models.CharField(max_length=100, blank=True, null=True)
    documentForlabourcard_status = models.CharField(max_length=20,blank=True)
    documentForlabourcardApplied_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    #EmployeeResumption Models
    enter_date = models.DateField(blank=True, null=True)
    resumption_Status = models.CharField(max_length=100, blank=True)
    other = models.CharField(max_length=100, blank=True, null=True)
    days_overstayed = models.PositiveIntegerField(default=0)
    resumption_comment = models.CharField(max_length=100, blank=True, null=True)
    resumption_status=models.CharField(max_length=200, blank=True, null=True)
    resumptionApplied_date = models.DateField(auto_now_add=True, blank=True, null=True)


    #Bank Models
    bank_name = models.CharField(max_length=100,default=True,null=True)
    branch = models.CharField(max_length=100,default=True,blank=True,null=True)
    iban_number = models.CharField(max_length=100,default=True,blank=True,null=True)
    
    Bankstart_date = models.DateField(default=True,blank=True,null=True)
    bank_code = models.CharField(max_length=50,default=True,blank=True,null=True)
    bankaccount_comment = models.CharField(default=True,blank=True,null=True)
    bankaccount_status = models.CharField(max_length=10,  default='Pending')
    bankaccount_applied_date =  models.DateField(auto_now_add=True, blank=True, null=True)

    #EmployeeTravel Models
    request_type = models.CharField(max_length=100,blank=True, null=True )
    purpose_of_visit = models.CharField(max_length=20, blank=True, null=True)
    travel_start_date = models.DateField(blank=True, null=True)
    travel_end_date = models.DateField(blank=True, null=True)
    country_of_travel = models.CharField(max_length=100, blank=True, null=True)
    entity_company_traveling_for = models.CharField(max_length=200,blank=True, null=True)
    advance_amount_required = models.CharField(default=False,blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    visa_to_be_processed = models.CharField(max_length=3, blank=True, null=True)
    book_hotel_accommodation = models.CharField(max_length=3, blank=True, null=True)
    flight_ticket_required = models.CharField( default=False,blank=True, null=True)
    visa_letter_required = models.CharField( default=False,blank=True, null=True)
    employeetravel_comments = models.CharField(max_length=500, blank=True, null=True)
    employeetravel_status = models.CharField(max_length=20,blank=True,null=True)
    employeetravel_applied_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)


       

    def _str_(self):
        return f"MasterTable Entry: {self.emp_id}"


class visitingCard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    
    master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
    username = models.CharField(max_length=100,default=True,blank=True,null=True)
    mobilenum = models.CharField(max_length=50,default=True,blank=True,null=True)
    email = models.EmailField(default=True,blank=True,null=True)
    poBox = models.CharField(max_length=100,default=True,blank=True,null=True)
    unitedstate = models.CharField(max_length=100,default=True,blank=True,null=True)
    designation = models.CharField(max_length=100,default=True,blank=True,null=True)
    Visitingcountry = models.CharField(max_length=100,default=True,blank=True,null=True)
    telphone = models.CharField(max_length=100,default=True,blank=True,null=True)
    extnum = models.CharField(max_length=100,default=True,blank=True,null=True)
    faxnum = models.CharField(max_length=100,default=True,blank=True,null=True)
    def _str_(self):
        return f"{self.username}'s visiting card"


class AttendanceStatus(Enum):
    CHECKIN = "Check-in"
    MISSPUNCH = "Miss-punch"
    CHECKOUT="Check-out"

class userAttendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    chk_date = models.DateField(null=True, blank=True)
    userattendance_status = models.CharField(max_length=50, null=True, blank=True)  # Add max_length
    total_hours = models.CharField(max_length=50, blank=True, null=True, default='')  # Provide default value
    working_hours = models.CharField(max_length=50, blank=True, null=True, default='')  # Provide default value

    def save(self, *args, **kwargs):
        # if self.check_in and not self.check_out:
        #     self.status = AttendanceStatus.CHECKIN.value
        if self.check_in and self.check_out:
            self.status = AttendanceStatus.CHECKOUT.value
        super().save(*args, **kwargs)
        
        
    class Meta:
        verbose_name = "User Daily Attendance"
        verbose_name_plural = "User Daily Attendance"
        
class DaywiseStatus(Enum):
    PENDING = "Pending"
    PRESENT = "Present"
    ABSENT = "Absent"      
        
class daywiseAttendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True) 
    username=models.CharField(max_length=200,blank=True)
    timeShortageExceed=models.CharField(max_length=200,blank=True)
    total_hours = models.CharField(max_length=50, blank=True, null=True, default='') 
    chk_date = models.DateField(null=True, blank=True) 
    def update_status(self):
        if self.check_in:
            self.status = DaywiseStatus.PRESENT.value
        else:
            self.status = DaywiseStatus.ABSENT.value
        super().save()
        
    class Meta:
        verbose_name = "Daywise Attedance"
        verbose_name_plural = "Daywise Attendance" 

class Log(models.Model):
    Profile=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    photo=models.ImageField(upload_to="logs")
    is_correct=models.BooleanField(default=False)
    
    def _str_(self):
        return f"Log of {self.profile.id}"
    
    
class DetectedFaces(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='detected_faces', on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='profile_images/')
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    
    features = models.BinaryField(null=True,blank=True)  # Field to store facial features as binary data

    def save_features(self, features):
        self.features = features
        self.save()
        
    class Meta:
        verbose_name = "Detected Faces"
        verbose_name_plural = "Detected Faces"
        
class EmployeeList(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField()
    customer_status = (('active', 'active',),('inactive','inactive'))
    status = models.CharField(max_length=50,choices=customer_status,default='active')
    
    def _str_(self):
        return self.name
    
    class Meta:
        verbose_name = "Employee List"
        verbose_name_plural = "Employee List"



class EmailLog(models.Model):
    subject = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.subject


class LeaveApplication(models.Model):
    LEAVE_TYPES = (
        ('casual', 'Casual Leave'),
        ('sick', 'Sick Leave'),
        ('excuse', 'Excuse Leave'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    username = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    leaveapplication_reason = models.TextField()
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES, null=True, blank=True)
    leaveapplication_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    leaveapplication_applied_date = models.DateTimeField(default=timezone.now)

    def str(self):
        return f"{self.username}'s {self.get_leave_type_display()} Application ({self.status})"


class MedicalReimbursement(models.Model):
    CLAIM_TYPES = [
        ('Normal', 'Normal Medical Fees'),
        ('Urgent', 'Urgent Medical Fees'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
    username = models.CharField(max_length=255, verbose_name='Employee Name')
    emp_id = models.CharField(max_length=10, verbose_name='Employee Id')
    email = models.EmailField(verbose_name='Email Address')
    group = models.CharField(max_length=255, verbose_name='Business Group')
    department = models.CharField(max_length=255, verbose_name='Department')
    medicalreimbursement_reason = models.CharField(max_length=255, verbose_name='Reason', choices=CLAIM_TYPES)
    type_of_claim = models.CharField(max_length=255, verbose_name='Type of Medical Claim')
    amount_aed = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount (AED)')
    medicalReimbursement_comments = models.TextField(blank=True, verbose_name='Comments')
    medicalReimbursement_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
    medicalReimbursement_applied_date = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Date')

    attachments = models.ManyToManyField('Attachment', related_name='medical_reimbursements', blank=True, verbose_name='Attachments')

    def str(self):
        return f"Medical Reimbursement Request - {self.MedicalReimbursement_reason} - {self.username}"

class Attachment(models.Model):
    file = models.FileField(upload_to='medical_reimbursement_attachments/')


   
class LabourContract(models.Model):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
    emp_id = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200,blank=True, null=True)
    department = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    group = models.CharField(max_length=100, blank=True, null=True)
    labourcontract_reason = models.CharField(max_length=100, blank=True, null=True,choices=[
        ("Name Change","Name Change"),
        ("Position Change","Position Change"),
        ("Position and Salary Change","Position and Salary Change"),
        
        ("Salary Change","Salary Change")
        ],)
    amendment_date = models.DateField(blank=True, null=True)
    labourContract_comments = models.CharField(max_length=500, blank=True, null=True)
    labourContract_status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True)
    labourContract_applied_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def str(self):
        return f"{self.user.username}'s LabourContract"
    
    
class EmployeeReimbursement(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    
    master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
    username = models.CharField(max_length=200)
    emp_id = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    group = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    
    enter_amount = models.DecimalField(max_digits=10, decimal_places=2)
    note=models.CharField(max_length=300,blank=True,null=True,choices=[("Supporting bills should be scanned and attached in request form, originals should be submitted in HRD.Any claims without receipts will not be paid","Supporting bills should be scanned and attached in request form, originals should be submitted in HRD.Any claims without receipts will not be paid")])
    employeereimbursement_comment = models.CharField(max_length=100,blank=True,null=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    REIMBURSEMENT_CHOICES = [
        ('Air Passage Recruitment', 'Air Passage Recruitment'),
        ('Airticket Reimbursement', 'Airticket Reimbursement'),
        ('Examination Reimbursement', 'Examination Reimbursement'),
        ('Food Reimbursement', 'Food Reimbursement'),
        ('Insurance Claim', 'Insurance Claim'),
        ('Medical Fee Recruitment', 'Medical Fee Recruitment'),
        ('Parking Fees', 'Parking Fees'),
        ('Petrol Charges', 'Petrol Charges'),
        ('Postal Charges', 'Postal Charges'),
        ('Salik Fee', 'Salik Fee'),
        ('School Fees', 'School Fees'),
        ('Telephone Bill Claim', 'Telephone Bill Claim'),
        ('Transportation Fee', 'Transportation Fee'),
        ('Vehicle Repair Charges', 'Vehicle Repair Charges'),
        ('Vehicle related reimbursement', 'Vehicle related reimbursement'),
    ]

    reimbursement_type = models.CharField(max_length=300,choices=REIMBURSEMENT_CHOICES)
    employeereimbursement_status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True)
    employeereimbursement_applied_date = models.DateField(auto_now_add=True,blank=True,null=True)

    def _str_(self):
        return f"{self.username} - {self.reimbursement_type} - {self.Emp_Id}"


class BusinessTrip(models.Model):

    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    NAME_CHOICES = [
        ('Abdul Wahed Asad Hassan Abdulla', 'Abdul Wahed Asad Hassan Abdulla'),
        ('Abid Moosa Ali', 'Abid Moosa Ali'),
        ('Adham Fuddah Hakam Hakam', 'Adham Fuddah Hakam Hakam'),
        ('Ahammed Noufal Muhammed Kunhi', 'Ahammed Noufal Muhammed Kunhi'),
        ('Anil Kumar Paliekkara', 'Anil Kumar Paliekkara'),
        ('Diaa Aldeen Kamel Mohd Sadaqa', 'Diaa Aldeen Kamel Mohd Sadaqa'),
        ('Dileep Purushothaman Sri Kala Purushothaman', 'Dileep Purushothaman Sri Kala Purushothaman'),
        ('Elshafie Abdelbaset Abdelsalam Mohamed Youssef', 'Elshafie Abdelbaset Abdelsalam Mohamed Youssef'),
        ('Hardip Singh Gurnam Singh', 'Hardip Singh Gurnam Singh'),
        ('Hasen Mohamed Samsudeen', 'Hasen Mohamed Samsudeen'),
        ('Isarafil Nadaf', 'Isarafil Nadaf'),
        ('Jabir Ali', 'Jabir Ali'),
        ('Jashim Uddin', 'Jashim Uddin'),
        ('Mohammad Shakeer Noor Nayak Mohammad Haneef Noor Nayak', 'Mohammad Shakeer Noor Nayak Mohammad Haneef Noor Nayak'),
        ('Sandhya Akella Akella Somappa Somayajulu', 'Sandhya Akella Akella Somappa Somayajulu'),
        ('Sumitra Adhikari Ghimire', 'Sumitra Adhikari Ghimire'),
        ('Syed Ali Abbas Rizvi Syed Nusrat Ali Rizvi', 'Syed Ali Abbas Rizvi Syed Nusrat Ali Rizvi'),
    ]
    
    COUNTRY_CHOICES = [
        ('Afghanistan', 'Afghanistan'),
        ('Algeria', 'Algeria'),
        ('Bahrain', 'Bahrain'),
        ('Bangladesh', 'Bangladesh'),
        ('Bhutan', 'Bhutan'),
        ('Burma Union Myanmar', 'Burma Union Myanmar'),
        ('China', 'China'),
        ('Djibouti', 'Djibouti'),
        ('Egypt', 'Egypt'),
        ('Hong Kong', 'Hong Kong'),
        ('India', 'India'),
        ('Indonesia', 'Indonesia'),
        ('Iran', 'Iran'),
        ('Iraq', 'Iraq'),
        ('Japan', 'Japan'),
        ('Jordan', 'Jordan'),
        ('Kampuchea', 'Kampuchea'),
        ('Kuwait', 'Kuwait'),
        ('Lebanon', 'Lebanon'),
        ('Libya', 'Libya'),
        ('Malaysia', 'Malaysia'),
        ('Mauritania', 'Mauritania'),
        ('Morocco', 'Morocco'),
        ('Nepal', 'Nepal'),
        ('North Korea', 'North Korea'),
        ('Pakistan', 'Pakistan'),
        ('Palestine', 'Palestine'),
        ('Philippines', 'Philippines'),
        ('Qatar', 'Qatar'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Singapore', 'Singapore'),
        ('Somalia', 'Somalia'),
        ('South Korea', 'South Korea'),
        ('Sri Lanka', 'Sri Lanka'),
        ('Sudan', 'Sudan'),
        ('Sultanate Of Oman', 'Sultanate Of Oman'),
        ('Syria', 'Syria'),
        ('Taiwan', 'Taiwan'),
        ('Thailand', 'Thailand'),
        ('Tunisia', 'Tunisia'),
        ('United Arab Emirates', 'United Arab Emirates'),
        ('Vietnam', 'Vietnam'),
        ('Yemen', 'Yemen'),
    ]
    
    PAYMENT_CHOICES = [
        ('Cash', 'Cash'),
        ('Salary Deduction', 'Salary Deduction'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    
    master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
    emp_id = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200,blank=True, null=True)
    department = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    group = models.CharField(max_length=100, blank=True, null=True)
    
    employee_name=models.CharField(max_length=200, blank=True, null=True,choices=NAME_CHOICES)
    
    country_travel_to = models.CharField(max_length=200,choices=COUNTRY_CHOICES)
    
    businesstrip_reason = models.TextField(max_length=100, blank=True, null=True,)
    choices=[("Business Trip Other Expenses","Business Trip Other Expenses")]
    reimbursement_amount = models.FloatField()
    travel_request = models.CharField(max_length=100)
    mode_of_payment = models.CharField(max_length=100,choices=PAYMENT_CHOICES)
    amount_to_be_paid_back = models.FloatField()
    effective_date = models.DateField()
    businessTrip_comments = models.TextField(blank=True)
    businessTrip_status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True)
    businessTrip_applied_date=models.DateField(auto_now_add=True,blank=True,null=True)

    def _str_(self):
        return f"{self.user.username}'s BusinessTrip"
    
    
class Leaves(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
    username = models.CharField(max_length=255)
    emp_id = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=255)
    group = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    replaced_by = models.CharField(max_length=200, blank=True, null=True)
    leave_reason = models.CharField(max_length=50, default=True, null=True, choices=[
        ("1 Hour Exam Paper", "1 Hour Exam Paper"),
        ("2 Hour Exam Paper", "2 Hour Exam Paper"),
        ("3 Hour Exam Paper", "3 Hour Exam Paper"),
        ("Accident", "Accident"),
        ("Accomodation Shifting", "Accomodation Shifting"),
        ("Annual Leave Extension", "Annual Leave Extension"),
        ("Annual Vacation", "Annual Vacation"),
        ("Funeral", "Funeral"),
        ("Hajj", "Hajj"),
        ("Hospitalized", "Hospitalized"),
        ("Others", "Others"),
        ("Rest / Break", "Rest / Break"),
        ("Umrah", "Umrah"),
        ("Work Stress", "Work Stress"),
    ])
    leave_type = models.CharField(max_length=50, choices=[
        ("Annual Leave", "Annual Leave"),
        ("Sick Leave", "Sick Leave"),
        ("Maternity Leave", "Maternity Leave"),
        ("Personal Leave", "Personal Leave"),
        ("UnPaid Leave", "UnPaid Leave"),
    ])
    category = models.CharField(max_length=50, choices=[
        ("Vacation", "Vacation"),
        ("Maternity", "Maternity"),
        ("Unpaid", "Unpaid"),
        ("Personal", "Personal"),
        ("Sickness", "Sickness"),
    ])
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    passport_withdrawal_date = models.CharField(max_length=50,null=True, blank=True)
    request_for_airticket = models.CharField(max_length=50, choices=[
        ("Book Airticket", "Book Airticket"),
        ("Not Aplicable", "Not Aplicable"),
        ("Reimburse Airticket", "Reimburse Airticket",)
    ], null=True, blank=True)
    leaves_comments = models.TextField(blank=True)
    leaves_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
    leave_balance = models.IntegerField(default=100)
    duration = models.IntegerField(default=0, null=True, blank=True)
    leaves_applied_date = models.DateField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            previous_leave = Leaves.objects.filter(
                emp_id=self.emp_id,
                leaves_status='approved'
            ).order_by('-end_date').first()

            if previous_leave:
                self.leave_balance = previous_leave.leave_balance

        if self.leaves_status == 'approved':
            self.duration = (self.end_date - self.start_date).days + 1

            previous_leave = Leaves.objects.filter(
                emp_id=self.emp_id,
                leave_type=self.leave_type,
                leaves_status='approved'
            ).exclude(pk=self.pk).order_by('-end_date').first()

            if previous_leave:
                self.leave_balance = previous_leave.leave_balance - self.duration
            else:
                self.leave_balance -= self.duration

            previous_leaves_count = Leaves.objects.filter(
                emp_id=self.emp_id,
                leaves_status='approved',
                leave_type=self.leave_type,
                start_date__lte=self.start_date,
                end_date__gte=self.end_date
            ).exclude(pk=self.pk).count()

            self.leave_balance -= previous_leaves_count

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.start_date} to {self.end_date}"
    
    
class EmployeeAttendanceException(models.Model):
    
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    
    master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
    username = models.CharField(max_length=255,default=True,null=True, verbose_name='Employee Name')
    emp_id = models.CharField(max_length=10,default=True,null=True)
    email = models.EmailField(default=True,null=True)
    group = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    date_of_exception = models.DateField(default=True,null=True)
    hours_late_in = models.IntegerField(default=True,null=True)
    minutes_late_in = models.IntegerField(default=True,null=True)
    hours_early_out = models.IntegerField(default=True,null=True)
    minutes_early_out = models.IntegerField(default=True,null=True)
    attendanceException_reason = models.CharField(max_length=255,default=True,null=True, verbose_name='Reason')

    REASON_CHOICES = [ 
        ('Arrived late night from vacation', 'Arrived late night from vacation'),
        ('Bank work', 'Bank work'),
        ('COMP OFF', 'COMP Off'),
        ('Doctor Appointment', 'Doctor Appointment'),
        ('Due to Doctor Visit Self', 'Due to Doctor Visit Self'),
        ('Due to Doctor Visit with Family', 'Due to Doctor Visit with Family'),
        ('Due to annual leave', 'Due to annual leave'),
        ('Due to delay Metro', 'Due to delay Metro'),
        ('Due to headache' ,'Due to headache'),
        ('Due to personal work', 'Due to personal work'),
        ('Forget to Punch in','Forget to Punch in'),
        ('Forgot to Punch out','Forgot to Punch out'),
        ('Missed Punch In','Missed Punch In'),
        ('Missed Punch Out','Missed Punch Out'),
        ('Not well so late to office','Not well so late to office'),
        ('On Customer Site','On Customer Site'),
        ('On Siite','On Siite'),
        ('Others','Others'),
        ('Traffic','Traffic'),
        ('Went to kid school','Went to kid school'),
        ('Worked extra hours', 'Worked extra hours')

    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    attendanceException_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
    reason_category = models.CharField(max_length=200, choices=REASON_CHOICES,default=True,null=True)
    attendanceExceptionApplied_date = models.DateField(auto_now_add=True, blank=True, null=True)

    def str(self):
        return f"{self.Emp_Id} - {self.date_of_exception}"


class DocumentForVisa(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    DOCUMENT_TYPE =[
        ('AE_VISA','AE_VISA')
    ]

    COUNTRY_CHOICES = [
        ('Afghanistan', 'Afghanistan'),
        ('Algeria', 'Algeria'),
        ('Bahrain', 'Bahrain'),
        ('Bangladesh', 'Bangladesh'),
        ('Bhutan', 'Bhutan'),
        ('Burma Union Myanmar', 'Burma Union Myanmar'),
        ('China', 'China'),
        ('Djibouti', 'Djibouti'),
        ('Egypt', 'Egypt'),
        ('Hong Kong', 'Hong Kong'),
        ('India', 'India'),
        ('Indonesia', 'Indonesia'),
        ('Iran', 'Iran'),
        ('Iraq', 'Iraq'),
        ('Japan', 'Japan'),
        ('Jordan', 'Jordan'),
        ('Kampuchea', 'Kampuchea'),
        ('Kuwait', 'Kuwait'),
        ('Lebanon', 'Lebanon'),
        ('Libya', 'Libya'),
        ('Malaysia', 'Malaysia'),
        ('Mauritania', 'Mauritania'),
        ('Morocco', 'Morocco'),
        ('Nepal', 'Nepal'),
        ('North Korea', 'North Korea'),
        ('Pakistan', 'Pakistan'),
        ('Palestine', 'Palestine'),
        ('Philippines', 'Philippines'),
        ('Qatar', 'Qatar'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Singapore', 'Singapore'),
        ('Somalia', 'Somalia'),
        ('South Korea', 'South Korea'),
        ('Sri Lanka', 'Sri Lanka'),
        ('Sudan', 'Sudan'),
        ('Sultanate Of Oman', 'Sultanate Of Oman'),
        ('Syria', 'Syria'),
        ('Taiwan', 'Taiwan'),
        ('Thailand', 'Thailand'),
        ('Tunisia', 'Tunisia'),
        ('United Arab Emirates', 'United Arab Emirates'),
        ('Vietnam', 'Vietnam'),
        ('Yemen', 'Yemen'),
    ]

    VISA_TYPE_CHOICES = [
        ('Family Visa', 'Family Visa'),
        ('Residence Permit', 'Residence Permit'),
        ('Visit Visa', 'Visit Visa'),
    ]

    SPONSOR_TYPE_CHOICES = [
        ('Company Sponsored', 'Company Sponsored'),
        ('Family Sponsored', 'Family Sponsored'),
    ]
    VISA_TYPE_CHOICES = [
        ('Family Visa', 'Family Visa'),
        ('Residence Permit', 'Residence Permit'),
        ('Visit Visa', 'Visit Visa'),
    ]

    SPONSOR_NAME_CHOICES = [
        ('A Y C O BUILDING BR OF AL YOUSUF LLC', 'A Y C O BUILDING BR OF AL YOUSUF LLC'),
        ('AL YOUSUF ELEVATORS & ESCALATORS-BR-AL YOUSUF LLC', 'AL YOUSUF ELEVATORS & ESCALATORS-BR-AL YOUSUF LLC'),
        ('AL YOUSUF MEDICAL CENTER L.L.C.', 'AL YOUSUF MEDICAL CENTER L.L.C.'),
        ('AL YOUSUF PHARMACY L.L.C.', 'AL YOUSUF PHARMACY L.L.C.'),
        ('AL YOUSUF PROPERTY BR OF AL YOUSUF LLC', 'AL YOUSUF PROPERTY BR OF AL YOUSUF LLC'),
        ('AL YOUSUF ROBOTICS L.L.C.', 'AL YOUSUF ROBOTICS L.L.C.'),
        ('ALYOUSUF MEDICAL PROJECT CONTRACTING SOLUTIONS L.L.C.', 'ALYOUSUF MEDICAL PROJECT CONTRACTING SOLUTIONS L.L.C.'),
        ('AUTOSPORT (L.L.C.)', 'AUTOSPORT (L.L.C.)'),
        ('Advantage Limousine LLC', 'Advantage Limousine LLC'),
        ('Advantage Limousine-Dubai', 'Advantage Limousine-Dubai'),
        ('Advantage Taxi LLC', 'Advantage Taxi LLC'),
        ('Al Yousuf Agricultural and Landscaping LLC', 'Al Yousuf Agricultural and Landscaping LLC'),
        ('Al Yousuf Computer & Telecommunications (L.L.C.)', 'Al Yousuf Computer & Telecommunications (L.L.C.)'),
        ('Al Yousuf Computers & Telecommunications Abu Dhabi', 'Al Yousuf Computers & Telecommunications Abu Dhabi'),
        ('Al Yousuf Electronics LLC', 'Al Yousuf Electronics LLC'),
        ('Al Yousuf Electronics LLC - Abu Dhabi', 'Al Yousuf Electronics LLC - Abu Dhabi'),
        ('Al Yousuf International Construction LLC', 'Al Yousuf International Construction LLC'),
        ('Al Yousuf LLC', 'Al Yousuf LLC'),
        ('Al Yousuf LLC - Abu Dhabi', 'Al Yousuf LLC - Abu Dhabi'),
        ('Al Yousuf Motors LLC', 'Al Yousuf Motors LLC'),
        ('Al Yousuf Motors LLC - Abu Dhabi', 'Al Yousuf Motors LLC - Abu Dhabi'),
        ('Al Yousuf Real Estate LLC', 'Al Yousuf Real Estate LLC'),
        ('Al Yousuf Security Controls and Alarms LLC', 'Al Yousuf Security Controls and Alarms LLC'),
        ('Al Yousuf Sports Equipment LLC', 'Al Yousuf Sports Equipment LLC'),
        ('Al Yousuf Sports Equipment LLC - Abu Dhabi', 'Al Yousuf Sports Equipment LLC - Abu Dhabi'),
        ('Alyousuf Technical Solutions L.L.C.', 'Alyousuf Technical Solutions L.L.C.'),
        ('BIG BLUE MARINE EQUIPMENTS LLC', 'BIG BLUE MARINE EQUIPMENTS LLC'),
        ('Back on Track LLC', 'Back on Track LLC'),
        ('Delux Limousine LLC', 'Delux Limousine LLC'),
        ('Fujitech Co Ltd Dubai BR', 'Fujitech Co Ltd Dubai BR'),
        ('Future Technology (L.L.C.)', 'Future Technology (L.L.C.)'),
        ('Future Technology - LLC - Abu Dhabi', 'Future Technology - LLC - Abu Dhabi'),
        ('Imperbit Menmbrane Industries LLC', 'Imperbit Menmbrane Industries LLC'),
        ('Jebel Ali Free Zone', 'Jebel Ali Free Zone'),
        ('Nipon Kaiji Kyokai Dubai', 'Nipon Kaiji Kyokai Dubai'),
        ('Others', 'Others'),
        ('Sharjah Airport', 'Sharjah Airport'),
        ('Yamaha Motors Company', 'Yamaha Motors Company'),
    ]

    SPONSOR_RELATIONSHIP_CHOICES = [
        ('Brother', 'Brother'),
        ('Daughter', 'Daughter'),
        ('Father', 'Father'),
        ('Husband', 'Husband'),
        ('Mom Husband', 'Mom Husband'),
        ('Mother', 'Mother'),
        ('Not Related', 'Not Related'),
        ('Sister', 'Sister'),
        ('Son', 'Son'),
        ('Wife', 'Wife'),
    ]

    SPONSOR_NATIONALITY_CHOICES = [
        ('Afghanistan', 'Afghanistan'),
        ('Aland Islands', 'Aland Islands'),
        ('Albania', 'Albania'),
        ('Algeria', 'Algeria'),
        ('American Samoa', 'American Samoa'),
        ('Andorra', 'Andorra'),
        ('Angola', 'Angola'),
        ('Anguilla', 'Anguilla'),
        ('Antarctica', 'Antarctica'),
        ('Antigua', 'Antigua'),
        ('Antigua and Barbuda', 'Antigua and Barbuda'),
        ('Argentina', 'Argentina'),
        ('Armenia', 'Armenia'),
        ('Aruba', 'Aruba'),
        ('Australia', 'Australia'),
        ('Austria', 'Austria'),
        ('Azerbaijan', 'Azerbaijan'),
        ('Bahamas', 'Bahamas'),
        ('Bahrain', 'Bahrain'),
        ('Bangladesh', 'Bangladesh'),
        ('Barbados', 'Barbados'),
        ('Belgium', 'Belgium'),
        ('Belize', 'Belize'),
        ('Benin', 'Benin'),
        ('Bermuda', 'Bermuda'),
        ('Bhutan', 'Bhutan'),
        ('Bolivia', 'Bolivia'),
        ('Bosnia And Herzegovina', 'Bosnia And Herzegovina'),
        ('Botswana', 'Botswana'),
        ('Bouvet Island', 'Bouvet Island'),
        ('Brazil', 'Brazil'),
        ('British Indian Ocean Territory', 'British Indian Ocean Territory'),
        ('Brunei', 'Brunei'),
        ('Bulgaria', 'Bulgaria'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Burma Union Myanmar', 'Burma Union Myanmar'),
        ('Burundi', 'Burundi'),
        ('Cambodia', 'Cambodia'),
        ('Cameroon', 'Cameroon'),
        ('Canada', 'Canada'),
        ('Cape Verde', 'Cape Verde'),
        ('Cayman Island', 'Cayman Island'),
        ('Central Africa Republic', 'Central Africa Republic'),
        ('Chad', 'Chad'),
        ('Chile', 'Chile'),
        ('China', 'China'),
        ('Christmas Island', 'Christmas Island'),
        ('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands'),
        ('Colombia', 'Colombia'),
        ('Commonwealth of Dominica', 'Commonwealth of Dominica'),
        ('Comoros', 'Comoros'),
        ('Congo', 'Congo'),
        ('Cook Islands', 'Cook Islands'),
        ('Costa Rica', 'Costa Rica'),
        ("Cote d'Ivoire'", "Cote d'Ivoire'"),
        ('Croatia', 'Croatia'),
        ('Cuba', 'Cuba'),
        ('Cyprus', 'Cyprus'),
        ('Czech', 'Czech'),
        ('Czechoslovakia', 'Czechoslovakia'),
        ('Dagestan', 'Dagestan'),
        ('Dahomey', 'Dahomey'),
        ('Denmark', 'Denmark'),
        ('Djibouti', 'Djibouti'),
        ('Dominican', 'Dominican'),
        ('East Timor', 'East Timor'),
        ('Ecuador', 'Ecuador'),
        ('Egypt', 'Egypt'),
        ('El Salvador', 'El Salvador'),
        ('Eritrea', 'Eritrea'),
        ('Estonia', 'Estonia'),
        ('Ethiopia', 'Ethiopia'),
        ('Falkland Islands (Malvinas)', 'Falkland Islands (Malvinas)'),
        ('Faroe Islands', 'Faroe Islands'),
        ('Fiji', 'Fiji'),
        ('Finland', 'Finland'),
        ('France', 'France'),
        ('French Guiana', 'French Guiana'),
        ('French Polynesia', 'French Polynesia'),
        ('French Southern Territories', 'French Southern Territories'),
        ('Gabon', 'Gabon'),
        ('Gambia', 'Gambia'),
        ('Georgia', 'Georgia'),
        ('Germany', 'Germany'),
        ('Ghana', 'Ghana'),
        ('Gibraltar', 'Gibraltar'),
        ('Greece', 'Greece'),
        ('Greenland', 'Greenland'),
        ('Grenada', 'Grenada'),
        ('Guadeloupe', 'Guadeloupe'),
        ('Guam', 'Guam'),
        ('Guatemala', 'Guatemala'),
        ('Guernsey', 'Guernsey'),
        ('Guinea', 'Guinea'),
        ('Guinea-Bissau', 'Guinea-Bissau'),
        ('Guyana', 'Guyana'),
        ('Haiti', 'Haiti'),
        ('Heard Island and McDonald Islands', 'Heard Island and McDonald Islands'),
        ('Honduras', 'Honduras'),
        ('Hong Kong', 'Hong Kong'),
        ('Hungary', 'Hungary'),
        ('Iceland', 'Iceland'),
        ('India', 'India'),
        ('Indonesia', 'Indonesia'),
        ('Iran', 'Iran'),
        ('Iraq', 'Iraq'),
        ('Ireland', 'Ireland'),
        ('Isle of Man', 'Isle of Man'),
        ('Israel', 'Israel'),
        ('Italy', 'Italy'),
        ('Jamaica', 'Jamaica'),
        ('Japan', 'Japan'),
        ('Jersey', 'Jersey'),
        ('Jordan', 'Jordan'),
        ('Kampuchea', 'Kampuchea'),
        ('Kazakhstan', 'Kazakhstan'),
        ('Kenya', 'Kenya'),
        ('Kingston', 'Kingston'),
        ('Kiribati', 'Kiribati'),
        ('Kosovo', 'Kosovo'),
        ('Kuwait', 'Kuwait'),
        ('Kyrgyz', 'Kyrgyz'),
        ('Kyrgyz Republic', 'Kyrgyz Republic'),
        ('Kyrgyzstan', 'Kyrgyzstan'),
        ('Laos', 'Laos'),
        ('Latvia', 'Latvia'),
        ('Lebanon', 'Lebanon'),
        ('Lesotho', 'Lesotho'),
        ('Liberia', 'Liberia'),
        ('Libya', 'Libya'),
        ('Liechtenstein', 'Liechtenstein'),
        ('Lithuania', 'Lithuania'),
        ('Luxembourg', 'Luxembourg'),
        ('Macau', 'Macau'),
        ('Madagascar', 'Madagascar'),
        ('Magnolia', 'Magnolia'),
        ('Malawi', 'Malawi'),
        ('Malaysia', 'Malaysia'),
        ('Maldives', 'Maldives'),
        ('Mali', 'Mali'),
        ('Malta', 'Malta'),
        ('Marshall Island', 'Marshall Island'),
        ('Martinez Islands', 'Martinez Islands'),
        ('Martinique', 'Martinique'),
        ('Maryanne Island', 'Maryanne Island'),
        ('Mauritania', 'Mauritania'),
        ('Mauritius', 'Mauritius'),
        ('Mayotte', 'Mayotte'),
        ('Mexico', 'Mexico'),
        ('Micronesia', 'Micronesia'),
        ('Moldavia', 'Moldavia'),
        ('Monaco', 'Monaco'),
        ('Mongolia', 'Mongolia'),
        ('Montenegro', 'Montenegro'),
        ('Montserrat', 'Montserrat'),
        ('Morocco', 'Morocco'),
        ('Mozambique', 'Mozambique'),
        ('Namibia', 'Namibia'),
        ('Nauru', 'Nauru'),
        ('Nepal', 'Nepal'),
        ('Netherlands', 'Netherlands'),
        ('Netherlands Antilles', 'Netherlands Antilles'),
        ('Nevis', 'Nevis'),
        ('New Caledonia', 'New Caledonia'),
        ('New Guinea', 'New Guinea'),
        ('New Zealand', 'New Zealand'),
        ('Nicaragua', 'Nicaragua'),
        ('Niger', 'Niger'),
        ('Nigeria', 'Nigeria'),
        ('Niue', 'Niue'),
        ('Norfolk Island', 'Norfolk Island'),
        ('North Korea', 'North Korea'),
        ('Northern Mariana Islands', 'Northern Mariana Islands'),
        ('Norway', 'Norway'),
        ('Okinawa', 'Okinawa'),
        ('Other countries', 'Other countries'),
        ('Pakistan', 'Pakistan'),
        ('Palau', 'Palau'),
        ('Palestine', 'Palestine'),
        ('Panama', 'Panama'),
        ('Paraguay', 'Paraguay'),
        ('Peru', 'Peru'),
        ('Philippines', 'Philippines'),
        ('Poland', 'Poland'),
        ('Portugal', 'Portugal'),
        ('Puerto Rico', 'Puerto Rico'),
        ('Qatar', 'Qatar'),
        ('Republic Of Belarus', 'Republic Of Belarus'),
        ('Republic Of Guinea', 'Republic Of Guinea'),
        ('Republic Of Macedonia', 'Republic Of Macedonia'),
        ('Reunion', 'Reunion'),
        ('Romania', 'Romania'),
        ('Russia', 'Russia'),
        ('Rwanda', 'Rwanda'),
        ('Ryukyu Islands', 'Ryukyu Islands'),
        ('Saint Kitts And Nevis', 'Saint Kitts And Nevis'),
        ('Saint Lucia', 'Saint Lucia'),
        ('Saint Pierre and Miquelon', 'Saint Pierre and Miquelon'),
        ('Saint Vincent', 'Saint Vincent'),
        ('San Marino', 'San Marino'),
        ('Sao Tome', 'Sao Tome'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Senegal', 'Senegal'),
        ('Serbia', 'Serbia'),
        ('Seychelles', 'Seychelles'),
        ('Sierra Leone', 'Sierra Leone'),
        ('Singapore', 'Singapore'),
        ('Slovakia', 'Slovakia'),
        ('Slovenia', 'Slovenia'),
        ('Solomon Island', 'Solomon Island'),
        ('Somalia', 'Somalia'),
        ('South Africa', 'South Africa'),
        ('South Georgia and the South Sandwich Islands', 'South Georgia and the South Sandwich Islands'),
        ('South Korea', 'South Korea'),
        ('South Sudan', 'South Sudan'),
        ('Soviet Union', 'Soviet Union'),
        ('Spain', 'Spain'),
        ('Sri Lanka', 'Sri Lanka'),
        ('St Christopher', 'St Christopher'),
        ('St Helena', 'St Helena'),
        ('Sudan', 'Sudan'),
        ('Sultanate Of Oman', 'Sultanate Of Oman'),
        ('Suriname', 'Suriname'),
        ('Svalbard and Jan Mayen', 'Svalbard and Jan Mayen'),
        ('Swaziland', 'Swaziland'),
        ('Sweden', 'Sweden'),
        ('Switzerland', 'Switzerland'),
        ('Syria', 'Syria'),
        ('Tahiti', 'Tahiti'),
        ('Taiwan', 'Taiwan'),
        ('Tajikistan', 'Tajikistan'),
        ('Tanzania', 'Tanzania'),
        ('Tasmania', 'Tasmania'),
        ('Thailand', 'Thailand'),
        ('The Democratic Republic Of Congo', 'The Democratic Republic Of Congo'),
        ('The Hellenic Republic', 'The Hellenic Republic'),
        ('Timor', 'Timor'),
        ('Togo', 'Togo'),
        ('Tokelau', 'Tokelau'),
        ('Tonga', 'Tonga'),
        ('Tonga Islands', 'Tonga Islands'),
        ('Trinidad', 'Trinidad'),
        ('Tunisia', 'Tunisia'),
        ('Turkey', 'Turkey'),
        ('Turkmenistan', 'Turkmenistan'),
        ('Turks and Caicos Islands', 'Turks and Caicos Islands'),
        ('Tuvalu', 'Tuvalu'),
        ('U S A', 'U S A'),
        ('Uganda', 'Uganda'),
        ('Ukraine', 'Ukraine'),
        ('United Arab Emirates', 'United Arab Emirates'),
        ('United Kingdom', 'United Kingdom'),
        ('United States Minor Outlying Islands', 'United States Minor Outlying Islands'),
        ('Uruguay', 'Uruguay'),
        ('Uzbekistan', 'Uzbekistan'),
        ('Vanuatu', 'Vanuatu'),
        ('Vatican', 'Vatican'),
        ('Venezuela', 'Venezuela'),
        ('Vietnam', 'Vietnam'),
        ('Virgin Islands, British', 'Virgin Islands, British'),
        ('Vietnam', 'Vietnam'),
        ('Virgin Islands, British', 'Virgin Islands, British'),
        ('Virgin Islands, U.S.', 'Virgin Islands, U.S.'),
        ('Wallis and Futuna', 'Wallis and Futuna'),
        ('Western Sahara', 'Western Sahara'),
        ('Western Samoa', 'Western Samoa'),
        ('Yemen', 'Yemen'),
        ('Yugoslavia', 'Yugoslavia'),
        ('Zambia', 'Zambia'),
        ('Zimbabwe', 'Zimbabwe'),
        ]
    EMIRATE_CHOICES = [
    ('Abu Dhabi', 'Abu Dhabi'),
    ('Ajman', 'Ajman'),
    ('Al Ain', 'Al Ain'),
    ('Dubai', 'Dubai'),
    ('Fujairah', 'Fujairah'),
    ('Ras al-Khaimah', 'Ras al-Khaimah'),
    ('Sharjah', 'Sharjah'),
    ('Umm al-Qaiwain', 'Umm al-Qaiwain'),
    ]

    
    #DOCCMENT INFORMATION FOR ALL
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
    emp_id = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200,blank=True, null=True)
    department = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    group = models.CharField(max_length=100, blank=True, null=True)

    #EXTRA INFORMATION FOR VISA
    Visacountry_name = models.CharField(max_length=100,choices=COUNTRY_CHOICES,  blank=True, null=True)
    Visadocument_type = models.CharField(max_length=100,choices=DOCUMENT_TYPE, blank=True, null=True)
    Visacategory = models.CharField(max_length=100, blank=True, null=True)
    Visasub_category = models.CharField(max_length=100, blank=True, null=True)
    Visadocument_number = models.CharField(max_length=100, blank=True, null=True)
    Visaissued_by = models.CharField(max_length=100, blank=True, null=True)
    Visaissued_at = models.CharField(max_length=100, blank=True, null=True)
    Visaissued_date = models.DateField(blank=True, null=True)
    Visaissuing_authority = models.CharField(max_length=100, blank=True, null=True)
    Visavalid_from = models.DateField(blank=True, null=True)
    Visavalid_to = models.DateField(blank=True, null=True)
    Visaverified_by = models.CharField(max_length=100, blank=True, null=True)
    Visaverified_date = models.DateField(blank=True, null=True)
    
    #Additional Information For VISA
    visa_number = models.CharField(max_length=100, blank=True, null=True)
    visa_type = models.CharField(max_length=100,choices=VISA_TYPE_CHOICES ,blank=True, null=True)
    sponsor_type = models.CharField(max_length=100,choices=SPONSOR_TYPE_CHOICES, blank=True, null=True)
    sponsor_name = models.CharField(max_length=100,choices=SPONSOR_NAME_CHOICES, blank=True, null=True)
    sponsor_relationship = models.CharField(max_length=100,choices=SPONSOR_RELATIONSHIP_CHOICES, blank=True, null=True)
    sponsor_number = models.CharField(max_length=100, blank=True, null=True)
    sponsor_nationality = models.CharField(max_length=100,choices=SPONSOR_NATIONALITY_CHOICES, blank=True, null=True)
    emirate = models.CharField(max_length=100,choices=EMIRATE_CHOICES, blank=True, null=True)

    #For Status
    documentforvisa_status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True)
    
    #For applied date
    documentforvisaApplie_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
   

    def str(self):
        return f"{self.user.username}'s Document record of visa"
    

class DocumentForPassport(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    DOCUMENT_TYPE =[
        ('AE_PASSPORT','AE_PASSPORT')
    ]

    COUNTRY_CHOICES = [
        ('Afghanistan', 'Afghanistan'),
        ('Algeria', 'Algeria'),
        ('Bahrain', 'Bahrain'),
        ('Bangladesh', 'Bangladesh'),
        ('Bhutan', 'Bhutan'),
        ('Burma Union Myanmar', 'Burma Union Myanmar'),
        ('China', 'China'),
        ('Djibouti', 'Djibouti'),
        ('Egypt', 'Egypt'),
        ('Hong Kong', 'Hong Kong'),
        ('India', 'India'),
        ('Indonesia', 'Indonesia'),
        ('Iran', 'Iran'),
        ('Iraq', 'Iraq'),
        ('Japan', 'Japan'),
        ('Jordan', 'Jordan'),
        ('Kampuchea', 'Kampuchea'),
        ('Kuwait', 'Kuwait'),
        ('Lebanon', 'Lebanon'),
        ('Libya', 'Libya'),
        ('Malaysia', 'Malaysia'),
        ('Mauritania', 'Mauritania'),
        ('Morocco', 'Morocco'),
        ('Nepal', 'Nepal'),
        ('North Korea', 'North Korea'),
        ('Pakistan', 'Pakistan'),
        ('Palestine', 'Palestine'),
        ('Philippines', 'Philippines'),
        ('Qatar', 'Qatar'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Singapore', 'Singapore'),
        ('Somalia', 'Somalia'),
        ('South Korea', 'South Korea'),
        ('Sri Lanka', 'Sri Lanka'),
        ('Sudan', 'Sudan'),
        ('Sultanate Of Oman', 'Sultanate Of Oman'),
        ('Syria', 'Syria'),
        ('Taiwan', 'Taiwan'),
        ('Thailand', 'Thailand'),
        ('Tunisia', 'Tunisia'),
        ('United Arab Emirates', 'United Arab Emirates'),
        ('Vietnam', 'Vietnam'),
        ('Yemen', 'Yemen'),
    ]

    PASSPORT_TYPE_CHOICES = [
        ('Family Visa', 'Family Visa'),
        ('Residence Permit', 'Residence Permit'),
        ('Visit Visa', 'Visit Visa'),
    ]
    
    #DOCUMENT INFORMATION FOR ALL
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
    emp_id = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200,blank=True, null=True)
    department = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    group = models.CharField(max_length=100, blank=True, null=True)

    #EXTRA INFORMATION FOR PASSPORT
    Passport_country_name = models.CharField(max_length=100,choices=COUNTRY_CHOICES,  blank=True, null=True)
    Passport_document_type = models.CharField(max_length=100,choices=DOCUMENT_TYPE, blank=True, null=True)
    Passport_category = models.CharField(max_length=100, blank=True, null=True)
    Passport_sub_category = models.CharField(max_length=100, blank=True, null=True)
    Passport_document_number = models.CharField(max_length=100, blank=True, null=True)
    Passport_issued_by = models.CharField(max_length=100, blank=True, null=True)
    Passport_issued_at = models.CharField(max_length=100, blank=True, null=True)
    Passport_issued_date = models.DateField(blank=True, null=True)
    Passport_issuing_authority = models.CharField(max_length=100, blank=True, null=True)
    Passport_valid_from = models.DateField(blank=True, null=True)
    Passport_valid_to = models.DateField(blank=True, null=True)
    Passport_verified_by = models.CharField(max_length=100, blank=True, null=True)
    Passport_verified_date = models.DateField(blank=True, null=True)

    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_type = models.CharField(max_length=100,choices=PASSPORT_TYPE_CHOICES, blank=True, null=True)
    country_of_issue = models.CharField(max_length=100, blank=True, null=True)
    place_of_issue = models.CharField(max_length=100, blank=True, null=True)
    number_of_accompanying_person = models.CharField(max_length=100, blank=True, null=True)
    previous_passport_number = models.CharField(max_length=100, blank=True, null=True)


    #For Status
    documentforpassport_status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True)

    #For applied date
    documentforpassportApplied_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def str(self):
        return f"{self.user.username}'s Document record of Passport"



class DocumentForLabourCard(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]


    DOCUMENT_TYPE =[
        ('AE_LABOURCARD','AE_LABOURCARD')
    ]

    COUNTRY_CHOICES = [
        ('Afghanistan', 'Afghanistan'),
        ('Algeria', 'Algeria'),
        ('Bahrain', 'Bahrain'),
        ('Bangladesh', 'Bangladesh'),
        ('Bhutan', 'Bhutan'),
        ('Burma Union Myanmar', 'Burma Union Myanmar'),
        ('China', 'China'),
        ('Djibouti', 'Djibouti'),
        ('Egypt', 'Egypt'),
        ('Hong Kong', 'Hong Kong'),
        ('India', 'India'),
        ('Indonesia', 'Indonesia'),
        ('Iran', 'Iran'),
        ('Iraq', 'Iraq'),
        ('Japan', 'Japan'),
        ('Jordan', 'Jordan'),
        ('Kampuchea', 'Kampuchea'),
        ('Kuwait', 'Kuwait'),
        ('Lebanon', 'Lebanon'),
        ('Libya', 'Libya'),
        ('Malaysia', 'Malaysia'),
        ('Mauritania', 'Mauritania'),
        ('Morocco', 'Morocco'),
        ('Nepal', 'Nepal'),
        ('North Korea', 'North Korea'),
        ('Pakistan', 'Pakistan'),
        ('Palestine', 'Palestine'),
        ('Philippines', 'Philippines'),
        ('Qatar', 'Qatar'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Singapore', 'Singapore'),
        ('Somalia', 'Somalia'),
        ('South Korea', 'South Korea'),
        ('Sri Lanka', 'Sri Lanka'),
        ('Sudan', 'Sudan'),
        ('Sultanate Of Oman', 'Sultanate Of Oman'),
        ('Syria', 'Syria'),
        ('Taiwan', 'Taiwan'),
        ('Thailand', 'Thailand'),
        ('Tunisia', 'Tunisia'),
        ('United Arab Emirates', 'United Arab Emirates'),
        ('Vietnam', 'Vietnam'),
        ('Yemen', 'Yemen'),
    ]

    ALY_PLACE_OF_ISSUE = [
        ('Abu Dhabi ', 'Abu Dhabi'),
        ('Ajman', 'Ajman'),
        ('Al Ain', 'Al Ain'),
        ('Dubai', 'Dubai'),
        ('Fujairah', 'Fujairah'),
        ('Ras al-Khaimah', 'Ras al-Khaimah'),
        ('Sharjah', 'Sharjah'),
        ('Umm al-Qaiwain', 'Umm al-Qaiwain'),
    ]
    
    #DOCUMENT INFORMATION FOR ALL
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
    emp_id = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200,blank=True, null=True)
    department = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    group = models.CharField(max_length=100, blank=True, null=True)

    #EXTRA INFORMATION FOR LABOURCARD
    LabourCardcountry_name = models.CharField(max_length=100,choices=COUNTRY_CHOICES,  blank=True, null=True)
    LabourCarddocument_type = models.CharField(max_length=100,choices=DOCUMENT_TYPE, blank=True, null=True)
    LabourCardcategory = models.CharField(max_length=100, blank=True, null=True)
    LabourCardsub_category = models.CharField(max_length=100, blank=True, null=True)
    LabourCarddocument_number = models.CharField(max_length=100, blank=True, null=True)
    LabourCardissued_by = models.CharField(max_length=100, blank=True, null=True)
    LabourCardissued_at = models.CharField(max_length=100, blank=True, null=True)
    LabourCardissued_date = models.DateField(blank=True, null=True)
    LabourCardissuing_authority = models.CharField(max_length=100, blank=True, null=True)
    LabourCardvalid_from = models.DateField(blank=True, null=True)
    LabourCardvalid_to = models.DateField(blank=True, null=True)
    LabourCardverified_by = models.CharField(max_length=100, blank=True, null=True)
    LabourCardverified_date = models.DateField(blank=True, null=True)
    
    #Additional Information For Labour Card
    aly_personal_id_number = models.CharField(max_length=100, blank=True, null=True)
    aly_work_permit_number = models.CharField(max_length=100, blank=True, null=True)
    aly_place_of_issue = models.CharField(max_length=100,choices=ALY_PLACE_OF_ISSUE, blank=True, null=True)
    


    #For Status
    documentForlabourcard_status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True)
    documentForlabourcardApplied_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def str(self):
        return f"{self.user.username}'s Document record of Labour Card"
    

class EmployeeResumption(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    
    master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
    username = models.CharField(max_length=200)
    emp_id = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    group = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    # enter_date = models.DateField(auto_now_add=True, blank=True, null=True)
    enter_date = models.DateField(blank=True, null=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    RESUMPTION_STATUS = [
        ('Overstayed with prior intimation and separate leave application for extension of overstayed leave period is to be submitted', 'Overstayed with prior intimation and separate leave application for extension of overstayed leave period is to be submitted'),
        ('Overstayed without prior approval or intimation and is liable for termination', 'Overstayed without prior approval or intimation and is liable for termination'),
        ('Overstayed without prior approval/intimation', 'Overstayed without prior approval/intimation'),
        ('Reported for duty prior to expiry of leave', 'Reported for duty prior to expiry of leave'),
        ('Reported for duty without any overstay', 'Reported for duty without any overstay'),
        
    ]
    resumption_Status = models.CharField(max_length=100, choices=STATUS_CHOICES, blank=True)
    other = models.CharField(max_length=100, blank=True, null=True)
    days_overstayed = models.PositiveIntegerField(default=0)
    resumption_comment = models.CharField(max_length=100, blank=True, null=True)
    resumption_status=models.CharField(max_length=200,choices=RESUMPTION_STATUS, blank=True, null=True)
    resumptionApplied_date = models.DateField(auto_now_add=True, blank=True, null=True)

  

    def str(self):
        return f"{self.username} - {self.Emp_Id}"







class BankAccount(models.Model):
    
    BANK_CHOICES = [
        ('ALFA Exchange', 'ALFA Exchange'),
        ('ARBIFT', 'ARBIFT'),
        ('Abu Dhabi Commercial Bank', 'Abu Dhabi Commercial Bank'),
        ('Abu Dhabi Islamic Bank', 'Abu Dhabi Islamic Bank'),
        ('Ahmed Al Amery Exchange Est - Abu Dhabi', 'Ahmed Al Amery Exchange Est - Abu Dhabi'),
        ('Ahmed Al Hussain Exchange Est - Dubai', 'Ahmed Al Hussain Exchange Est - Dubai'),
        ('Ain Al Faydah Exchange - Al Ain', 'Ain Al Faydah Exchange - Al Ain'),
        ('Ajman Bank', 'Ajman Bank'),
        ('Al Ahalia Money Exchange Bureau - Abu Dhabi', 'Al Ahalia Money Exchange Bureau - Abu Dhabi'),
        ('Al Ahli Bank Of Kuwait K.S.C.', 'Al Ahli Bank Of Kuwait K.S.C.'),
        ('Al Ansari Exchange LLC', 'Al Ansari Exchange LLC'),
        ('Al Ansari Exchange Services - Al Ain', 'Al Ansari Exchange Services - Al Ain'),
        ('Al Azhar Exchange - Dubai', 'Al Azhar Exchange - Dubai'),
        ('Al Bader Exchange - Abu Dhabi', 'Al Bader Exchange - Abu Dhabi'),
        ('Al Balooch Money Exchange - Al Ain', 'Al Balooch Money Exchange - Al Ain'),
        ('Al Dahab Exchange Dubai', 'Al Dahab Exchange Dubai'),
        ('Al Darmaki Exchange Est - Dubai', 'Al Darmaki Exchange Est - Dubai'),
        ('Al Dhahery Exchange', 'Al Dhahery Exchange'),
        ('Al Dhahery Money Exchange - Al Ain', 'Al Dhahery Money Exchange - Al Ain'),
        ('Al Dinar Exchange Company', 'Al Dinar Exchange Company'),
        ('Al Falah Exchange Company - Abu Dhabi', 'Al Falah Exchange Company - Abu Dhabi'),
        ('Al Fardan Exchange - Abu Dhabi', 'Al Fardan Exchange - Abu Dhabi'),
        ('Al Fuad Exchange - Dubai', 'Al Fuad Exchange - Dubai'),
        ('Al Gergawi Exchange LLC - Dubai', 'Al Gergawi Exchange LLC - Dubai'),
        ('Al Ghurair Exchange - Dubai', 'Al Ghurair Exchange - Dubai'),
        ('Al Ghurair International Exchange - Dubai', 'Al Ghurair International Exchange - Dubai'),
        ('Al Hadha Exchange LLC - Dubai', 'Al Hadha Exchange LLC - Dubai'),
        ('Al Hamed Exchange - Sharjah', 'Al Hamed Exchange - Sharjah'),
        ('Al Hamriyah Exchange - Dubai', 'Al Hamriyah Exchange - Dubai'),
        ('Al Hilal Bank', 'Al Hilal Bank'),
        ('Al Jarwan Money Exchange - Sharjah', 'Al Jarwan Money Exchange - Sharjah'),
        ('Al Masood Exchange - Abu Dhabi', 'Al Masood Exchange - Abu Dhabi'),
        ('Al Mazroui Exchange Est - Abu Dhabi', 'Al Mazroui Exchange Est - Abu Dhabi'),
        ('Al Modawallah Exchange - Dubai', 'Al Modawallah Exchange - Dubai'),
        ('Al Mona Exchange CO LLC - Dubai', 'Al Mona Exchange CO LLC - Dubai'),
        ('Al Mussabah Exchange - Dubai', 'Al Mussabah Exchange - Dubai'),
        ('Al Nafees Exchange LLC - Dubai', 'Al Nafees Exchange LLC - Dubai'),
        ('Al Ne\'Emah Exchange CO LLC - Dubai', 'Al Ne\'Emah Exchange CO LLC - Dubai'),
        ('Al Nibal International Exchange', 'Al Nibal International Exchange'),
        ('Al Rajihi Exchange Company LLC - Dubai', 'Al Rajihi Exchange Company LLC - Dubai'),
        ('Al Razouki Int\'L Exchange CO LLC - Dubai', 'Al Razouki Int\'L Exchange CO LLC - Dubai'),
        ('Al Rostamani Exchange - Dubai', 'Al Rostamani Exchange - Dubai'),
        ('Al Zari & Al Fardan Exchange LLC - Sharjah', 'Al Zari & Al Fardan Exchange LLC - Sharjah'),
        ('Al Zarooni Exchange - Dubai', 'Al Zarooni Exchange - Dubai'),
        ('Alfalah Exchange Company', 'Alfalah Exchange Company'),
        ('Alukkass Exchange Dubai', 'Alukkass Exchange Dubai'),
        ('Arab African International Bank', 'Arab African International Bank'),
        ('Arab Bank - Qatar', 'Arab Bank - Qatar'),
        ('Arab Bank PLC', 'Arab Bank PLC'),
        ('Arabian Exchange Co - Abu Dhabi', 'Arabian Exchange Co - Abu Dhabi'),
        ('Ary International Exchange - Dubai', 'Ary International Exchange - Dubai'),
        ('Asia Exchange Centre - Dubai', 'Asia Exchange Centre - Dubai'),
        ('Aziz Exchange CO LLC - Dubai', 'Aziz Exchange CO LLC - Dubai'),
        # Add your new bank choices here
        ('Bank MISR', 'Bank MISR'),
        ('Bank Melli Iran', 'Bank Melli Iran'),
        ('Bank Of Baroda - Al Ain', 'Bank Of Baroda - Al Ain'),
        ('Bank Of Baroda - Deira', 'Bank Of Baroda - Deira'),
        ('Bank Of Baroda - Dubai HO', 'Bank Of Baroda - Dubai HO'),
        ('Bank Of Baroda - RAK', 'Bank Of Baroda - RAK'),
        ('Bank Of Baroda - Sharjah', 'Bank Of Baroda - Sharjah'),
        ('Bank Of Sharjah', 'Bank Of Sharjah'),
        ('Bank Saderat Iran', 'Bank Saderat Iran'),
        ('Banque Libanaise(France)', 'Banque Libanaise(France)'),
        ('Banque Paribas', 'Banque Paribas'),
        ('Barclays', 'Barclays'),
        ('Bhagwandas Jethanand And Sons - Sharjah', 'Bhagwandas Jethanand And Sons - Sharjah'),
        ('Bin Bakheet Exchange Est - Ajman', 'Bin Bakheet Exchange Est - Ajman'),
        ('Bin Belaila Exchange CO LLC', 'Bin Belaila Exchange CO LLC'),
        ('Bin Belaila Exchange CO LLC - Dubai', 'Bin Belaila Exchange CO LLC - Dubai'),
        ('Blom Bank France', 'Blom Bank France'),
        ('C3', 'C3'),
        ('Cash Express Exchange Est - Dubai', 'Cash Express Exchange Est - Dubai'),
        ('Citibank N.A.', 'Citibank N.A.'),
        ('City Exchange LLC - Dubai', 'City Exchange LLC - Dubai'),
        ('Commercial Bank Of Dubai', 'Commercial Bank Of Dubai'),
        ('Commercial Bank-Qatar', 'Commercial Bank-Qatar'),
        ('Credit Agricole', 'Credit Agricole'),
        ('Daniba International Exchange - Dubai', 'Daniba International Exchange - Dubai'),
        ('Day Exchange LLC - Dubai', 'Day Exchange LLC - Dubai'),
        ('Dinar Exchange - Dubai', 'Dinar Exchange - Dubai'),
        ('Doha Bank', 'Doha Bank'),
        ('Dubai Bank PJSC', 'Dubai Bank PJSC'),
        ('Dubai Exchange Centre LLC - Dubai', 'Dubai Exchange Centre LLC - Dubai'),
        ('Dubai Express Exchange', 'Dubai Express Exchange'),
        ('Dubai Islamic Bank', 'Dubai Islamic Bank'),
        ('Dunia', 'Dunia'),
        ('Economic Exchange', 'Economic Exchange'),
        ('Economic Exchange Centre', 'Economic Exchange Centre'),
        ('El Nilein Bank', 'El Nilein Bank'),
        ('Emirates & East India Exchange - Sharjah', 'Emirates & East India Exchange - Sharjah'),
        ('Emirates India International Exchange - Sharjah', 'Emirates India International Exchange - Sharjah'),
        ('Emirates Islamic Bank', 'Emirates Islamic Bank'),
        ('Emirates NBD', 'Emirates NBD'),
        ('Federal Exchange - Dubai', 'Federal Exchange - Dubai'),
        ('Finance House', 'Finance House'),
        ('First Gulf Bank', 'First Gulf Bank'),
        ('First Gulf Exchange Centre - Dubai', 'First Gulf Exchange Centre - Dubai'),
        ('Future Exchange', 'Future Exchange'),
        ('GCC Exchange', 'GCC Exchange'),
        ('Global Exchange', 'Global Exchange'),
        ('Gomti Exchange LLC - Dubai', 'Gomti Exchange LLC - Dubai'),
        ('Gulf Express Exchange - Dubai', 'Gulf Express Exchange - Dubai'),
        ('Gulf Int\'L Exchange CO LLC - Dubai', 'Gulf Int\'L Exchange CO LLC - Dubai'),
        ('HSBC Financial Services', 'HSBC Financial Services'),
        ('HSBC Middle East', 'HSBC Middle East'),
        ('Habib Bank A.G. Zurich', 'Habib Bank A.G. Zurich'),
        ('Habib Bank Limited', 'Habib Bank Limited'),
        ('Habib Exchange CO LLC - Sharjah', 'Habib Exchange CO LLC - Sharjah'),
        ('Hadi Express Exchange - Dubai', 'Hadi Express Exchange - Dubai'),
        ('Harib Sultan Exchange - Abu Dhabi', 'Harib Sultan Exchange - Abu Dhabi'),
        ('Horizon Exchange - Dubai', 'Horizon Exchange - Dubai'),
        ('International Development Exchange - Dubai', 'International Development Exchange - Dubai'),
        ('Invest Bank', 'Invest Bank'),
        ('Janata Bank', 'Janata Bank'),
        ('Jumana Exchange Est - Dubai', 'Jumana Exchange Est - Dubai'),
        ('Kanoo Exchange - Dubai', 'Kanoo Exchange - Dubai'),
        ('Khalil Al Fardan Exchange - Dubai', 'Khalil Al Fardan Exchange - Dubai'),
        ('Khalili Exchange CO LLC - Dubai', 'Khalili Exchange CO LLC - Dubai'),
        ('Lari Exchange Est - Abu Dhabi', 'Lari Exchange Est - Abu Dhabi'),
        ('Lee La Megh Exchange LLC - Dubai', 'Lee La Megh Exchange LLC - Dubai'),
        ('Lloyds Bank', 'Lloyds Bank'),
        ('Lulu Exchange', 'Lulu Exchange'),
        ('Malik Exchange - Abu Dhabi', 'Malik Exchange - Abu Dhabi'),
        ('Mashreq PSC', 'Mashreq PSC'),
        ('Multinet Trust Exchange LLC - Dubai', 'Multinet Trust Exchange LLC - Dubai'),
        ('Nanikdas Nathoomal Exchange CO LLC - Dubai', 'Nanikdas Nathoomal Exchange CO LLC - Dubai'),
        ('Naser Khoory Exchange Est - Abu Dhabi', 'Naser Khoory Exchange Est - Abu Dhabi'),
        ('Nasim Al Barari Exchange', 'Nasim Al Barari Exchange'),
        ('National Bank Of Abu Dhabi', 'National Bank Of Abu Dhabi'),
        ('National Bank Of Bahrain', 'National Bank Of Bahrain'),
        ('National Bank Of Fujairah', 'National Bank Of Fujairah'),
        ('National Bank Of Kuwait', 'National Bank Of Kuwait'),
        ('National Bank Of Oman', 'National Bank Of Oman'),
        ('National Bank Of Umm Al Qaiwain', 'National Bank Of Umm Al Qaiwain'),
        ('National Exchange CO - Abu Dhabi', 'National Exchange CO - Abu Dhabi'),
        ('Noor Islamic Bank', 'Noor Islamic Bank'),
        ('Oasis Exchange', 'Oasis Exchange'),
        ('Orient Exchange COLLC - Dubai', 'Orient Exchange COLLC - Dubai'),
        ('Others', 'Others'),
        ('Pacific Exchange - Dubai', 'Pacific Exchange - Dubai'),
        ('Qatar National Bank', 'Qatar National Bank'),
        ('Rafidain Bank', 'Rafidain Bank'),
        ('Rak Bank', 'Rak Bank'),
        ('Redha Al Ansari Exchange Est - Dubai', 'Redha Al Ansari Exchange Est - Dubai'),
        ('Reems Exchange - Dubai', 'Reems Exchange - Dubai'),
        ('Royal Bank Of Canada', 'Royal Bank Of Canada'),
        ('Royal Bank Of Scotland', 'Royal Bank Of Scotland'),
        ('Royal Exchange CO LLC', 'Royal Exchange CO LLC'),
        ('Sa\'Ad Exchange - Fujairah', 'Sa\'Ad Exchange - Fujairah'),
        ('Sabah Exchange - Sharjah', 'Sabah Exchange - Sharjah'),
        ('Sajwani Exchange - Dubai', 'Sajwani Exchange - Dubai'),
        ('Salim Exchange - Sharjah', 'Salim Exchange - Sharjah'),
        ('Samba Financial Group', 'Samba Financial Group'),
        ('Sana\'A Exchange - Dubai', 'Sana\'A Exchange - Dubai'),
        ('Sawan Exchange CO LLC - Dubai', 'Sawan Exchange CO LLC - Dubai'),
        ('Seidco', 'Seidco'),
        ('Shaheen Money Exchange LLC - Dubai', 'Shaheen Money Exchange LLC - Dubai'),
        ('Sharaf Exchange', 'Sharaf Exchange'),
        ('Sharjah International Exchange - Sharjah', 'Sharjah International Exchange - Sharjah'),
        ('Sharjah Islamic Bank', 'Sharjah Islamic Bank'),
        ('Standard Chartered Bank', 'Standard Chartered Bank'),
        ('Tabra & Al Nebal Exchange - Dubai', 'Tabra & Al Nebal Exchange - Dubai'),
        ('Tahir Exchange Est - Dubai', 'Tahir Exchange Est - Dubai'),
        ('Taymour & Abou Harb Exchange CO LLC - Sharjah', 'Taymour & Abou Harb Exchange CO LLC - Sharjah'),
        ('U.A.E. Exchange Centre LLC - Dubai', 'U.A.E. Exchange Centre LLC - Dubai'),
        ('Union Exchange - Abu Dhabi', 'Union Exchange - Abu Dhabi'),
        ('Union National Bank', 'Union National Bank'),
        ('United Arab Bank', 'United Arab Bank'),
        ('United Bank Ltd', 'United Bank Ltd'),
        ('Universal Exchange Centre - Dubai', 'Universal Exchange Centre - Dubai'),
        ('Wall Street Exchange Centre LLC - Dubai', 'Wall Street Exchange Centre LLC - Dubai'),
        ('Waseela Equity', 'Waseela Equity'),
        ('Workers Equity Holdings', 'Workers Equity Holdings'),
        ('Zahra Al Yousuf Exchange - Dubai', 'Zahra Al Yousuf Exchange - Dubai'),
        ('Zareen Exchange', 'Zareen Exchange'),
    ]

     
    # Add a status field
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    
    master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
    username = models.CharField(max_length=100,default=True,blank=True,null=True)
    emp_id = models.CharField(max_length=50,default=True,blank=True,null=True)
    email = models.EmailField(default=True,blank=True,null=True)
    group = models.CharField(max_length=100,default=True,blank=True,null=True)
    department = models.CharField(max_length=100,default=True,blank=True,null=True)
    bank_name = models.CharField(max_length=100, choices=BANK_CHOICES)
    branch = models.CharField(max_length=100,default=True,blank=True,null=True)
    iban_number = models.CharField(max_length=100,default=True,blank=True,null=True)
    Bankstart_date = models.DateField(default=True,blank=True,null=True)
    bank_code = models.CharField(max_length=50,default=True,blank=True,null=True)
    bankaccount_comment = models.CharField(default=True,blank=True,null=True)
    bankaccount_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    bankaccount_applied_date = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.username}'s Bank Account"

class EmployeeTravel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    PURPOSE_OF_VISIT_CHOICES = [
        ('business_trip', 'Business Trip'),
        ('work_assignment', 'Work Assignment'),
    ]

    COUNTRY_CHOICES = [
        ('Afghanistan', 'Afghanistan'),
        ('Aland Islands', 'Aland Islands'),
        ('Albania', 'Albania'),
        ('Algeria', 'Algeria'),
        ('American Samoa', 'American Samoa'),
        ('Andorra', 'Andorra'),
        ('Angola', 'Angola'),
        ('Anguilla', 'Anguilla'),
        ('Antarctica', 'Antarctica'),
        ('Antigua', 'Antigua'),
        ('Antigua and Barbuda', 'Antigua and Barbuda'),
        ('Argentina', 'Argentina'),
        ('Armenia', 'Armenia'),
        ('Aruba', 'Aruba'),
        ('Australia', 'Australia'),
        ('Austria', 'Austria'),
        ('Azerbaijan', 'Azerbaijan'),
        # Include all other countries here
    ]

    CURRENCY_CHOICES = [
        ('AED', 'AED'),
        ('BHD', 'BHD'),
        ('CNY', 'CNY'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
        ('INR', 'INR'),
        ('JPY', 'JPY'),
        ('KRW', 'KRW'),
        ('KWD', 'KWD'),
        ('OMR', 'OMR'),
        ('QAR', 'QAR'),
        ('SAR', 'SAR'),
        ('SEK', 'SEK'),
        ('USD', 'USD'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    
    master_entry = models.ForeignKey(MasterTable, on_delete=models.CASCADE,blank=True,null=True)
    username = models.CharField(max_length=255,blank=True, null=True)
    emp_id = models.CharField(max_length=100, blank=True, null=True )
    email = models.EmailField(max_length=100 ,blank=True, null=True)
    group = models.CharField(max_length=100,blank=True, null=True )
    department = models.CharField(max_length=100 ,blank=True, null=True)
    request_type = models.CharField(max_length=100,blank=True, null=True )
    purpose_of_visit = models.CharField(max_length=20, choices=PURPOSE_OF_VISIT_CHOICES,blank=True, null=True)
    travel_start_date = models.DateField(blank=True, null=True)
    travel_end_date = models.DateField(blank=True, null=True)
    country_of_travel = models.CharField(max_length=100, choices=COUNTRY_CHOICES,blank=True, null=True)
    entity_company_traveling_for = models.CharField(max_length=200,blank=True, null=True)
    advance_amount_required = models.CharField(default=False,blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES,blank=True, null=True)
    visa_to_be_processed = models.CharField(max_length=3, blank=True, null=True)
    book_hotel_accommodation = models.CharField(max_length=3, blank=True, null=True)
    flight_ticket_required = models.CharField( default=False,blank=True, null=True)
    visa_letter_required = models.CharField( default=False,blank=True, null=True)
    employeetravel_comments = models.CharField(max_length=500, blank=True, null=True)
    employeetravel_status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True,null=True)
    employeetravel_applied_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)


    def str(self):
        return f"{self.username}'s Employee Travel"
