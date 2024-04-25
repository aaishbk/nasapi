from itertools import takewhile
import streamlit as st
import psycopg2
import pandas as pd
import os
import plotly.express as px  
from dotenv import load_dotenv

dotenv_path = 'C:\\Users\\User\\NASAAPI\\NASAPI.env'
load_dotenv(dotenv_path)

# Function to get APOD Data
def get_apod_data():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    query = "SELECT * FROM ab_nasapi_apod ORDER BY date"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df  

# Function to get DSF data
def get_dsf_data():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    query = "SELECT * FROM ab_nasapi_dsf ORDER BY begin_time"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Streamlit Dashboard
def main():
    st.title('NASA Data Dashboard')
    
    tab1, tab2 = st.tabs(["Astronomy Picture of the Day", "Solar Flare Activity"])
            
    #APOD Data Tab
    with tab1:
        df_apod = get_apod_data()
        if 'index' not in st.session_state:
            st.session_state.index = 0  

        if not df_apod.empty:
            cols = st.columns([2, 7, 1]) 
            with cols[0]:
                if st.button("Previous"):
                    if st.session_state.index > 0:
                        st.session_state.index -= 1
            with cols[2]:  
                if st.button("Next"):
                    if st.session_state.index < len(df_apod) - 1:
                        st.session_state.index += 1

            # Current image and details
            row = df_apod.iloc[st.session_state.index]
            date = row['date'].strftime("%B %d, %Y")
            st.subheader(date)
            st.image(row['url'], caption=row['title'])
            st.write(row['explanation'])
        else:
            st.write("No data available")
     
    with tab2:
        df_solar = get_dsf_data()
        if not df_solar.empty:
            # Displaying information on most recent flare
            st.header(f"**Total Solar Flares Recorded:** {len(df_solar)}")
            most_recent_flare = df_solar.iloc[0]
            st.subheader(f"**Most Recent Flare Details:**")
            st.write(f"**Class Type:** {most_recent_flare['class_type']}")
            st.write(f"**Start Time:** {most_recent_flare['begin_time']}")
            st.write(f"**Peak Time:** {most_recent_flare['peak_time']}")
            st.write(f"**End Time:** {most_recent_flare['end_time']}")
            st.write(f"**Source Location:** {most_recent_flare['source_location']}")
            
            # Plotting the data
            st.subheader("**Solar Flare Activity Over Time**")
            fig = px.line(df_solar, x='begin_time', y=pd.Categorical(df_solar['class_type']).codes, 
                          labels={'y': 'Flare Class Code', 'x': 'Date'}, 
                          title='Solar Flare Classifications Over Time')
            fig.update_traces(mode='markers+lines')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No Solar Flare data available")

if __name__ == "__main__":
    main()
