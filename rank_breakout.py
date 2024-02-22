import os
import pandas as pd
import numpy as np

def calculate_iv_rank(df):
    iv_min = df['mark_iv'].min()
    iv_max = df['mark_iv'].max()
    current_iv = df['mark_iv'].iloc[-1]
    
    iv_rank = (current_iv - iv_min) / (iv_max - iv_min)
    return iv_rank

def dynamic_thresholds(df):
    iv_ranks = []
    
    # Start from index 1 to avoid empty dataframe
    for i in range(1, len(df)):
        temp_df = df.iloc[:i+1]
        iv_rank = calculate_iv_rank(temp_df)
        iv_ranks.append(iv_rank)
        
    mean_iv_rank = np.mean(iv_ranks)
    std_iv_rank = np.std(iv_ranks)
    
    low_threshold = mean_iv_rank - std_iv_rank
    high_threshold = mean_iv_rank + std_iv_rank
    
    return low_threshold, high_threshold

def iv_breakout_strategy(file_path):
    df = pd.read_csv(file_path)
    
    # Make sure you have enough data points
    if len(df) <= 1:
        return "NOT ENOUGH DATA"
    
    df = df[df['type'] == 'C']
    
    iv_rank = calculate_iv_rank(df)
    
    low_threshold, high_threshold = dynamic_thresholds(df)
    
    if iv_rank <= low_threshold:
        return "BUY"
    elif iv_rank >= high_threshold:
        return "SELL"
    else:
        return "HOLD"

if __name__ == "__main__":
    folder_path = 'sorted_on_strike'  
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            action = iv_breakout_strategy(file_path)
            print(f"For file {file_name}, the action is: {action}")
