import os
from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    print('Environment variables not loaded, because .env file is missing')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

DEFAULT_COMMANDS = (
    ('start', 'Pokreni bota'),
    ('help', 'Pomoć'),
    ('low_price', 'Spisak najjeftinijih hotela koji odgovaraju vašoj lokaciji'),
    ('guest_rating', 'Spiask najbolje ocenjenih hotela koji odgovaraju vašoj lokaciji'),
    ('best_deal', 'Najbolji odnos cene i lokacije, blizu centra a i solidna cena'),
    ('history', 'Prikaži istoriju tvojih pretraga')
)

API_HEADERS = {
    "x-rapidapi-key": os.getenv('RAPID_API_KEY'),
    "x-rapidapi-host": os.getenv('RAPID_API_HOST')
}

API_URLS = {
    "search_destination": "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination",
    "get_filter": "https://booking-com15.p.rapidapi.com/api/v1/hotels/getFilter",
    "search_hotels": "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels",
    "get_hotel_details": "https://booking-com15.p.rapidapi.com/api/v1/hotels/getHotelDetails",
    "get_hotel_photos": "https://booking-com15.p.rapidapi.com/api/v1/hotels/getHotelPhotos"
}