from msilib.text import tables
from dotenv import load_dotenv
import streamlit as st
import psycopg2
import pandas as pd
import os

dotenv_path = 'C:\\Users\\User\\NASAAPI\\NASAPI.env'
load_dotenv(dotenv_path)

# Function to get APOD Data
def get_apod_data():
    conn = psycopg2.connect(
        dbname = os.getenv('db_name'),
        user = os.getenv('db_user'),
        password = os.getenv('db_password'),
        host = os.getenv('db_host'),
        port=os.getenv('DB_PORT')
    )
    query = "SELECT * FROM ab_nasapi_apod ORDER BY date"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df  

# Streamlit Dashboard
def main():
    st.title('NASA Data Dashboard')
    df = get_apod_data()
 
    #APOD Data Tab
    if 'index' not in st.session_state:
        st.session_state.index = 0  # initialize index

    if not df.empty:
        # Buttons for navigation
        cols = st.columns([2, 7, 1])  # Adjusting column widths for better alignment
        with cols[0]:
            if st.button("Previous"):
                if st.session_state.index > 0:
                    st.session_state.index -= 1
        with cols[2]:  # This is the third column, which now contains the "Next" button
            if st.button("Next"):
                if st.session_state.index < len(df) - 1:
                    st.session_state.index += 1

        # Current image and details
        row = df.iloc[st.session_state.index]
        date = row['date'].strftime("%B %d, %Y")
        st.subheader(date)
        st.image(row['url'], caption=row['title'])
        st.write(row['explanation'])
    else:
        st.write("No data available")
             
if __name__ == "__main__":
    main()