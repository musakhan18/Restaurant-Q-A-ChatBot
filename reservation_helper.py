import streamlit as st
import db_helper
from datetime import datetime
import helper

def select_restaurant():
    restaurants = helper.Restaurants()
    selected_restaurant = st.selectbox("Select a Restaurant", list(restaurants.keys()))
    timings = restaurants[selected_restaurant]['timings_24']
    st.write(f"{selected_restaurant} Timings:")
    for time_type, time_value in timings.items():
        st.write(f"{time_type.capitalize()} Time: {time_value}")
    return selected_restaurant

def take_booking_details(selected_restaurant):
    booking_prompt = f"Write your Booking Details for {selected_restaurant}:"
    user_input = st.text_input(booking_prompt)
    return helper.extract_reservation_info(user_input)

def check_details(people, date,time,name):
    if not people:
        people = st.number_input("Enter the number of people:", min_value=1, step=1,key="num_people")

    if not date:
        date_str = st.text_input("Enter the reservation date (YYYY-MM-DD):",key="date_input")
        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
    
    if not time:
        time_str = st.text_input("Enter the reservation time (HH:MM AM/PM):",  key="time_input")
        time = datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M:%S") if time_str else None

    if not name:
        name = st.text_input("Enter your name:", key="name_input")
    
    return people, date,time,name

def take_user_input():
    selected_restaurant = select_restaurant()
    booking_prompt = f"Write your Booking Details for {selected_restaurant}:"
    user_input = st.text_input(booking_prompt)
     
    return selected_restaurant,user_input
        
def extract_info(selected_restaurant, user_input):
    people, date, time, name = helper.extract_reservation_info(user_input)
    people, date, time, name = check_details(people, date, time, name)
    return selected_restaurant,time, date, people, name

def order_reservation(selected_restaurant,time, date, people, name):
    st.subheader("Reservation Summary:")
    st.write(f"Restaurant: {selected_restaurant}")
    st.write(f"Customer Name: {name}")
    st.write(f"Number of People: {people}")
    st.write(f"Reservation Time: {time}")
    st.write(f"Reservation Date: {date}")
    st.success("Reservation placed successfully!")

def make_reservation():
    selected_restaurant,user_input=take_user_input()
    if user_input:
        selected_restaurant,time, date, people, name=extract_info(selected_restaurant,user_input)
        if st.button("Place Reservation"):
            db_helper.add_reservation(selected_restaurant,time, date, people, name)
            order_reservation(selected_restaurant,time, date, people, name)
    