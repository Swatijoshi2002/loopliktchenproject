import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone

# Function to generate the report
def generate_report():
    # Load data from the database into Pandas DataFrames
    store_status_df = pd.read_csv('path/to/store_status.csv')
    business_hours_df = pd.read_csv('path/to/business_hours.csv')
    store_timezones_df = pd.read_csv('path/to/store_timezones.csv')

    # Merge data sources to get complete information
    merged_df = store_status_df.merge(business_hours_df, on='store_id', how='left')
    merged_df = merged_df.merge(store_timezones_df, on='store_id', how='left')

    # Set the current timestamp as the maximum timestamp from store_status_df
    current_timestamp = pd.to_datetime(store_status_df['timestamp_utc']).max()

    # Adjust the current timestamp to UTC
    current_timestamp = current_timestamp.tz_localize('UTC')

    # Initialize report data
    report_data = []

    # Iterate over each store
    for store_id, group_df in merged_df.groupby('store_id'):
        # Get the store's timezone
        timezone_str = group_df['timezone_str'].iloc[0]

        # Set the timezone for datetime operations
        tz = timezone(timezone_str)

        # Filter data within the last week
        week_start = current_timestamp - timedelta(days=7)
        store_df = group_df[group_df['timestamp_utc'] >= week_start]

        # Calculate the time range for the report
        report_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        report_end = current_timestamp.replace(hour=23, minute=59, second=59, microsecond=0)

        # Calculate business hours within the report time range
        business_hours_df = store_df[
            (store_df['dayOfWeek'] == report_start.weekday()) |
            (store_df['dayOfWeek'] == report_end.weekday())
        ]

        # Generate the report for each day within the report time range
        current_day = report_start
        while current_day <= report_end:
            # Filter data for the current day
            day_df = business_hours_df[business_hours_df['dayOfWeek'] == current_day.weekday()]

            # Get the start and end times for the current day
            if len(day_df) > 0:
                start_time = tz.localize(datetime.combine(current_day.date(), day_df['start_time_local'].iloc[0]))
                end_time = tz.localize(datetime.combine(current_day.date(), day_df['end_time_local'].iloc[0]))
            else:
                # If no data available, assume the store is open 24/7
                start_time = tz.localize(datetime.combine(current_day.date(), datetime.min.time()))
                end_time = tz.localize(datetime.combine(current_day.date(), datetime.max.time()))

            # Filter data within the business hours of the current day
            day_data = store_df[
                (store_df['timestamp_utc'] >= start_time) &
                (store_df['timestamp_utc'] <= end_time)
            ]

            # Calculate uptime and downtime for the current day
            uptime_minutes = calculate_uptime_minutes(day_data, start_time, end_time)
            downtime_minutes = calculate_downtime_minutes(start_time, end_time, uptime_minutes)

            # Add the day's report data to the report list
            report_data.append({
                'store_id': store_id,
                'uptime_last_hour
