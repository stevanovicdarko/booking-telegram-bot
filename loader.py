from telebot import TeleBot
from telebot import StateMemoryStorage
from config_data import config
from database.model import create_db_and_tabels

"""
Bot Loader Module.
This module initializes the core components of the bot, including FSM storage,
the bot instance itself, and the database infrastructure.
"""

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
create_db_and_tabels()
