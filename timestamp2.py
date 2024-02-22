#BTCUSDT-1h-2023-05-21


import pandas as pd
from datetime import datetime, timezone

# Read the CSV file without headers
df = pd.read_csv('BTCUSDT-1h-2023-05-21.csv', header=None)  

# Function to convert Unix timestamp (in milliseconds) to UTC and adjust minutes, seconds, and microseconds
def convert_to_utc_and_adjust(timestamp):
    try:
        # Convert Unix timestamp (in milliseconds) to seconds
        timestamp_in_seconds = timestamp / 1000
        # Convert to datetime in UTC
        utc_time = datetime.utcfromtimestamp(timestamp_in_seconds).replace(tzinfo=timezone.utc)
        # Set minutes, seconds, and microseconds to 00
        adjusted_time = utc_time.replace(minute=0, second=0, microsecond=0)
        return adjusted_time
    except Exception as e:
        print(f"Error processing timestamp: {timestamp}, Error: {e}")
        return None

# Apply the conversion function to the 7th column (index 6)
df['timestamp'] = df[6].apply(convert_to_utc_and_adjust)

# Save the modified DataFrame to a new CSV file
output_file = 'output_with_timestamps1.csv'  
df.to_csv(output_file, index=False)

print(f"File saved as {output_file}")
