import pandas as pd

# Load the original CSV file
df = pd.read_csv('combined.csv')

# Specify the column name for splitting
column_name = 'symbol'

# Get unique values in the specified column
unique_values = df[column_name].unique()

# Create separate CSV files for each unique value
for value in unique_values:
    # Create a new DataFrame containing only rows with the current value
    sub_df = df[df[column_name] == value]
    
    # Define the name for the output CSV file based on the value
    output_filename = f'{value}.csv'
    
    # Save the sub DataFrame to a new CSV file
    sub_df.to_csv(output_filename, index=False)

print("CSV files have been split successfully!")
