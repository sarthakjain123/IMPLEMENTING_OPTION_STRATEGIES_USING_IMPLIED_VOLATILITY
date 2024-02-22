import os
import pandas as pd

# Specify the folder where your CSV files are located
folder_path = 'sorted_on_symbol'

# Specify the three columns for hierarchical sorting
sorting_columns = ['date', 'hour', 'type']

# Get a list of all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Iterate through each CSV file and sort it hierarchically
for file in csv_files:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(folder_path, file))
    
    # Sort the DataFrame hierarchically by the specified columns
    df_sorted = df.sort_values(by=sorting_columns)
    
    # Define the path for the sorted CSV file (you can customize the output path)
    output_path = os.path.join(folder_path, f'sorted_{file}')
    
    # Save the sorted DataFrame to a new CSV file
    df_sorted.to_csv(output_path, index=False)

print("CSV files have been sorted hierarchically!")
