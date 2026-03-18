from telebot import TeleBot
from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS

"""
Module for configuring the Telegram Bot's command menu.
This ensures that users can see and select available commands directly from the UI.
"""

def set_default_commands(bot: TeleBot) -> None:
    """
    Registers the default set of commands with the Telegram server.
    This updates the 'Menu' button in the user's chat interface.

    Args:
        bot (TeleBot): The initialized instance of the Telegram bot.

    Note:
        DEFAULT_COMMANDS should be a list of tuples, where each tuple
        contains ('command_name', 'description').
    """

    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
