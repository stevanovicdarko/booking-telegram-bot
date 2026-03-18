from telebot.handler_backends import State, StatesGroup

"""
Definition of Finite State Machine (FSM) states.
These states track the user's progress through the hotel search dialogue.
Each state corresponds to a specific step in the data collection process.
"""

class UserState(StatesGroup):
    """
    StatesGroup representing the sequential flow of the bot's interaction.
    """

    start_state = State()
    city_state = State()
    country_state = State()
    district_state = State()
    arrival_state = State()
    departure_state = State()
    pricerange_state = State()