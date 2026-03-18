from states.all_states import UserState
from loader import bot
from telebot.types import CallbackQuery


@bot.callback_query_handler(func=None, state=UserState.district_state)
def handle_district(callback_query) -> None:
    """
    Handles the callback from the district selection keyboard.
    Extracts the district ID, confirms the choice, and prompts for arrival date.

    Args:
        callback_query (CallbackQuery): The Telegram callback object containing
                                        the data from the pressed button.
    """

    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    with bot.retrieve_data(callback_query.from_user.id) as data:
        data['new_search']['district_id'] = callback_query.data.split(',')[0]
    bot.send_message(callback_query.from_user.id, callback_query.data.split(',')[1])
    bot.send_message(callback_query.from_user.id, 'Molimo unesite datum dolaska (format: DD.MM.GGGG):')
    bot.set_state(callback_query.from_user.id, UserState.arrival_state)