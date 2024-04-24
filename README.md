# nasapi
As part of my final capstone project, I developed this application to better the process of collecing and visulizing data from the NASA API.
These were the steps I took to complete the application:
1) I wrote a python script that has functions to connect to my SQL database and functions to fetch the data from the offical NASA API.
2) I chose the astronomy picture of the day API and created a table in SQL to store the data in their respective columns according to the NASA API.
3) I then created a function in my script to fetch the data from the APOD NASA API and insert it into the SQL table.
4) I then created another python script where I query the SQL database with streamlit, and also customized my streamlit dashboard to visualize the data best.
5) This process is automated as I have uploaded the fetching API script onto a EC2 instance where a cron job is scheduled to run everyday so that a new image is pulled and displayed.
6) The final application is then hosted using Streamlit Cloud.
