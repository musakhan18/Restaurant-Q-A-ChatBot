import re
from word2number import w2n
from datetime import datetime
from dateutil import parser
import db_helper

def Processing(res):
    res = re.sub(r'.*<bot>:|Question:.*|<endofstring>.*', '', res).strip()
    return res

def extract_order_details(user_input):
    # Define a regular expression pattern to match quantity and item
    pattern = re.compile(r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s*([a-zA-Z\s]+?)(?=\band\b|\,|$)', re.IGNORECASE)
    
    # Find all matches in the user input
    matches = pattern.findall(user_input)
    
    # Convert word numbers to numeric form
    def convert_word_to_number(word):
        try:
            return str(w2n.word_to_num(word))
        except ValueError:
            return word
    
    # Process matches
    order_details = []
    for match in matches:
        quantity, item = match
        quantity = convert_word_to_number(quantity)
        order_details.append((quantity, item.strip()))

    return order_details


def Restaurants():
    if 'restaurants' not in locals():
        restaurants = {}
    else:
        restaurants = locals()['restaurants']

    restaurants_data = db_helper.get_restaurants_data()

    for data in restaurants_data:
        restaurant_name, fooditem_name, price, opening_time, closing_time = data

        # Check if the restaurant is already in the dictionary
        if restaurant_name not in restaurants:
            restaurants[restaurant_name] = {'dishes': [], 'timings_24': {'opening': opening_time, 'closing': closing_time}}

        # Append the dish information to the 'dishes' list
        restaurants[restaurant_name]['dishes'].append({'name': fooditem_name, 'price': price})

    return restaurants

def extract_reservation_info(user_input):
    # Define regular expressions
    number_of_people_pattern = re.compile(r'(\d+)\s*(person|people)?')
    name_pattern = re.compile(r'\b(name is|my name is|I am)\s+([a-zA-Z]+)\b')

    # Extract information using regex
    number_of_people_match = number_of_people_pattern.search(user_input)
    name_match = name_pattern.search(user_input)

    # Extracted information
    number_of_people = int(number_of_people_match.group(1)) if number_of_people_match else None
    name = name_match.group(2) if name_match else None
    date = extract_date(user_input)
    time=extract_time(user_input)

    return number_of_people, date, time, name


def extract_date(user_input):
    date_patterns = [
        r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b',
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s?\d{1,2}(?:st|nd|rd|th)?(?:,\s?\d{2,4})?\b',
        r'\b(\d{1,2}(?:st|nd|rd|th)?\s(?:January|February|March|April|May|June|July|August|September|October|November|December)(?:,\s?\d{2,4})?)\b',
    ]
    
    date_str = None

    for date_pattern in date_patterns:
        match = re.search(date_pattern, user_input, re.IGNORECASE)
        if match:
            date_str = match.group()
            break

    date = None
    if date_str:
        try:
            date = parser.parse(date_str).date()
            date=date.strftime("%Y-%m-%d")
        except ValueError:
            pass

    return date

def extract_time(user_input):
    time_pattern = re.compile(r'\bat\s+(\d{1,2}(?::\d{2})?\s*[APMapm]{2})\b')
    time_match = time_pattern.search(user_input)
    
    if time_match:
        time_str = time_match.group(1)
        
        # Check if there's a space between the hour and am/pm
        if ' ' in time_str:
            # If there is, replace the space with ''
            time_str = time_str.replace(' ', '')

        try:
            # Parse the time using dateutil.parser
            parsed_time = parser.parse(time_str).time()
            # Convert to SQL time format
            time = parsed_time.strftime("%H:%M:%S")
        except ValueError:
            time = None
    else:
        time = None

    return time


