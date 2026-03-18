from telebot.types import Message
from states.all_states import UserState
from loader import bot

"""
Fallback handler for the initial state.
Captures any text input that isn't a command while the user is in 'start_state'.
"""

@bot.message_handler(state=UserState.start_state)
def handle_control_start_state(message: Message) -> None:
    """
    Guides the user back to the main commands if they send plain text
    instead of using a valid /command in the start state.

    Args:
        message (Message): Telegram message object containing the unintended text.

    """


    user_input = message.text
    bot.send_message(message.from_user.id,
                     "Zdravo! Uneo si {}, ali bi trebalo da koristiš jednu od sledećih komandi:"
                     "\nlow_price - Lista top 10 najjeftinijih hotela na vašoj lokaciji\n"
                     "\nguest_rating - Lista top 10 najbolje ocenjenih hotela prema recenzijama\n"
                     "\nbest_deal - Lista top 10 hotela najbližih centru grada\n".format(user_input))
