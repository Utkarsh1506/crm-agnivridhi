from django.core.management.base import BaseCommand
from clients.models import Client
from payments.models import RevenueEntry
from accounts.models import User
from decimal import Decimal
from datetime import datetime
import pytz


class Command(BaseCommand):
    help = 'Bulk add revenue entries from admin data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n💰 ADDING REVENUE ENTRIES:\n'))

        data = [
            {'name': "Guleria's", 'pitched': 5000, 'received': 5000, 'pending': 900, 'recorded_by': 'Vasu Agarwal'},
            {'name': 'SHARVOO AVIATION CONSULTANT PVT LTD', 'pitched': 20000, 'received': 11800, 'pending': 11800, 'recorded_by': 'Aaryav Singh'},
            {'name': 'Aggarwal file manufacturers', 'pitched': 5000, 'received': 5000, 'pending': 900, 'recorded_by': 'Akash Tyagi'},
            {'name': 'STAR YOUTH ASSOCIATION', 'pitched': 25000, 'received': 5900, 'pending': 23600, 'recorded_by': 'Rahul Panth'},
            {'name': 'Vibhanshu enterprises', 'pitched': 10000, 'received': 5900, 'pending': 5900, 'recorded_by': 'Akash Tyagi'},
            {'name': 'KRITI PRODUCTIONS', 'pitched': 11800, 'received': 0, 'pending': 13924, 'recorded_by': 'Aaryav Singh'},
            {'name': 'Darsun scientific pvt ltd', 'pitched': 10000, 'received': 11800, 'pending': 0, 'recorded_by': 'Mohd Rihan'},
            {'name': 'Shivansh Hrudeswari Construction', 'pitched': 5000, 'received': 5900, 'pending': 0, 'recorded_by': 'Mohd Rihan'},
            {'name': 'Vashnavi Pharmacy', 'pitched': 10000, 'received': 11800, 'pending': 0, 'recorded_by': 'Mohd Rihan'},
            {'name': 'Utkarsh Pvt Ltd', 'pitched': 0, 'received': 0, 'pending': 0, 'recorded_by': 'aisha1'},
            {'name': 'LEDERRA PRIVATE LIMITED', 'pitched': 20000, 'received': 5900, 'pending': 17700, 'recorded_by': 'Babita Goswami'},
            {'name': 'BRIO LIFESCIENCES', 'pitched': 40000, 'received': 10000, 'pending': 37200, 'recorded_by': 'Sharik Khan'},
            {'name': 'ULTRA VISION SOLAR', 'pitched': 80000, 'received': 15340, 'pending': 79060, 'recorded_by': 'Sharik Khan'},
            {'name': 'CHOROIBETI EDUCATIONAL AND WELFARE TRUST', 'pitched': 20600, 'received': 5900, 'pending': 18408, 'recorded_by': 'Himadri Sharma'},
            {'name': 'Sarfraz Auto Garage', 'pitched': 5000, 'received': 5900, 'pending': 0, 'recorded_by': 'Himadri Sharma'},
        ]

        added_count = 0

        for item in data:
            try:
                # Find client
                client = Client.objects.filter(company_name__icontains=item['name']).first()
                if not client:
                    self.stdout.write(self.style.WARNING(f'⚠️  Client not found: {item["name"]}'))
                    continue

                # Find recorded_by user
                user = User.objects.filter(first_name=item['recorded_by'].split()[0]).first()
                if not user:
                    user = User.objects.filter(role='ADMIN').first()

                # Check if entry already exists
                existing = RevenueEntry.objects.filter(
                    client=client,
                    total_pitched_amount=Decimal(str(item['pitched']))
                ).exists()

                if not existing:
                    entry = RevenueEntry.objects.create(
                        client=client,
                        total_pitched_amount=Decimal(str(item['pitched'])),
                        received_amount=Decimal(str(item['received'])),
                        pending_amount=Decimal(str(item['pending'])),
                        recorded_by=user,
                        source='CLIENT_CREATION'
                    )
                    self.stdout.write(
                        f'✅ {client.company_name}: '
                        f'₹{item["pitched"]} pitched, ₹{item["received"]} received'
                    )
                    added_count += 1
                else:
                    self.stdout.write(f'⏭️  Already exists: {client.company_name}')

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error for {item["name"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ ADDED: {added_count} revenue entries\n'))
