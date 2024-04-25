import os
from re import S
import requests
import psycopg2
from dotenv import load_dotenv

dotenv_path = 'C:\\Users\\User\\NASAAPI\\NASAPI.env'

# Load environment variables from the specified path
load_dotenv(dotenv_path)

# Function for SQL Database Connection
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

# Function for fetching data from the NASA API
def fetch_data(api_key, endpoint):
    url = f"https://api.nasa.gov/{endpoint}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
# Function for inserting Astronomy Picture of the Day data from API into SQL APOD Database
def insert_apod_data(data, conn):
    cursor =  conn.cursor()
    cursor.execute("""
        INSERT INTO ab_nasapi_apod (date, explanation, title, url, media_type, hdurl)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (date) DO UPDATE SET
        explanation = EXCLUDED.explanation,
        title = EXCLUDED.title,
        url = EXCLUDED.url,
        media_type = EXCLUDED.media_type,
        hdurl = EXCLUDED.hdurl;
    """, (data['date'], 
          data['explanation'], 
          data['title'], data['url'], 
          data['media_type'], 
          data['hdurl']))
    conn.commit()
    cursor.close()

# Function for inserting DONKI Solar Flare data from API into SQL DSF Database
def insert_dsf_data(data, conn):
    cursor = conn.cursor()
    for event in data:  
        cursor.execute("""
            INSERT INTO ab_nasapi_dsf (flr_id, begin_time, peak_time, end_time, class_type, source_location, active_region_num, note, submission_time, link)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (flr_id) DO UPDATE SET 
            begin_time = EXCLUDED.begin_time,
            peak_time = EXCLUDED.peak_time,
            end_time = EXCLUDED.end_time,
            class_type = EXCLUDED.class_type,
            source_location = EXCLUDED.source_location,
            active_region_num = EXCLUDED.active_region_num,
            note = EXCLUDED.note,
            submission_time = EXCLUDED.submission_time,
            link = EXCLUDED.link;
        """, (event['flrID'],
              event['beginTime'],
              event['peakTime'],
              event['endTime'],
              event['classType'],
              event['sourceLocation'],
              event['activeRegionNum'],
              event['note'],
              event['submissionTime'],
              event['link']))
        conn.commit()
    cursor.close()


#Main
if __name__ == "__main__":
    api_key = os.getenv('API_KEY')
    conn = get_db_connection()
    
    # Fetch & insert APOD data
    apod_data = fetch_data(api_key, 'planetary/apod') #Endpoint
    if apod_data:
        insert_apod_data(apod_data,conn)
        
    # Fetch & insert DSF data
    dsf_data = fetch_data(api_key, 'DONKI/FLR') #Endpoint
    if dsf_data:
        insert_dsf_data(dsf_data, conn)

    conn.close()
