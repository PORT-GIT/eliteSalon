# this is the code that will helo me export the service durations to a csv file
import csv
from django.core.management.base import BaseCommand
from salon.models import service

class Command(BaseCommand):
    help = "Export service duration to a csv file"

    def handle(self, *args, **kwargs):
        filename = "serviceDurations.csv"

        with open(filename, mode='w', newline='', encoding="utf-8") as csvfile:
            fieldnames = ['Service Name', 'Duration of Service']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for svc in service.objects.all():
                writer.writerow({'Service Name': svc.service_name, 'Duration of Service': svc.durationOfService}) 

        self.stdout.write(self.style.SUCCESS(f'Successfully exported service durations to {filename}'))
