import streamlit as st
import sqlite3
import datetime
import pandas as pd
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page
import requests

st.set_page_config(page_title="User Profile", page_icon="🔧")

# Optional -- adds the title and icon to the current page
add_page_title()

# Function to create a SQLite connection
def create_connection():
    conn = sqlite3.connect('videos.db')
    return conn

# Function to edit a user's information
def edit_user_profile(conn, user_id, name, addr1, addr2, zip_code, city, state, country, email, phone, interest_topics, birth_date):
    query = 'UPDATE user_profiles SET name=?, address_line1=?, address_line2=?, zip_code=?, city=?, state=?, country=?, email=?, phone=?, interest_topics=?, birth_date=? WHERE user_id=?'
    conn.execute(query, (name, addr1, addr2, zip_code, city, state, country, email, phone, interest_topics,birth_date, user_id))
    conn.commit()

# Function to fetch user profile by user_id
def fetch_user_profile(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
    return cursor.fetchone()

# Function to get city and state from ZIP code
def get_city_state_country(zip_code):
    try:
        response = requests.get(f"http://api.zippopotam.us/us/{zip_code}")
        if response.status_code == 200:
            data = response.json()
            city = data['places'][0]['place name']
            state = data['places'][0]['state']
            #country = data['country']
            country = 'US'
            return city, state, country
        else:
            return None, None, None
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None, None, None

# Main function to run the app
def main():

    if "auth" not in st.session_state:
        switch_page("four paws")

    conn = create_connection()

    st.subheader('Edit User Profile')

    #st.session_state['user_id'] = 2
    #st.write(st.session_state.user_id[0])

    #st.write(st.session_state.user_id)

    user_profile = fetch_user_profile(conn, st.session_state.user_id)
    #st.write(user_profile)

    if user_profile:
        name = st.text_input('Name', value=user_profile[3])
        addr1 = st.text_input('Address Line1', value=user_profile[4])
        #addr2 = st.text_input('Address Line2', value=user_profile[5])
        addr2 = ""

        if not user_profile[13]:
            st.success('Please enter your ZIP code for personalized service.')

        zip_code = st.text_input('Zip Code', value=user_profile[13])

        val_city = None
        val_state = None
        val_country = None

        if zip_code:
            val_city, val_state, val_country = get_city_state_country(zip_code)
            if val_city and val_state and val_country:
                st.caption(f"{val_city}, {val_state} {zip_code} {val_country}")
            else:
                st.error("Invalid ZIP code or data not found.")

            #if val_city:
            #    city = st.text_input('City', value=val_city, disabled=True)
            #if val_state:
            #    state = st.text_input('State', value=val_state, disabled=True)
            #if val_country:
            #    country = st.text_input('Country', value=val_country, disabled=True)

        email = st.text_input('Email', value=user_profile[9], disabled=True)
        phone = st.text_input('Phone', value=user_profile[10])
        interest_topics = st.text_input('Interest Topics', value=user_profile[14])
        birth_date = st.date_input('Birth Date', value=pd.to_datetime(user_profile[15]))

        if st.button('Confirm'):
            if zip_code:
                edit_user_profile(conn, st.session_state.user_id, name, addr1, addr2, zip_code, val_city, val_state, val_country, email, phone, interest_topics, birth_date)
                st.success('User profile information updated successfully!')
            else:
                st.error("Please fill out your ZIP code.")

if __name__ == '__main__':
    main()
