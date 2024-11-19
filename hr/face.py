# import logging
# logger = logging.getLogger(__name__)

# class LoginSchema(Schema):
#     username: str
#     password: str

# @api.post("/login")
# def login(request, data: LoginSchema):
#     try:
#         # Try to get all entries from MasterTable that match the username
#         master_entries = MasterTable.objects.filter(username__iexact=data.username)
#         if not master_entries.exists():
#             return JsonResponse({"error": "User not found"}, status=404)
#     except MasterTable.DoesNotExist:
#         return JsonResponse({"error": "User not found"}, status=404)
    
#     # Assume the first entry for creating or getting the CustomUser
#     master_entry = master_entries.first()
    
#     # Create or get the CustomUser
#     user, created = CustomUser.objects.get_or_create(
#         username=master_entry.username,
#         defaults={
#             'department': master_entry.department,
#             'emp_id': master_entry.emp_id,
#             'phone_number': master_entry.phone_number,
#             'designation': master_entry.designation,
#             'group': master_entry.group,
#             'address': master_entry.address,
#             'country': master_entry.country,
#             'state': master_entry.state,
#             'whats_up_number': master_entry.whats_up_number,
#             'date_of_birth': master_entry.date_of_birth,
#             'date_joined': master_entry.date_joined,
#             'otp': master_entry.otp,
#             'is_active': master_entry.is_active,
#             'email': master_entry.email,
#             'first_name': master_entry.first_name,
#             'last_name': master_entry.last_name,
#         }
#     )

#     if created:
#         # Set password if the user is newly created
#         user.set_password(master_entry.password)
#         user.save()

#     # Verify the password with the CustomUser instance
#     if not user.check_password(data.password):
#         return JsonResponse({"error": "Invalid password"}, status=401)
    
#     if not user.is_active:
#         return JsonResponse({"error": "Account not activated"}, status=401)
    
#     # Generate or retrieve the token
#     user.last_login = timezone.now()
#     user.save(update_fields=['last_login'])
#     token, created = Token.objects.get_or_create(user=user)
    
#     # Track existing leaves
#     existing_leaves = Leaves.objects.filter(emp_id=master_entry.emp_id)
    
   
#     for master_entry in master_entries:
#         # Check if a leave entry already exists for the given master_entry id
#         if not Leaves.objects.filter(master_entry=master_entry).exists():
#             Leaves.objects.create(
#                 master_entry=master_entry,
#                 user=user,
#                 emp_id=master_entry.emp_id,
#                 email=master_entry.email,
#                 username=f"{master_entry.first_name} {master_entry.last_name}",
#                 department=master_entry.department,
#                 group=master_entry.group,
                
#                 start_date=master_entry.start_date,
#                 end_date=master_entry.end_date,
#                 replaced_by=master_entry.replaced_by,
#                 leave_reason=master_entry.leave_reason,
#                 leave_type=master_entry.leave_type,
#                 category=master_entry.category,
#                 passport_withdrawal_date=master_entry.passport_withdrawal_date,
#                 request_for_airticket=master_entry.request_for_airticket,
#                 leaves_comments=master_entry.leaves_comments,
#                 leaves_status=master_entry.leaves_status,
#                 leave_balance=master_entry.leave_balance,
#                 duration=master_entry.duration,
#                 leaves_applied_date=master_entry.leaves_applied_date,
#             )
#             logger.info("Leave entry created for master_entry id: %s", master_entry.id)
#         else:
#             logger.info("Leave entry already exists for master_entry id: %s", master_entry.id)

#     for master_entry in master_entries:
#         if not daywiseAttendance.objects.filter(master_entry=master_entry).exists():
#             daywiseAttendance.objects.create(
#                 user=user,
#                 master_entry=master_entry,
#                 username=f"{master_entry.first_name} {master_entry.last_name}",
#                 check_in=master_entry.check_in,
#                 check_out=master_entry.check_out,
#                 status=master_entry.status,
#                 timeShortageExceed=master_entry.timeShortageExceed,
#                 total_hours=master_entry.total_hours,
#                 chk_date=master_entry.chk_date,
#             )
#             logger.info("daywiseAttendance created for emp_id: %s", master_entry.emp_id)
#         else:
#             logger.info("Leave entry already exists for master_entry id: %s", master_entry.id)

#     for master_entry in master_entries:
#         if not EmployeeAttendanceException.objects.filter(master_entry=master_entry).exists():
            
#             EmployeeAttendanceException.objects.create(
#                 user=user,
#                 master_entry=master_entry,
#                 emp_id=master_entry.emp_id,
#                 email=master_entry.email,
#                 username=f"{master_entry.first_name} {master_entry.last_name}",
#                 department=master_entry.department,
#                 group=master_entry.group,
#                 date_of_exception=master_entry.date_of_exception,
#                 hours_late_in=master_entry.hours_late_in,
#                 minutes_late_in=master_entry.minutes_late_in,
#                 hours_early_out =master_entry.hours_early_out ,
#                 attendanceException_reason=master_entry.attendanceException_reason,
#                 attendanceException_status=master_entry.attendanceException_status,
#                 reason_category=master_entry.reason_category,
#                 attendanceExceptionApplied_date =master_entry.attendanceExceptionApplied_date ,
#                 minutes_early_out =master_entry.minutes_early_out
#             )
#             logger.info("daywiseAttendance for emp_id: %s", master_entry.emp_id)
#         else:
#             logger.info("Leave entry already exists for master_entry id: %s", master_entry.id)

    
    
    
    
#     logger.info("User %s: token %s (new: %s)", user.username, token.key, created)
    
#     user_dict = {
#         'username': user.username,
#     }
    
#     return JsonResponse({'token': token.key, 'user': user_dict})