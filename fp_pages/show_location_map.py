import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import sqlite3
import datetime

# Function to get latitude and longitude from a zip code
def get_lat_lon_zip(zip_code):
    geolocator = Nominatim(user_agent="zip_code_locator")
    location = geolocator.geocode({"postalcode": zip_code, "country": "US"})
    return (location.latitude, location.longitude)

# Function to get latitude and longitude from an address
def get_lat_lon_address(address):
    geolocator = Nominatim(user_agent="address_locator")
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude)

# Function to fetch user profile by user_id
def fetch_user_profile(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
    return cursor.fetchone()

# Function to create a SQLite connection
def create_connection():
    conn = sqlite3.connect('videos.db')
    return conn

# Streamlit App
def main():
    st.title("Map Based on Location")
    
    # Selection bar for choosing input type
    input_type = st.radio("Choose input type:", ("Stored Location in User Table", "Zip Code", "Address"))
    
    # Input based on selection
    if input_type == "Stored Location in User Table":
        conn = create_connection()
        user_profile = fetch_user_profile(conn, st.session_state.user_id)
        if user_profile:
            zip_code = user_profile[13]
            if zip_code:
                try:
                    st.write('Stored Zip Code: '+str(zip_code))
                    lat, lon = get_lat_lon_zip(zip_code)
                    m = folium.Map(location=[lat, lon], zoom_start=12)
                    folium.Marker([lat, lon], popup=f"Zip Code: {zip_code}").add_to(m)
                    folium_static(m)
                except AttributeError:
                    st.error("Invalid Zip Code")
    elif input_type == "Zip Code":
        zip_code = st.text_input("Enter a US zip code:")
        if zip_code:
            try:
                lat, lon = get_lat_lon_zip(zip_code)
                m = folium.Map(location=[lat, lon], zoom_start=12)
                folium.Marker([lat, lon], popup=f"Zip Code: {zip_code}").add_to(m)
                folium_static(m)
            except AttributeError:
                st.error("Invalid Zip Code")
    elif input_type == "Address":
        address = st.text_input("Enter an address:")
        if address:
            try:
                lat, lon = get_lat_lon_address(address)
                m = folium.Map(location=[lat, lon], zoom_start=12)
                folium.Marker([lat, lon], popup=f"Address: {address}").add_to(m)
                folium_static(m)
            except AttributeError:
                st.error("Invalid Address")

if __name__ == "__main__":
    main()

