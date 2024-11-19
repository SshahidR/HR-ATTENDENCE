# from django.core.management.base import BaseCommand
# from ninja import Schema
# from hr.models import MasterTable, BankAccount, CustomUser
# import logging

# logger = logging.getLogger(__name__)

# class LoginSchema(Schema):
#     username: str
#     password: str

# class Command(BaseCommand):
#     help = 'Sync MasterTable with relevant tables'

#     def add_arguments(self, parser):
#         parser.add_argument('username', type=str, help='Username for login')

#     def handle(self, *args, **kwargs):
#         username = kwargs['username']
#         try:
#             # First, attempt to find the user in CustomUser
#             user = CustomUser.objects.get(username__iexact=username)
#             logger.info(f"User found in CustomUser: {username}")
#         except CustomUser.DoesNotExist:
#             # If user is not found in CustomUser, attempt to find entries in MasterTable
#             master_entries = MasterTable.objects.filter(username__iexact=username)
#             if not master_entries.exists():
#                 self.stdout.write(self.style.ERROR("User not found"))
#                 return

#             master_entry = master_entries.first()
#             user, created = CustomUser.objects.get_or_create(
#                 username=master_entry.username,
#                 defaults={
#                     'department': master_entry.department,
#                     'emp_id': master_entry.emp_id,
#                     'phone_number': master_entry.phone_number,
#                     'designation': master_entry.designation,
#                     'group': master_entry.group,
#                     'address': master_entry.address,
#                     'country': master_entry.country,
#                     'state': master_entry.state,
#                     'whats_up_number': master_entry.whats_up_number,
#                     'date_of_birth': master_entry.date_of_birth,
#                     'date_joined': master_entry.date_joined,
#                     'otp': master_entry.otp,
#                     'is_active': master_entry.is_active,
#                     'email': master_entry.email,
#                     'first_name': master_entry.first_name,
#                     'last_name': master_entry.last_name,
#                 }
#             )
#             if created:
#                 logger.info(f"User created for emp_id: {master_entry.emp_id}")
#             else:
#                 logger.info(f"User updated for emp_id: {master_entry.emp_id}")

#         master_entries = MasterTable.objects.filter(username__iexact=username)
#         for master_entry in master_entries:
#             if not BankAccount.objects.filter(master_entry=master_entry).exists():
#                 BankAccount.objects.create(
#                     user=user,
#                     master_entry=master_entry,
#                     emp_id=master_entry.emp_id,
#                     email=master_entry.email,
#                     username=f"{master_entry.first_name} {master_entry.last_name}",
#                     department=master_entry.department,
#                     group=master_entry.group,
#                     bank_name=master_entry.bank_name,
#                     branch=master_entry.branch,
#                     iban_number=master_entry.iban_number,
#                     Bankstart_date=master_entry.Bankstart_date,
#                     bank_code=master_entry.bank_code,
#                     bankaccount_comment=master_entry.bankaccount_comment,
#                     bankaccount_status=master_entry.bankaccount_status,
#                     bankaccount_applied_date=master_entry.bankaccount_applied_date,
#                 )
#                 logger.info(f"BankAccount entry created for emp_id: {master_entry.emp_id}")
#             else:
#                 logger.info(f"BankAccount entry already exists for master_entry id: {master_entry.id}")




# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
# from ninja import Schema
# from hr.models import MasterTable, BankAccount, CustomUser
# import logging

# logger = logging.getLogger(__name__)

# class LoginSchema(Schema):
#     username: str
#     password: str

# class Command(BaseCommand):
#     help = 'Sync MasterTable with relevant tables'

#     def add_arguments(self, parser):
#         parser.add_argument('username', type=str, help='Username for login')

#     def handle(self, *args, **kwargs):
#         username = kwargs['username']
#         try:
#             # First, attempt to find the user in CustomUser
#             user = CustomUser.objects.get(username__iexact=username)
#             logger.info(f"User found in CustomUser: {username}")
#         except CustomUser.DoesNotExist:
#             # If user is not found in CustomUser, attempt to find entries in MasterTable
#             master_entries = MasterTable.objects.filter(username__iexact=username)
#             if not master_entries.exists():
#                 self.stdout.write(self.style.ERROR("User not found"))
#                 return

#             master_entry = master_entries.first()
#             random_password = CustomUser.objects.make_random_password()
#             user, created = CustomUser.objects.get_or_create(
#                 username=master_entry.username,
#                 defaults={
#                     'department': master_entry.department,
#                     'emp_id': master_entry.emp_id,
#                     'phone_number': master_entry.phone_number,
#                     'designation': master_entry.designation,
#                     'group': master_entry.group,
#                     'address': master_entry.address,
#                     'country': master_entry.country,
#                     'state': master_entry.state,
#                     'whats_up_number': master_entry.whats_up_number,
#                     'date_of_birth': master_entry.date_of_birth,
#                     'date_joined': master_entry.date_joined,
#                     'otp': master_entry.otp,
#                     'is_active': master_entry.is_active,
#                     'email': master_entry.email,
#                     'first_name': master_entry.first_name,
#                     'last_name': master_entry.last_name,
#                 }
#             )
#             if created:
#                 user.set_password(random_password)
#                 user.save()
#                 logger.info(f"User created for emp_id: {master_entry.emp_id} with a random password")
#             else:
#                 logger.info(f"User updated for emp_id: {master_entry.emp_id}")

#         master_entries = MasterTable.objects.filter(username__iexact=username)
#         for master_entry in master_entries:
#             if not BankAccount.objects.filter(master_entry=master_entry).exists():
#                 BankAccount.objects.create(
#                     user=user,
#                     master_entry=master_entry,
#                     emp_id=master_entry.emp_id,
#                     email=master_entry.email,
#                     username=f"{master_entry.first_name} {master_entry.last_name}",
#                     department=master_entry.department,
#                     group=master_entry.group,
#                     bank_name=master_entry.bank_name,
#                     branch=master_entry.branch,
#                     iban_number=master_entry.iban_number,
#                     Bankstart_date=master_entry.Bankstart_date,
#                     bank_code=master_entry.bank_code,
#                     bankaccount_comment=master_entry.bankaccount_comment,
#                     bankaccount_status=master_entry.bankaccount_status,
#                     bankaccount_applied_date=master_entry.bankaccount_applied_date,
#                 )
#                 logger.info(f"BankAccount entry created for emp_id: {master_entry.emp_id}")
#             else:
#                 logger.info(f"BankAccount entry already exists for master_entry id: {master_entry.id}")
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ninja import Schema
from hr.models import MasterTable, BankAccount, CustomUser
import logging

logger = logging.getLogger(__name__)

class LoginSchema(Schema):
    username: str
    password: str

class Command(BaseCommand):
    help = 'Sync MasterTable with relevant tables'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for login')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        try:
            # First, attempt to find the user in CustomUser
            user = CustomUser.objects.get(username__iexact=username)
            logger.info(f"User found in CustomUser: {username}")
        except CustomUser.DoesNotExist:
            # If user is not found in CustomUser, attempt to find entries in MasterTable
            master_entries = MasterTable.objects.filter(username__iexact=username)
            if not master_entries.exists():
                self.stdout.write(self.style.ERROR("User not found"))
                return

            master_entry = master_entries.first()
            random_password = CustomUser.objects.make_random_password()
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
                user.set_password(random_password)
                user.save()
                logger.info(f"User created for emp_id: {master_entry.emp_id} with a random password: {random_password}")
            else:
                logger.info(f"User updated for emp_id: {master_entry.emp_id}")

        master_entries = MasterTable.objects.filter(username__iexact=username)
        for master_entry in master_entries:
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
                logger.info(f"BankAccount entry created for emp_id: {master_entry.emp_id}")
            else:
                logger.info(f"BankAccount entry already exists for master_entry id: {master_entry.id}")
