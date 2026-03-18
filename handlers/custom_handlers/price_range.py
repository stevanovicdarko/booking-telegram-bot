from telebot.types import Message
from states.all_states import UserState
from loader import bot
from utils.handler_functions import is_connection_ok, parse_price_range, is_all_digit
from api_booking.endpoints import search_hotels, get_hotel_details, get_hotel_photo
from database.crud import store_data
from datetime import datetime

"""
Final handler in the search sequence.
Processes the price range, executes API requests for hotel data, 
displays results to the user, and logs the search in the database.
"""

@bot.message_handler(state=UserState.pricerange_state)
def handle_state(message: Message) -> None:
    """
    Finalizes the search parameters, fetches hotel data from Booking API,
    presents results to the user, and logs the search in the database.

    Args:
         message (Message): Telegram message object containing the price range
                            string (e.g., '50-150').


    """
    price_range = message.text

    # 1. Validation of price range input
    price_min, price_max = parse_price_range(price_range)
    if not price_min:
        bot.send_message(message.from_user.id, 'Raspon cena nije ispravno unet, pokušajte ponovo!')
        return

    if not is_all_digit(price_min, price_max):
        bot.send_message(message.from_user.id, 'Raspon cena nije ispravno unet, pokušajte ponovo!')
        return

    # 2. Logic for sorting based on the initial command chosen by user
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_search']['price_min'] = price_min
        data['new_search']['price_max'] = price_max

        if data['new_search']['command'] == 'lowprice':
            sort_type = "price"
        elif data['new_search']['command'] == 'guestrating':
            sort_type = 'bayesian_review_score'
        else:
            sort_type = 'distance'

    # 3. API Call: Fetch list of hotels
    response = search_hotels(data['new_search'], sort_type)

    if not is_connection_ok(response):
        bot.send_message(message.from_user.id, 'Greška u povezivanju sa serverom, pokušajte ponovo!')
        return

    hotels_id = response.json()
    if 'data' not in hotels_id.keys() or len(hotels_id['data']['hotels']) == 0:
        bot.send_message(message.from_user.id, 'Nažalost, nismo pronašli ništa što odgovara vašim kriterijumima.'
                                               ' Probajte sa drugim unosom.')
        bot.set_state(message.from_user.id, UserState.start_state)
        return

    hotel_catalogue = []

    # 4. Processing Results: Iterate through found hotels and fetch deep details
    for elemnts in hotels_id['data']['hotels']:
        hotel_catalogue.append({
            'hotel_id': elemnts['hotel_id'],
            'accessibilityLabel': elemnts['accessibilityLabel'],
            'price': elemnts['property']['priceBreakdown']['grossPrice']['value'],
            'currency': elemnts['property']['priceBreakdown']['grossPrice']['currency']
        })

    if not hotel_catalogue:
        bot.send_message(message.from_user.id, 'Nema rezultata za vašu pretragu.'
                                               'Izmenite parametre pretrage i pokušajte ponovo.')
        bot.set_state(message.from_user.id, UserState.start_state)
        return

    for elements in hotel_catalogue:
        with bot.retrieve_data(message.from_user.id) as data:
            arrival_date = data['new_search']["arrival_date"]
            departure_date = data['new_search']["departure_date"]
            response_1 = get_hotel_details(data['new_search'], elements)

        if not is_connection_ok(response_1):
            bot.send_message(message.from_user.id, 'Greška u povezivanju sa serverom, pokušajte ponovo!')
            return
        hotels_details = response_1.json()

        hotel_name = hotels_details['data']['hotel_name']
        hotel_url = hotels_details['data']['url']
        hotel_description = elements['accessibilityLabel']
        hotel_price = str(elements['price']) + ' ' + elements['currency']
        hotel_dates = str(arrival_date) + ' - ' + str(departure_date)
        hotel_coordinates = str(round(float(hotels_details['data']['latitude']), 4)) + ', ' + \
                            str(round(float(hotels_details['data']['longitude']), 4))

        # 5. Fetch and display photos
        response = get_hotel_photo(elements)
        if not is_connection_ok(response_1):
            bot.send_message(message.from_user.id, 'Greška u povezivanju sa serverom, pokušajte ponovo!')
            return

        hotels_photos = response.json()
        hotel_photos_catalogue = []

        for index in range(2):
            hotel_photos_catalogue.append(hotels_photos['data'][index]['url'])

        bot.send_message(message.from_user.id,
                         '{}\n{}\n{}\n{}\n{}\n{}\n'.format(
                             hotel_name, hotel_url, hotel_description, hotel_price, hotel_dates,
                             str('Coordinates: ') + hotel_coordinates))
        n = 1
        for image in hotel_photos_catalogue:
            bot.send_message(message.from_user.id, '<a href="{}">Фото {}</a>'.format(image, n), parse_mode='HTML')
            n += 1

        # 6. Database Storage: Log this hotel into user history
        store_data(search_user_id=message.from_user.id,
                   search_date=datetime.now(),
                   search_url=hotel_url,
                   search_hotel_title=hotel_description,
                   search_hotel_price=round(elements['price'], 2),
                   search_hotel_photos=hotel_photos_catalogue[0],
                   search_hotel_coordinates=hotel_coordinates
                   )
