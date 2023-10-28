from langchain_helper import chain
import streamlit as st
import order_helper as oh
import reservation_helper as rh
import helper

st.title("Restaurants Q&A ChatBot")
prompt = st.text_input("Enter Your Question")

if prompt:
    if "order" in prompt.lower():
        st.header("Place an Order")
        oh.place_order()

    elif "reservation" in prompt.lower() or "booking" in prompt.lower() or "book" in prompt.lower():
        st.header("Make Reservation")
        rh.make_reservation()
        
    else:
        res = chain(prompt)
        st.write(helper.Processing(res))
