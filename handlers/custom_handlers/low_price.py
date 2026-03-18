from telebot.types import Message
from states.all_states import UserState
from loader import bot

"""
Handler for the /low_price command.
Starts the hotel search scenario with 'Price Lowest' sorting criteria.
"""

@bot.message_handler(state='*', commands=['low_price'])
def handle_low_price_command(message: Message) -> None:
    """
    Initiates the search process for low-priced hotels.
    Sets up the initial data structure in FSM storage and moves the user to city input.

    Args:
        message (Message): Telegram message object.
    """
    bot.send_message(message.from_user.id, 'Unesite grad koji Vas zanima: ')
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_search'] = {'command': 'lowprice'}
        data['new_search']['user'] = message.from_user.id
        print(data['new_search'])

    bot.set_state(message.from_user.id, UserState.city_state)
