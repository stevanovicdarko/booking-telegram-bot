from telebot.types import Message
from states.all_states import UserState
from loader import bot

"""
Entry point handlers for the Telegram bot.
Handles the initial interaction when a user starts the bot.
"""

@bot.message_handler(commands=['start'])
def handle_start(message: Message) -> None:
    """
    Handles the /start command.
    Greets the user, displays the main menu of commands, and
    initializes the user's state to 'start_state'.

    Args:
        message (Message): Telegram message object containing user info.
    """

    bot.send_message(message.from_user.id, "Dobro došli u bot za pronalaženje hotela sa sajtu BOOKING.COM!\n"
                                            "\nMolimo izaberite jednu od sledećih komandi:\n"
                                            "\n/low_price - Lista top 10 najjeftinijih hotela na vašoj lokaciji\n"
                                            "\n/guest_rating - Lista top 10 najbolje ocenjenih hotela na osnovu recenzija\n"
                                            "\n/best_deal - Lista top 10 hotela najbližih centru grada"
                     )

    bot.set_state(message.from_user.id, UserState.start_state)
