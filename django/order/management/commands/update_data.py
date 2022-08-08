from django.core.management.base import BaseCommand, CommandError
import telebot
import threading

from order.utils.get_data_from_sheet import get_data_from_sheet
from order.models import Order, TelegramID
from config import settings
import datetime


class Command(BaseCommand):
    bot = telebot.TeleBot(settings.TELEGRAM_API)

    def __init__(self):
        super().__init__()
        self.users = TelegramID.objects.all()

    def create_row(self, row) -> None:
        """
        Check delivery date and save it to database
        :param row: sheet table row
        """
        if row.delivery_date < datetime.date.today():
            self.send_info(f"Срок поставки прошел {row}")
        Order.objects.create(**row)

    def send_info(self, message) -> None:
        """
        send message to all users
        :param message: telegram message
        """
        for user in self.users:
            self.bot.send_message(user.user_id, message)

    def handle(self, *args, **options) -> None:
        self.stdout.write("STARTING TELEGRAM BOT")
        threading.Thread(target=self.bot.polling).start()

        self.stdout.write("GETTING DATA FROM SHEET")
        df = get_data_from_sheet()
        Order.objects.all().delete()
        self.stdout.write("UPDATE DATA TO DATABASE")
        df.apply(self.create_row, axis=1)
        self.stdout.write("STOPPING TELEGRAM BOT")
        self.bot.stop_bot()
        self.stdout.write(self.style.SUCCESS('Successfully updated'))


@Command.bot.message_handler(commands=['start', 'help'])
def send_welcome(message) -> None:
    """
    GETTING MESSAGE FROM TELEGRAM USER AND
    SAVING ID TO DATABASE

    :param message: telegram message
    """
    TelegramID.objects.get_or_create(user_id=message.chat.id)
    Command.bot.reply_to(message, "Howdy")
