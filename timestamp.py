import pandas as pd
from datetime import datetime, timezone

# Read the CSV file
df = pd.read_csv('sorted_BTC-240628-31000-P.csv')  
# Function to handle the date and hour formatting
def convert_to_utc(row):
    try:
        # Constructing the date-time string and converting to datetime object
        datetime_str = f"{row['date']} {int(row['hour']):02d}:00"
        timestamp = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        return timestamp
    except ValueError as e:
        # Print error for debugging
        print(f"Error processing row: Date: {row['date']}, Hour: {row['hour']}, Error: {e}")
        return None

# Convert to UTC timestamp and create a new column
df['timestamp'] = df.apply(convert_to_utc, axis=1)

# Save the modified DataFrame to a new CSV file
output_file = 'output_with_timestamps.csv' 
df.to_csv(output_file, index=False)

print(f"File saved as {output_file}")
