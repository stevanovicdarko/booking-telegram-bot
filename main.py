import loader
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter
import handlers

"""
Main Entry Point.
This script orchestrates the bot's startup by registering commands, 
applying custom filters, and initiating the polling loop.
"""

if __name__ == '__main__':
    print('TeleBot start working')

    set_default_commands(loader.bot)
    loader.bot.add_custom_filter(StateFilter(loader.bot))

    loader.bot.infinity_polling()

    print('TeleBot end working')

