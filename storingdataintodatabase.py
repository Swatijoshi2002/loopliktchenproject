import pandas as pd
import psycopg2  

# Connect to the database
conn = psycopg2.connect(database="your_database", user="your_user", password="your_password", host="your_host", port="your_port")
cursor = conn.cursor()

# Read and insert data from store_status.csv
store_status_df = pd.read_csv('store_status.csv')
store_status_records = store_status_df.to_dict('records')

for record in store_status_records:
    cursor.execute("INSERT INTO store_status (store_id, timestamp_utc, status) VALUES (%s, %s, %s)",
                   (record['store_id'], record['timestamp_utc'], record['status']))

# Read and insert data from business_hours.csv
business_hours_df = pd.read_csv('business_hours.csv')
business_hours_records = business_hours_df.to_dict('records')

for record in business_hours_records:
    cursor.execute("INSERT INTO business_hours (store_id, day_of_week, start_time_local, end_time_local) VALUES (%s, %s, %s, %s)",
                   (record['store_id'], record['dayOfWeek'], record['start_time_local'], record['end_time_local']))

# Read and insert data from store_timezones.csv
store_timezones_df = pd.read_csv('store_timezones.csv')
store_timezones_records = store_timezones_df.to_dict('records')

for record in store_timezones_records:
    cursor.execute("INSERT INTO store_timezones (store_id, timezone_str) VALUES (%s, %s)",
                   (record['store_id'], record['timezone_str']))

# Commit the changes and close the database connection
conn.commit()
cursor.close()
conn.close()
