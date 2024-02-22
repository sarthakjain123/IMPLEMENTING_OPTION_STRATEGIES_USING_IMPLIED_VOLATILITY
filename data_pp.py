# sorted_on_symbol , spot_data

import os
import glob
import pandas as pd
from datetime import datetime, timezone

def convert_to_utc(row):
    date_str = f"{row['date']} {int(row['hour']):02d}:00"
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)

def unix_to_utc(unix_time):
    return datetime.utcfromtimestamp(int(unix_time) / 1000).replace(minute=0, second=0, microsecond=0, tzinfo=timezone.utc)

def extract_strike_price(strike_value):
    return strike_value.split('-')[1] if '-' in strike_value else None

if not os.path.exists('final_dat'):
    os.makedirs('final_dat')

# Create a dictionary for timestamps and spot prices from folder2
timestamp_spot_price = {}
for file_path in glob.glob('spot_data/*.csv'):
    df2 = pd.read_csv(file_path, header=None)
    df2['timestamp'] = df2[6].apply(unix_to_utc)
    for _, row in df2.iterrows():
        timestamp_spot_price[row['timestamp']] = row[4]

# Process files in folder1 and update with spot_price
for file_path in glob.glob('sorted_on_symbol/*.csv'):
    df1 = pd.read_csv(file_path)
    df1['timestamp'] = df1.apply(convert_to_utc, axis=1)
    df1['strike_price'] = df1['strike'].apply(extract_strike_price)

    df1['spot_price'] = df1['timestamp'].map(timestamp_spot_price)

    df1.to_csv(f"final_dat/{os.path.basename(file_path)}", index=False)

print("Processing complete. Modified files saved in 'final_dat' folder.")
