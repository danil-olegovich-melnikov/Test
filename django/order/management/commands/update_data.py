from django.core.management.base import BaseCommand, CommandError
from order.utils.get_data_from_sheet import get_data_from_sheet
from order.models import Order, TelegramID
from config import settings
import datetime

class Command(BaseCommand):
    @staticmethod
    def create_row(row):
        if row.delivery_date < datetime.date.today():
            Command.send_info(f"Срок поставки прошел {row}")
        Order.objects.create(**row)

    @staticmethod
    def send_info(message):
        if settings.TELEGRAM_BOT is False:
            return

        users = TelegramID.objects.all()
        for user in users:
            settings.TELEGRAM_BOT.send_message(user.user_id, message)

    def handle(self, *args, **options):
        df = get_data_from_sheet()
        Order.objects.all().delete()
        df.apply(self.create_row, axis=1)
        self.stdout.write(self.style.SUCCESS('Successfully updated'))
