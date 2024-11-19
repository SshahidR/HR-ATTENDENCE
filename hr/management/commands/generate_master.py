from django.core.management.base import BaseCommand
from hr.models import generate_master_table

class Command(BaseCommand):
    help = 'Generate MasterTable model dynamically'

    def handle(self, *args, **kwargs):
        MasterTable = generate_master_table()
        self.stdout.write(self.style.SUCCESS('Successfully created MasterTable model'))