from telebot.types import Message
from loader import bot
from database.crud import retrieve_data


@bot.message_handler(state='*', commands=['history'])
def handle_history_command(message: Message) -> None:
    hotels = retrieve_data(message.from_user.id)
    for rows in hotels:
        bot.send_message(message.from_user.id, rows)
