from config.celery import app
import time
from django.core.management.base import BaseCommand
import telebot
import threading

from .utils.get_data_from_sheet import get_data_from_sheet
from .models import Order, TelegramID
from config import settings
import datetime


bot = telebot.TeleBot(settings.TELEGRAM_API)


def create_row(row, users) -> None:
    """
    Check delivery date and save it to database
    :param row: sheet table row
    """
    if row.delivery_date < datetime.date.today():
        send_info(f"Срок поставки прошел {row}", users)
    Order.objects.create(**row)


def send_info(message, users) -> None:
    """
    send message to all users
    :param message: telegram message
    """
    for user in users:
        bot.send_message(user.user_id, message)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message) -> None:
    """
    GETTING MESSAGE FROM TELEGRAM USER AND
    SAVING ID TO DATABASE
    :param message: telegram message
    """
    TelegramID.objects.get_or_create(user_id=message.chat.id)
    bot.reply_to(message, "Howdy")


@app.task
def update_data():
    users = TelegramID.objects.all()
    print("STARTING TELEGRAM BOT")
    threading.Thread(target=bot.polling).start()

    print("GETTING DATA FROM SHEET")
    df = get_data_from_sheet()
    Order.objects.all().delete()
    print("STARTING UPDATING DATA TO DATABASE")
    df.apply(create_row, axis=1, args=(users,))
    print("STOPPING TELEGRAM BOT")
    bot.stop_bot()
    print('Successfully updated')
