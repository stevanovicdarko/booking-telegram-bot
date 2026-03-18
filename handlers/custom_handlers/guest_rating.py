from telebot.types import Message
from states.all_states import UserState
from loader import bot

"""
Handler for the /guest_rating command.
Initiates the search scenario specifically for highly-rated hotels.
"""

@bot.message_handler(state='*', commands=['guest_rating'])
def handle_guest_rating_command(message: Message) -> None:
    """
    Triggers the hotel search flow with 'Guest Rating' as the sorting criteria.
    Updates the FSM context and prompts the user for city input.

    Args:
        message (Message): Telegram message object.
    """


    bot.send_message(message.from_user.id, 'Unesite grad koji Vas zanima: ')
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_search'] = {'command': 'guestrating'}
        data['new_search']['user'] = message.from_user.id

    bot.set_state(message.from_user.id, UserState.city_state)