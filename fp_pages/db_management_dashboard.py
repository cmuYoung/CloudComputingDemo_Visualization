import streamlit as st
import sqlite3
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page

# Optional -- adds the title and icon to the current page
add_page_title()

# Function to fetch and display table contents
def display_table_contents(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Display table headers
    columns = [description[0] for description in cursor.description]
    st.write(columns)

    # Display table contents
    for row in rows:
        st.write(row)

# Function to execute SQL query
def execute_query(conn, query):
    try:
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        return "Query executed successfully."
    except Exception as e:
        return str(e)

def main():
    #st.title('SQLite Table Viewer')

    if "auth" not in st.session_state:
        switch_page("login demo")

    # Connect to SQLite database
    conn = sqlite3.connect('videos.db')

    menu = ['View Tables', 'Perform SQL Table Alteration']
    default_ix = menu.index('View Tables')
    choice = st.sidebar.selectbox('Manage Tables', menu, index=default_ix)

    if choice == 'View Tables':

        st.subheader("View Tables")
        # List available tables
        table_names = [table[0] for table in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
        selected_table = st.sidebar.selectbox('Select Table', table_names)

        # Display selected table contents
        if selected_table:
            display_table_contents(conn, selected_table)

    elif choice == 'Perform SQL Table Alteration':
        st.subheader("Perform SQL Table Alteration")
        st.write("""
        Use this tool to execute SQL queries to alter tables.
        For example, you can use queries like:
        - ALTER TABLE table_name ADD COLUMN new_column_name column_type;
        - ALTER TABLE table_name DROP COLUMN column_name;
        """)

        # Text area for inputting SQL query
        query = st.text_area("Enter your SQL query here:")

        # Button to execute the query
        if st.button("Execute"):
            if query.strip() != "":
                result = execute_query(conn,query)
                st.write(result)
            else:
                st.write("Please enter a valid SQL query.")



    # Close connection
    conn.close()

if __name__ == '__main__':
    main()
