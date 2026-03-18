## 🏨 Telegram bot for searching hotels on Booking.com
This bot searches for hotels on the Booking.com platform according to the entered user preferences.
These include:
1. **City**
2. **Country**
3. **District** (via dynamic selection)
4. **Arrival date**
5. **Departure date**
6. **Price range** (from - to, budget per night)


After receiving the above data, the bot will provide the user with a list of hotels meeting these criteria.
> **🌐 Language Note:** While the codebase, architecture, and documentation are written in **English**, 
> the bot's interactive messages and user interface are in **Serbian**.

## 📺 Demo
Check out the bot in action:

https://github.com/user-attachments/assets/44d9b909-33af-4ff6-9b72-c6b3c134225b

*Note: The video shows a full search cycle from location selection to hotel results.*

## 🚀 How to Run the Bot

Follow these steps to set up and launch the bot on your local machine. This guide assumes you have **Python 3.8+** installed.

### 1. Clone the Repository
Open your terminal and run:
```bash
  git clone [URL_WHERE_THIS_IS_LOCATED]
```

### 2. Create a Virtual Environment(Recommended) 
It is best practice to run the bot in a virtual environment to keep dependencies organized:

#### Create the environment
```bash
  python -m venv venv
```

Activate it.

### 3.Install Required Packages
```bash
  pip install --upgrade pip
  pip install -r requirements.txt
```

### 4.Configuration (Environment Variables)

The bot uses a .env file to securely manage sensitive information.

1. Create a file named .env in the root directory.
2. Copy the structure from .env.template and add your real keys:

```bash
  BOT_TOKEN='your_telegram_bot_token_here'
  RAPID_API_KEY='your_rapidapi_key_here'
```
> **Note:** You can get your **BOT_TOKEN** from [@BotFather](https://t.me/BotFather) and the **API Key** from 
> the [Booking.com API on RapidAPI](https://rapidapi.com/DataCrawler/api/booking-com15).

### 5.Launch the Bot
Once the configuration is complete, start the bot by running:
```bash
  python main.py
```


## 🧠 Bot Algorithm
This bot uses a **Finite State Machine (FSM)** to manage user dialogues and ensure data integrity at each step.
> 📊 **Visual FSM Logic**: For a detailed overview of all states, transitions, and fallback mechanisms,
> please refer to the [FSM Logic Diagram](https://github.com/stevanovicdarko/booking-telegram-bot/blob/master/telebot_FSM.png)

This bot has several commands, each of which performs a specific function according to the following list:
1. /start        - launches the bot
2. /help         - provides a list of commands with their brief descriptions
3. /history      - provides the entire request history
4. /low_price    - sorts the received results by ascending price
5. /guest_rating - sorts the received results by guest reviews from best to worst
6. /best_deal    - sorts the received results by distance to the center from closest to farthest
By choosing one of the result filtration methods, the bot starts a dialogue with the user.
Within this dialogue, it receives all the necessary information to form a request and generate a result.
The commands /start, /help, and /history can be used by the user at any time.

### custom command:

**/low_price**

Description: Starts the scenario for searching hotels with the minimum price. After calling the command, 
the bot requests the city where the hotels need to be found. 
The chosen sorting method and user ID are saved in the internal state of the bot. 
The bot transitions the user to the UserState.city_state to wait for city input.

**/guest_rating**

Description: Starts the scenario for searching hotels with the best rating. After calling the command,
the bot requests the city where the hotels need to be found. 
The chosen sorting method and user ID are saved in the internal state of the bot. 
The bot transitions the user to the UserState.city_state to wait for city input.

**/best_deal**

Description: Starts the scenario for searching hotels with the shortest distance to the city center. 
After calling the command, the bot requests the city where the hotels need to be found.
The chosen sorting method and user ID are saved in the internal state of the bot. 
The bot transitions the user to the UserState.city_state to wait for city input.

#### Dialogue Scenarios

Regardless of the choice of /low_price, /guest_rating, or /best_deal commands,
the dialogue proceeds to the city request (UserState.city_state) and goes through the following stages:

##### City Input

Action:
Checking the correctness of the city name (is_valid_city_or_state_name)
In case of error — repeated input request
Saving the city and transitioning to the country request (UserState.country_state)

##### Country Input

Action:
Checking the country name (is_valid_city_or_state_name)
Request to the search_destination API to clarify the city
With parameters: {"query": 'city, country'}
Handling connection errors
If multiple matches are found — clarification request
Saving the city code (destination_id)
Request to the get_filter API to obtain a list of districts
With parameters: {"dest_id": 'City code',
              "search_type": 'Search type (city)',
              "arrival_date": 'Today',
              "departure_date": 'Tomorrow'}
Sending the user a keyboard with a list of districts
Transitioning to UserState.district_state

##### District Selection

Action:
Saving the district_id
Requesting the arrival date (UserState.arrival_state)

##### Arrival Date Input

Action:
Formatting and checking the date (format_date)
Prohibiting input of past dates
Transitioning to the departure date input (UserState.departure_state)

##### Departure Date Input

Action:
Checking the correctness of the date and ensuring it is later than the arrival date
Transitioning to the budget input (UserState.pricerange_state)

##### Price Range Input

Action:
Parsing the range (parse_price_range) and checking numeric values (is_all_digit)
Determining the sorting type (price / rating / distance)
Request to the search_hotels API
With parameters: {"dest_id": 'User ID',
              "search_type": 'City',
              "categories_filter": 'District',
              "arrival_date": 'Arrival date',
              "departure_date": 'Departure date',
              "price_min": 'Minimum price',
              "price_max": 'Maximum price',
              "sort_by": 'Sorting type according to the selected command (low_price, /guest_rating, /best_deal)',
              "currency_code": 'Currency code'}
Forming a list of hotels consisting of dictionaries with the following keys: hotel code, hotel title, price, currency code
Checking if the hotel list is populated
For each hotel, a request for detailed information is made (get_hotel_details)
With parameters: {"hotel_id": hotel code,
              "arrival_date": 'Arrival date',
              "departure_date": 'Departure date',
              "currency_code": "Currency code"}
Temporary storage of data about: hotel name, link to the hotel, hotel title, price, currency code, 
arrival date, departure date, and hotel location coordinates
Requesting photos (get_hotel_photo)
With parameters: {"hotel_id": hotel code}
Receiving hotel photos
Sending the user description, price, links, coordinates, and 5 photos
Saving search results in the database (store_data)

###### Price Range Input (Example)
User: /low_price
Bot: Enter the city you are interested in:
User: Belgrade
Bot: Enter the country:
...
Bot: Select the district you are interested in:
[Keyboard with districts]
...
Bot: Enter your arrival date in DD.MM.YYYY format:
...
Bot: Enter the budget per night from - to:
...
Bot: (Sending search results)

### default command:

**/start** - launches the bot

**/help** - provides a list of commands with their brief descriptions

**/history** - provides the entire request history

