import pandas as pd
import os

def combine_csv_files(folder_path, output_file):
    combined_data = pd.DataFrame()

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)

            # Read each CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Check if the columns in df match the columns in combined_data
            if combined_data.empty:
                combined_data = df
            else:
                # Check if the columns match
                if all(df.columns == combined_data.columns):
                    # Concatenate the data to the combined_data DataFrame
                    combined_data = pd.concat([combined_data, df], ignore_index=True)
                else:
                    print(f"Columns in {filename} do not match. Skipping the file.")

    # Write the combined data to a new CSV file
    combined_data.to_csv(output_file, index=False)

    print(f"Combined CSV files saved to {output_file}")

folder_path = "Main Data"  # Replace with your folder path
output_file = "combined.csv"
combine_csv_files(folder_path, output_file)