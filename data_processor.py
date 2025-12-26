import pandas as pd
import json
import os

def load_config(config_path='source/json.config'):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, 'r') as f:
        return json.load(f)

def clean_dataset(df):
    initial_rows = len(df)
    df = df.drop_duplicates()
    
    cols_to_check = ['Applicant_Income', 'Coapplicant_Income', 'Loan_Amount', 'Loan_Term_Months']
    for col in cols_to_check:
        if col in df.columns:
            df = df[df[col] >= 0]

    print(f"Cleaning Report: {initial_rows - len(df)} rows removed.")
    return df

def convert_csv_to_json(input_path, output_path):
    print(f"Reading data from {input_path}...")
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: The file {input_path} was not found.")
        return
    
    cleaned_df = clean_dataset(df)
    
    print(f"Saving JSON to {output_path}...")
    cleaned_df.to_json(output_path, orient='records', indent=4)
    print("Conversion successful.")

if __name__ == "__main__":
    config = load_config()
    convert_csv_to_json(config['input_csv'], config['output_json'])
