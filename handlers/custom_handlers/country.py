from telebot.types import Message
from states.all_states import UserState
from loader import bot
from utils.handler_functions import is_valid_city_or_state_name, is_connection_ok
from api_booking.endpoints import search_destination, get_filter
from datetime import date, timedelta
from keyboards.district_keyboard import gen_markup

"""
Handler for country input and destination resolution.
This module validates the country, communicates with Booking API to find the destination ID,
and fetches available districts for the selected city.
"""

@bot.message_handler(state=UserState.country_state)
def handle_country(message: Message) -> None:
    """
    Processes country input, retrieves destination ID, and presents district options via inline keyboard.

    Args:
        message (Message): Telegram message object containing the country name.
    """

    country = message.text

    # 1. Validation of country name string
    if not is_valid_city_or_state_name(country):
        bot.send_message(message.from_user.id, 'Neispravan naziv države, pokušajte ponovo!')
        return
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_search']['country'] = country

    # 2. API Call: Search for the destination ID based on City and Country
    response = search_destination(data['new_search'])

    if not is_connection_ok(response):
        bot.send_message(message.from_user.id, 'Problem sa vezom. Molimo unesite državu ponovo.')
        return

    # 3. Filtering the API response to find an exact match
    city_info = response.json()
    cities_catalogue = []
    try:
        for elem in city_info['data']:
            if elem['search_type'] == 'city' and \
                    elem['city_name'].lower() == data['new_search']['city'].lower() and \
                    elem['country'].lower() == data['new_search']['country'].lower():
                cities_catalogue.append({'city_name': elem['city_name'],
                                         'country_name': elem['country'],
                                         'dest_id': elem['dest_id']
                                         })
    except BaseException('API FAILURE'):
        bot.send_message(message.from_user.id, 'Greška u povezivanju sa serverom. Unesite grad ponovo.')
        return

    # 4. Handling Ambiguity: Ensure only one clear match is found
    if len(cities_catalogue) != 1:
        bot.send_message(message.from_user.id, 'Nije moguće precizno odrediti grad. '
                                               'Molimo vas da jasnije navedete naziv grada i države.'
                                               )
        bot.set_state(message.from_user.id, UserState.city_state)
        return

    # 5. API Call: Fetch districts (filters) for the verified destination
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_search']['destination_id'] = cities_catalogue[0]['dest_id']

        response = get_filter(data['new_search'])

        if not is_connection_ok(response):
            bot.send_message(message.from_user.id, 'Problem sa vezom. Molimo unesite državu ponovo.')
            return

        # 6. Extracting districts to build the Inline Keyboard
        filter_info = response.json()
        districts_catalogue = {}

        for filters in filter_info['data']['filters']:
            if filters['field'] == 'di':
                for districts in filters['options']:
                    districts_catalogue[districts['title']] = districts['genericId'] + ',' + districts['title']

        # 7. Presenting the districts and transitioning state
        bot.send_message(message.from_user.id, 'Izaberite željenu opštinu: ',
                         reply_markup=gen_markup(districts_catalogue))
        bot.set_state(message.from_user.id, UserState.district_state)