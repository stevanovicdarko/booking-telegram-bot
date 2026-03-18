from telebot.types import Message
from states.all_states import UserState
from loader import bot

"""
Handler for the /help command.
Provides guidance on how to use the bot and list of available commands.
"""

@bot.message_handler(commands=['help'])
def handle_start(message: Message) -> None:
    """
    Displays a help message with command descriptions.
    Resets the user's state to 'start_state' to ensure they can
    initiate a new search from a clean slate.

    Args:
        message (Message): Telegram message object.
    """

    bot.send_message(message.from_user.id,
                     "Ovaj bot je napravljen da ti pomogne pri rezervaciji hotela na sajtu BOOKING.COM\n"
                     "Pomoć sa komandama:\n"
                     "/start - Pokreni bota\n"
                     "/low_price - Pronađi najjeftinije hotele u izabranom gradu\n"
                     "/guest_rating - Pronađi najbolje ocenjene hotele\n"
                     "/best_deal - Pronađi hotele najbliže centru grada\n"
                     "/history - Pogledaj istoriju svojih pretraga\n"
                     "/help - Prikaži ovu pomoć"
                     )

    bot.set_state(message.from_user.id, UserState.start_state)