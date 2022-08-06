import telebot
from config import settings
from order.models import Order, TelegramID

from django.core.management.base import BaseCommand


bot = telebot.TeleBot(settings.TELEGRAM_API)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    TelegramID.objects.get_or_create(user_id=message.chat.id)
    bot.reply_to(message, "Howdy")


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('TELEGRAM BOT RUNNING'))
        settings.TELEGRAM_BOT = bot
        bot.infinity_polling()
