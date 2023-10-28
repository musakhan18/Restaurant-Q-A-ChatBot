from datetime import timedelta,datetime
import mysql.connector
import decimal
import helper
global cnx

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="restaurant_chatbot"
)

# Create a cursor
cursor = conn.cursor()

def get_res_id(restaurant_name):
    try:
        cursor.execute("SELECT restaurant_id FROM Restaurants WHERE restaurant_name = %s", (restaurant_name,))
        result = cursor.fetchone()

        if result is not None:
            restaurant_id = result[0]
            return restaurant_id
        else:
            # Handle the case where no result is found (restaurant not in the database)
            return None

    except mysql.connector.Error as err:
        # Handle MySQL errors
        print(f"MySQL Error: {err}")
        return None


# Function to get IDs
def get_ids(restaurant_name, item_name):
    restaurant_id=get_res_id(restaurant_name)
    if restaurant_id:
        cursor.execute("SELECT item_id, price FROM FoodItems WHERE restaurant_id = %s AND item_name = %s", (restaurant_id, item_name))
        item_data = cursor.fetchone()
        if item_data:
            return restaurant_id, item_data[0], item_data[1], item_name

    return None

# Function to insert order details
def insert_order_details(restaurant_name, order_details, order_id,c_name,c_address):
    for quantity, item_name in order_details:
        print("\n", restaurant_name, item_name, "\n")
        ids = get_ids(restaurant_name, item_name)
        if ids:
            restaurant_id, item_id, price, food_item_name = ids
            quantity = int(quantity)
            price = float(price)
            total_price = quantity * price
            cursor.execute("INSERT INTO orders (order_id,restraurant_name,item_id,food_item_name ,quantity, total_price,c_name,c_address) VALUES (%s, %s, %s, %s, %s, %s,%s,%s)",
                           (order_id,restaurant_name,item_id,food_item_name,quantity, decimal.Decimal(str(total_price)),c_name,c_address))
            conn.commit()
            print("Order details inserted successfully.")
        else:
            print("Restaurant or item not found.")

def calculate_total_price(order_id):
    cursor.execute("SELECT SUM(total_price) FROM orders WHERE order_id = %s", (order_id,))
    total_price = cursor.fetchone()[0]
    return total_price

def add_reservation(restaurant_name, reservation_time, reservation_date, number_of_people, customer_name):
    cursor.execute("SELECT restaurant_id FROM Restaurants WHERE restaurant_name = %s", (restaurant_name,))
    restaurant_id = cursor.fetchone()[0]

    # Insert reservation details into Reservations table
    cursor.execute("""
        INSERT INTO Reservations 
        (restaurant_id, restaurant_name, reservation_time, reservation_date, number_of_people, customer_name) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (restaurant_id, restaurant_name, reservation_time, reservation_date, number_of_people, customer_name))

    # Commit the changes
    conn.commit()

def get_restaurants_data():
    cursor.execute("""
    SELECT r.restaurant_name, f.item_name, f.price, t.opening_time, t.closing_time
    FROM Restaurants r
    JOIN FoodItems f ON r.restaurant_id = f.restaurant_id
    JOIN Timings t ON r.restaurant_id = t.restaurant_id
""")

    restaurants_data = cursor.fetchall()
    return restaurants_data


# def add_timings():
#     restaurants=helper.Restaurants()
#     for restaurant_name, data in restaurants.items():
#         opening_time = data['timings_24']['opening']
#         closing_time = data['timings_24']['closing']

#     # Get restaurant_id from Restaurants table
#         cursor.execute("SELECT restaurant_id FROM Restaurants WHERE restaurant_name = %s", (restaurant_name,))
#         restaurant_id = cursor.fetchone()[0]

#     # Insert timings into Timings table
#         cursor.execute("INSERT INTO Timings (restaurant_id, opening_time, closing_time) VALUES (%s, %s, %s)",
#                    (restaurant_id, opening_time, closing_time))

# # Commit the changes
#     conn.commit()
