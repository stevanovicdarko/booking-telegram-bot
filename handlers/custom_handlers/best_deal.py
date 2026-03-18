from telebot.types import Message
from states.all_states import UserState
from loader import bot

"""
Handler for the /best_deal command.
Starts the search scenario focused on proximity to the city center.
"""

@bot.message_handler(state='*', commands=['best_deal'])
def handle_best_deal_command(message: Message) -> None:
    """
    Initializes a search for hotels with 'Distance to Center' as the primary filter.
    Stores the session intent and prompts for city input.

    Args:
        message (Message): Telegram message object.
    """

    bot.send_message(message.from_user.id, 'Unesite grad koji Vas zanima: ')
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_search'] = {'command': 'distance2centre'}
        data['new_search']['user'] = message.from_user.id
        print(data['new_search'])

    bot.set_state(message.from_user.id, UserState.city_state)