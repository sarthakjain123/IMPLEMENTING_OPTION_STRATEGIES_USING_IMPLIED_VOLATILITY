import os
import shutil
import glob
import pandas as pd

folder_path = 'final_dat'  # Replace with the path to your folder
put_data_folder = 'put_data'
call_data_folder = 'call_data'

# Create the 'put_data' and 'call_data' folders if they don't exist
os.makedirs(put_data_folder, exist_ok=True)
os.makedirs(call_data_folder, exist_ok=True)

# Iterate over each file in the folder
for file_path in glob.glob(folder_path + '/*.csv'):
    df = pd.read_csv(file_path)

    # Check if 'spot_price' column exists and is not empty
    if 'spot_price' in df and not df['spot_price'].isnull().all():
        # Remove rows where 'spot_price' is empty and save the file
        df = df.dropna(subset=['spot_price'])
        df.to_csv(file_path, index=False)

        # Determine the destination folder based on the file name
        if file_path.endswith('P.csv'):
            shutil.move(file_path, os.path.join(put_data_folder, os.path.basename(file_path)))
        elif file_path.endswith('C.csv'):
            shutil.move(file_path, os.path.join(call_data_folder, os.path.basename(file_path)))
    else:
        # Delete the file if 'spot_price' column is empty or doesn't exist
        os.remove(file_path)

print("Processing complete. Files sorted into 'put_data' and 'call_data' folders.")
