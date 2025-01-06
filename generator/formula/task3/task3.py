# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 18:05:40 2024

@author: JC TU
"""

import openai
import pandas as pd
import logging
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("conversion_evaluation.log"),
        logging.StreamHandler()
    ]
)

# Configure OpenAI client (LLAMA model API)
client = openai.OpenAI(
    # If environment variables are not set, you can directly set the API key here.
    api_key="",
    # api_key=os.getenv("OPENAI_API_KEY"),  # It's recommended to read from environment variables
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def call_llama_api(expression, source_type):
    """
    Call the LLAMA model API to compute the value of a given expression.

    Parameters:
        expression (str): The expression.
        source_type (str): The type of the expression (Infix, Prefix, Postfix).

    Returns:
        float or None: The computed value of the expression, or None if it fails.
    """
    prompt = f"Calculate the value of the following {source_type} expression. Only return a number, no additional text: {source_type}: {expression} Value:"

    try:
        completion = client.chat.completions.create(
            model="qwen2.5-32b-instruct",  # Model list: https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.0,  # Set to 0 for deterministic output
            max_tokens=50  # Short enough to only get the number
        )

        # Extract the generated value
        value_str = completion.choices[0].message.content.strip()
        print(f"Expression Type: {source_type}, Expression: {expression}, Value: {value_str}")

        # Attempt to convert the returned content to a float
        try:
            value = float(value_str)
            return value
        except ValueError:
            logging.error(f"Unable to convert returned content to a number. Content: '{value_str}'")
            return None

    except Exception as e:
        logging.error(f"API call failed, expression: {expression}, type: {source_type}, error: {e}")
        return None

def main():
    # Read dataset
    input_csv_path = r'task.csv'
    output_csv_path = r'qwen2.5_32b_instruct_task3_calculated_resultson.csv'

    try:
        df = pd.read_csv(input_csv_path)
        logging.info(f"Successfully loaded dataset with {len(df)} records.")
    except Exception as e:
        logging.error(f"Failed to read dataset, error: {e}")
        return

    # Create a dictionary to store the computation results
    results = {
        'Infix_Result': [],
        'Prefix_Result': [],
        'Postfix_Result': []
    }

    # Define expression types
    expr_types = ['Infix', 'Prefix', 'Postfix']

    # Iterate through each record
    for index, row in df.iterrows():
        logging.info(f"Processing record {index + 1}/{len(df)}.")
        for expr_type in expr_types:
            expression = str(row[expr_type]).strip()
            if pd.isna(expression) or expression == '':
                logging.warning(f"Record {index + 1}: {expr_type} expression is empty.")
                results[f'{expr_type}_Result'].append(None)
                continue

            # Call the API for calculation
            value = call_llama_api(expression, expr_type)

            # Add the result to the corresponding dictionary
            results[f'{expr_type}_Result'].append(value)

    # Merge original data and results
    for key, value in results.items():
        df[key] = value

    # Save the results to a CSV file
    try:
        df.to_csv(output_csv_path, index=False)
        logging.info(f"Computation results have been saved to '{output_csv_path}'.")
    except Exception as e:
        logging.error(f"Failed to save results to CSV, error: {e}")

if __name__ == "__main__":
    main()
