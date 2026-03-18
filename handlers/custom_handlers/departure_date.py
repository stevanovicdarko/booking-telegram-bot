from telebot.types import Message
from states.all_states import UserState
from loader import bot
from utils.handler_functions import format_date

"""
Handler for the check-out (departure) date input.
Performs cross-validation with the arrival date to ensure a logical stay duration.
"""

@bot.message_handler(state=UserState.departure_state)
def handle_departure_date(message: Message) -> None:
    """
    Processes the departure date.
    Validates the format and ensures it occurs after the previously stored arrival date.

    Args:
        message (Message): Telegram message object containing the departure date.
    """


    input_date = message.text
    departure_date = format_date(input_date)
    if not departure_date:
        bot.send_message(message.from_user.id, 'Neispravan format datuma odlaska. Molimo unesite ponovo (npr. 15.05.2026):')
        return

    with bot.retrieve_data(message.from_user.id) as data:
        arrival_date = data['new_search']['arrival_date']
        if departure_date < arrival_date:
            bot.send_message(message.from_user.id, 'Greška pri unosu datuma odlaska, on mora biti posle datuma dolaska.'
                                                   'Molimo unesit ponovo:')
            return
        data['new_search']['departure_date'] = departure_date
    bot.send_message(message.from_user.id, 'Navedite raspon cene po noćenju (npr. 30-80):')
    bot.set_state(message.from_user.id, UserState.pricerange_state)