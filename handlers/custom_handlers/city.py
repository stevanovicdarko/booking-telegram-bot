from telebot.types import Message
from states.all_states import UserState
from loader import bot
from utils.handler_functions import is_valid_city_or_state_name

"""
Handler for city name input.
Validates the user's input and advances the search sequence to the country selection.
"""

@bot.message_handler(state=UserState.city_state)
def handle_city(message: Message) -> None:
    """
    Processes the city name provided by the user.
    Uses a validation utility to ensure the input is a valid string.

    Args:
        message (Message): Telegram message object containing the city name.
    """

    city = message.text
    if not is_valid_city_or_state_name(city):
        bot.send_message(message.from_user.id, 'Navedeni naziv grada nije validan. Molimo Vas da pokušate ponovo: ')
        return

    with bot.retrieve_data(message.from_user.id) as data:
        data['new_search']['city'] = city

    bot.send_message(message.from_user.id, 'Unesite državu: ')
    bot.set_state(message.from_user.id, UserState.country_state)
