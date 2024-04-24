import os
from re import S
import requests
import psycopg2
from dotenv import load_dotenv

dotenv_path = 'C:\\Users\\User\\NASAAPI\\NASAPI.env'
load_dotenv()

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
api_key = os.getenv('API_KEY')

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
    
# Function for inserting APOD data from API into SQL APOD Database
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

#Main
if __name__ == "__main__":
    api_key = 'b8dkKZ9Fcyhcl25Ekhmf1vzUEOuvGLg3FdkNerSJ'
    conn = get_db_connection()
    
    # Fetch & insert APOD data
    apod_data = fetch_data(api_key, 'planetary/apod') #Endpoint
    if apod_data:
        insert_apod_data(apod_data,conn)

    conn.close()