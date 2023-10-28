import streamlit as st
import db_helper
import random
import helper

def display_restaurant_menu(restaurants):
    selected_restaurant = st.selectbox("Select a Restaurant", list(restaurants.keys()))
    st.header(f"Menu for {selected_restaurant}")
    for dish in restaurants[selected_restaurant]['dishes']:
        st.write(f"Name: {dish['name']},     Price: {dish['price']} Rs.")
    return selected_restaurant

def place_order_db(selected_restaurant, user_order_string):
    if user_order_string:
        user_order_matches = helper.extract_order_details(user_order_string)
        user_name = st.text_input("Enter your name:")
        user_address = st.text_area("Enter your address:")
        order_id = random.randint(1, 100)  # Assign the order ID
        if st.button("Place Order"):
            db_helper.insert_order_details(selected_restaurant, user_order_matches, order_id,user_name,user_address)
            order_summary(order_id,selected_restaurant,user_order_matches,user_name,user_address)
    
def order_summary(order_id,selected_restaurant,user_order_matches,user_name,user_address):
    totalPrice=db_helper.calculate_total_price(order_id)
    st.subheader("Order Summary:")
    st.write(f"Restaurant: {selected_restaurant}\n\n Order id: {order_id}")
    for quantity, item in user_order_matches:
        st.write(f"Item: {item},Quantity: {quantity}")
    st.write(f"Customer Name: {user_name}")
    st.write(f"Delivery Address: {user_address}")
    st.write(f"\nTotal Price: {totalPrice}")
    st.success("Order placed successfully!")

def place_order():
    restaurants=helper.Restaurants()
    selected_restaurant= display_restaurant_menu(restaurants)
    order_prompt = f"Write your order for {selected_restaurant}:"
    user_order_string = st.text_input(order_prompt)
    if user_order_string:
        place_order_db(selected_restaurant, user_order_string)