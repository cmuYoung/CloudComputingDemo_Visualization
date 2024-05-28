from langchain.chains import LLMChain
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
from openai import OpenAI
import boto3
import json
import io
import os
import random
import time
import re
from time import sleep
import streamlit as st
import pydeck as pdk
import googlemaps
import os
import pandas as pd
import sqlite3
from streamlit_feedback import streamlit_feedback
import datetime
import base64
from PIL import Image
from st_pages import Page, Section, show_pages, add_page_title
from utils.oauth import oauth
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page
import folium
from streamlit_folium import folium_static

#st.set_page_config(page_title="Four Paws", page_icon="🐶")

# Optional -- adds the title and icon to the current page
#add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be

pages_to_show = [
    Page("CloudDemo.py", "CMU Cloud Computing Demo", "📌")
]

if 'auth' in st.session_state:
    pages_to_show.append(Page("fp_pages/show_stock_chart.py", "Stock Performance", "📈"))
    pages_to_show.append(Page("fp_pages/show_location_map.py", "Map Based on Location", "🗺️"))
    pages_to_show.append(Page("fp_pages/gaze_recorder.py", "Gaze Recorder", "📌"))
    pages_to_show.append(Page("fp_pages/manage_videos.py", "Manage Videos", "📌"))
    pages_to_show.append(Page("fp_pages/user_profile.py", "User Profile", "🔧"))

    st.session_state["admin_flag"] = 'Y'
    #if "admin_flag" in st.session_state:
    if True:
        if st.session_state["admin_flag"] == 'Y':
            pages_to_show.append(Section("Admin Settings", icon="🔧"))
            pages_to_show.append(Page("fp_pages/db_management_dashboard.py", "Database Management Dashboard", "🔧"))

# Show the selected pages
show_pages(pages_to_show)

add_page_title()


# Function to create a SQLite connection
def create_connection():
    conn = sqlite3.connect('videos.db')
    return conn

# Function to create a table if it doesn't exist
def create_table(conn):
    
    query = '''
    CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER PRIMARY KEY,
        ai_model_id TEXT,
        prompt_header_id INTEGER,
        name TEXT,
        address_line1 TEXT,
        address_line2 TEXT,
        city TEXT,
        state TEXT,
        country TEXT,
        email TEXT,
        phone TEXT,
        creation_date DATE,
        admin_flag VARCHAR(1) default 'N',
        zip_code INTEGER,
        interest_topics TEXT,
        birth_date DATE
    )
    '''
    conn.execute(query)

    query = '''
    CREATE UNIQUE INDEX IF NOT EXISTS user_profiles_U1
    ON user_profiles(email)
    '''
    conn.execute(query)
    conn.commit()

    cursor = conn.cursor()

    if 'payload' not in st.session_state:
        quit()

    # Define the sample record to insert
    full_name = st.session_state.payload["name"]
    email = st.session_state.payload["email"]
    sample_user_record = (full_name, 'gpt-3.5-turbo', email, datetime.datetime.now())

    print('++ name = ' + full_name)
    print('++ email = ' + email)
    print('++ STEP #1')

    # Insert the sample record if it doesn't already exist
    cursor.execute('''INSERT OR IGNORE INTO user_profiles (name, ai_model_id, email, creation_date) VALUES (?, ?, ?, ?)''', sample_user_record)

    user_id = fetch_user_id(conn, email)

    if user_id:
        st.session_state['user_id'] = user_id

    conn.commit()
    print('++ STEP #1.1')



# Function to fetch user_id  by email
def fetch_user_id(conn, email):
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM user_profiles WHERE email = ?', (email,))
    user_id = cursor.fetchone()[0]
    return user_id

# Function to fetch user profile by user_id
def fetch_user_profile(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
    return cursor.fetchone()

    return feedback

#####################################################################

# Main function to run the Streamlit app
def main():

    st.write(" ")
    st.write(" ")
    if 'auth' not in st.session_state:
        st.sidebar.markdown('''
        <span style="font-size:20px; font-weight:bold;">Hi, Welcome!</span>
        ''', unsafe_allow_html=True)
    else:
        given_name = st.session_state.payload["given_name"]
        st.sidebar.markdown(f'''
        <span style="font-size:20px; font-weight:bold;">Hi {given_name}, Let's See how exciting the project can be.</span>
        ''', unsafe_allow_html=True)

    st.sidebar.write("Use this tool to quickly find out...")

    # OAuth
    oauth()

    conn = create_connection()
    create_table(conn)

    if 'auth' not in st.session_state:
        quit()

    if 'auth' in st.session_state:
        user_id = fetch_user_id(conn, st.session_state.payload["email"])
        if user_id:
            st.session_state['user_id'] = user_id    

    user_profile = fetch_user_profile(conn, st.session_state.user_id)
    if user_profile:
        print(user_profile)
        name = user_profile[3]
        st.subheader(f'Hi {name}! Welcome to the website! You are logged in.')
        st.session_state['admin_flag'] = user_profile[12] #admin_flag
        print('ADMIN='+st.session_state['admin_flag'])
        if user_profile[13] and user_profile[6] and  user_profile[7]:
            st.session_state['zip_code'] = user_profile[13] #zip_code
            st.session_state['city_state'] = user_profile[6] + ', ' + user_profile[7]
            #print('ZIP_CODE='+st.session_state['zip_code'])
        if st.session_state['admin_flag'] == 'Y':
            if "admin_run" not in st.session_state:
                    st.session_state['admin_run'] = 'Y'
                    st.rerun()


    if 'zip_code' not in st.session_state:
        print('No zip code found')
        switch_page("user profile")

    # Log-out button
    if 'auth' in st.session_state:
        st.sidebar.write(" ")
        #st.write(st.session_state["payload"])
        if st.sidebar.button("Logout"):
            del st.session_state["auth"]
            del st.session_state["token"]
            del st.session_state["payload"]
            del st.session_state["user_id"]
            st.rerun()

    quit()


if __name__ == '__main__':
    main()
