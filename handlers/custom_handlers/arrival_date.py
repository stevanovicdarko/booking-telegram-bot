from telebot.types import Message
from states.all_states import UserState
from loader import bot
from utils.handler_functions import format_date
from datetime import date

"""
Handler for the check-in (arrival) date input.
Validates the date format and ensures the date is set in the future.
"""

@bot.message_handler(state=UserState.arrival_state)
def handle_arrival_date(message: Message) -> None:
    """
    Processes the arrival date provided by the user.
    Uses 'format_date' utility for parsing and performs a logical check
    to prevent past-date bookings.

    Args:
        message (Message): Telegram message object containing the date string.
    """


    input_date = message.text
    arrival_date = format_date(input_date)
    if not arrival_date:
        bot.send_message(message.from_user.id, 'Neispravan datum dolaska. Pokušajte ponovo:')
        return

    date_today = date.today()

    if date_today >= arrival_date:
        bot.send_message(message.from_user.id, 'Datum dolaska ne može biti u prošlosti. Unesite novi datum:')
        return

    with bot.retrieve_data(message.from_user.id) as data:
        data['new_search']['arrival_date'] = arrival_date
    bot.send_message(message.from_user.id, 'Unesite datum odlaska:')
    bot.set_state(message.from_user.id, UserState.departure_state)