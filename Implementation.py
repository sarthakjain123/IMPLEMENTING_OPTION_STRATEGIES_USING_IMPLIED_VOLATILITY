import glob
import pandas as pd
import pandas_ta as pta

folder_path_C = 'call_data'  
folder_path_P = 'put_data'   

# Function to process each file and calculate RSI
def process_file(file_path):
    df = pd.read_csv(file_path)

    # Skip files with very few rows
    if len(df) <= 15:
        print(f"File {file_path} has 15 or fewer rows. Skipping.")
        return []

    # Ensure necessary columns are present and numeric
    if 'mark_iv' not in df.columns or 'strike_price' not in df.columns or 'spot_price' not in df.columns or 'volume_contracts' not in df.columns:
        print(f"Missing required columns in {file_path}. Skipping file.")
        return []

    df['mark_iv'] = pd.to_numeric(df['mark_iv'], errors='coerce')
    df['strike_price'] = pd.to_numeric(df['strike_price'], errors='coerce')
    df['spot_price'] = pd.to_numeric(df['spot_price'], errors='coerce')
    df['volume'] = pd.to_numeric(df['volume_contracts'], errors='coerce')

    df['RSI'] = pta.rsi(df['mark_iv'], length=14)

    flag = False
    entry = 0
    pnl = []
    for index, row in df.iterrows():
        # Skip rows with volume equal to 0
        if row['volume_contracts'] == 0:
            continue

        if pd.notna(row['RSI']):
            if row['RSI'] < 30 and not flag:
                print("In", row['close'])
                entry = row['close']
                dif_bel_30 = row['strike_price'] - row['spot_price']
                print(f"dif_bel_30: {dif_bel_30}")
                flag = True
            elif row['RSI'] > 70 and flag:
                print("Out RSI", row['close'])
                dif_abv_70 = row['strike_price'] - row['spot_price']
                print(f"dif_abv_70: {dif_abv_70}")
                pnl.append(row['close'] - entry)
                flag = False

    return pnl

# Process all files in the 'call_data' folder
for file_path in glob.glob(folder_path_C + '/*.csv'):
    pnl = process_file(file_path)
    print(f"File: {file_path}, PNL: {pnl}, Sum of PNL_C: {sum(pnl)}")

# Process all files in the 'put_data' folder
for file_path in glob.glob(folder_path_P + '/*.csv'):
    pnl = process_file(file_path)
    print(f"File: {file_path}, PNL: {pnl}, Sum of PNL_P: {sum(pnl)}")
