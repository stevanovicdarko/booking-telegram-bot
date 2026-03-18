from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict


"""
Module for generating dynamic inline keyboards.
Specifically used for displaying district selections.
"""

def gen_markup(buttons_info: Dict[str, str]) -> InlineKeyboardMarkup:
    """
    Generates an InlineKeyboardMarkup based on a dictionary of button labels and callbacks.

    Args:
        buttons_info (dict): A dictionary where:
            - Key (str): The text displayed on the button.
            - Value (str): The callback_data sent to the bot when clicked.

    Returns:
        InlineKeyboardMarkup: A ready-to-send Telegram keyboard object.
    """
    keyboard = InlineKeyboardMarkup()

    for text_keyboard, callback_keyboard in buttons_info.items():
        button = InlineKeyboardButton(text=text_keyboard, callback_data=callback_keyboard)
        keyboard.add(button)
    return keyboard
