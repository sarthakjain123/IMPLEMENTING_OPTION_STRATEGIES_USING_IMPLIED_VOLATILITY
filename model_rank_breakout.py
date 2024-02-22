import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer

def calculate_iv_rank(df):
    iv_min = df['mark_iv'].min()
    iv_max = df['mark_iv'].max()
    current_iv = df['mark_iv'].iloc[-1]
    if np.isnan(iv_min) or np.isnan(iv_max) or np.isnan(current_iv) or iv_max == iv_min:
        return np.nan
    iv_rank = (current_iv - iv_min) / (iv_max - iv_min)
    return iv_rank

def generate_features_and_labels(df):
    features = []
    labels = []
    low_threshold, high_threshold = df['iv_rank'].mean() - df['iv_rank'].std(), df['iv_rank'].mean() + df['iv_rank'].std()
    for i, row in df.iterrows():
        iv_rank = row['iv_rank']
        delta = row['delta']
        gamma = row['gamma']
        vega = row['vega']
        theta = row['theta']
        option_type = 'CALL' if row['type'] == 'C' else 'PUT'
        
        if iv_rank <= low_threshold:
            label = f"BUY_{option_type}"
        elif iv_rank >= high_threshold:
            label = f"SELL_{option_type}"
        else:
            label = f"HOLD_{option_type}"
        
        is_call = 1 if option_type == 'CALL' else 0
        features.append([iv_rank, delta, gamma, vega, theta, is_call])
        labels.append(label)

    # Remove rows where any element is NaN
    cleaned_features = [f for f in features if not np.isnan(f).any()]
    
    if not cleaned_features:  # Check if the list is empty
        return np.array([]), np.array([])

    # Impute missing values
    imputer = SimpleImputer(strategy='mean')
    cleaned_features = imputer.fit_transform(cleaned_features)
    
    return np.array(cleaned_features), np.array(labels)

if __name__ == "__main__":
    all_features = []
    all_labels = []
    folder_path = 'sorted_on_strike'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df['iv_rank'] = df.apply(lambda row: calculate_iv_rank(df), axis=1)
            
            features, labels = generate_features_and_labels(df)
            
            if features.size == 0:  # Skip empty features
                continue
            
            all_features.extend(features)
            all_labels.extend(labels)
    
    all_features = np.vstack(all_features)
    all_labels = np.array(all_labels)
    
    X_train, X_test, y_train, y_test = train_test_split(all_features, all_labels, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
