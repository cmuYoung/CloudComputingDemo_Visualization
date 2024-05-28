import streamlit as st
import pandas as pd
import sqlite3
import datetime
import time
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Manage Videos", page_icon="🔧")

# Optional -- adds the title and icon to the current page
add_page_title()


#logo_path = 'images/FourPaws_LogoWhite.png'
#st.sidebar.image(logo_path, width=300)

#st.image(logo_path, width=300)
st.write(" ")
st.write(" ")

# Define mapping of original column names to friendly column headers
column_headers_map = {
        'video_id': 'Video ID',
        'name': 'Name',
        'description': 'Description',
    }

columns_to_delete = ['user_id', 'video_id', 'creation_date']

# Function to create a SQLite connection
def create_connection():
    conn = sqlite3.connect('videos.db')
    return conn

# Function to create a table if it doesn't exist
def create_table(conn):
    query = '''
    CREATE TABLE IF NOT EXISTS videos (
        video_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        name TEXT,
        description TEXT,
        creation_date DATE
    )
    '''
    conn.execute(query)

    query = '''
    CREATE INDEX IF NOT EXISTS videos_N1
    ON videos(user_id)
    '''
    conn.execute(query)

def fetch_videos(conn, user_id):
    query = 'SELECT * FROM videos WHERE user_id = ?'
    videos_df = pd.read_sql(query, conn, params=(user_id,))
    return videos_df

def fetch_video(conn, video_id):
    query = 'SELECT * FROM videos WHERE video_id = ?'
    videos_df = pd.read_sql(query, conn, params=(video_id,))
    return videos_df

def cleanup_df(df):
    df.drop(columns=columns_to_delete, inplace=True)
    df.rename(columns=column_headers_map, inplace=True)
    return df

# Function to add a video to the database
def add_video(conn, name, description):
    query = 'INSERT INTO videos (user_id, name, description, creation_date) VALUES (?, ?, ?, ?)'
    conn.execute(query, (st.session_state['user_id'], name, description, datetime.datetime.now()))
    conn.commit()

# Function to delete a video from the database
def delete_video(conn, video_id):
    query = 'DELETE FROM videos WHERE video_id = ?'
    conn.execute(query, (video_id,))
    conn.commit()

# Function to edit a video's information
def edit_video(conn, video_id, name, description):
    query = 'UPDATE videos SET name=?, description=? WHERE video_id=?'
    conn.execute(query, (name, description, video_id))
    conn.commit()

# Main function to run the app
def main():
    #st.title('Manage Videos')

    if "auth" not in st.session_state:
        switch_page("login demo")

    conn = create_connection()
    create_table(conn)

    videos_df = fetch_videos(conn, st.session_state['user_id'])

    menu = ['View Videos', 'Add Video', 'Edit Video', 'Delete Video']
    default_ix = menu.index('View Videos')

    if videos_df.empty:
        #st.write('No videos')
        default_ix = menu.index('Add Video')
        msg = st.toast('No videos have been registered!', icon='❗')
        time.sleep(2)
        msg.toast('Please register your videos.', icon='😍')
    else:
        #st.write('videos are there.')
        default_ix = menu.index('View Videos')

        # Prepare the list for the selectbox
    video_options = [(f"{row['name']} ({row['description']})", row['video_id']) for _, row in videos_df.iterrows()]
    video_names = [option[0] for option in video_options]

    choice = st.sidebar.selectbox('Manage Videos', menu, index=default_ix)
   
    if choice == 'View Videos':
        st.subheader('View Videos')
        df = cleanup_df(videos_df)
        st.write(df)

    elif choice == 'Add Video':
        st.subheader('Add Video')
        name = st.text_input('Name')
        description = st.text_input('Description')
        if st.button('Confirm'):
            add_video(conn, name, description)
            st.success('Video added successfully!')
            st.toast('You can click Home in the menu.', icon='✅')

    elif choice == 'Edit Video':
        st.subheader('Edit Video')
        selected_video_name = st.sidebar.selectbox("Select a video to edit", video_names)
        selected_video_id = next(video_id for video_name, video_id in video_options if video_name == selected_video_name)
        selected_video = videos_df[videos_df['video_id'] == selected_video_id].iloc[0]
        name = st.text_input('Name', value=selected_video['name'])
        description = st.text_input('Description', value=selected_video['description'])

        if st.button('Confirm'):
            edit_video(conn, selected_video_id, name, description)
            st.success('Video information updated successfully!')

    elif choice == 'Delete Video':
        st.subheader('Delete Video')
        selected_video_name = st.sidebar.selectbox("Select a video to delete", video_names)
        selected_video_id = next(video_id for video_name, video_id in video_options if video_name == selected_video_name)

        videos_df = fetch_video(conn, selected_video_id)
        df = cleanup_df(videos_df)
        st.write(df)
        # Display data in Streamlit
        #for col in df.columns:
        #    st.write(f"**{col}**: {df[col].iloc[0]}")

        if st.button('Confirm'):
            delete_video(conn, selected_video_id)
            st.success('Video deleted successfully!')

    conn.close()

if __name__ == '__main__':
    main()

