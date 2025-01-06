# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:52:52 2024

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
        logging.FileHandler("equivalence_evaluation.log"),
        logging.StreamHandler()
    ]
)

# Define model list
model_list = [
    # "qwen2.5-0.5b-instruct",
    # "qwen2.5-1.5b-instruct",
    # "qwen2.5-3b-instruct",
    # "qwen2.5-7b-instruct",
    "qwen2.5-32b-instruct",
    # "qwen2.5-72b-instruct",
    # "llama3.1-8b-instruct",
    # "llama3.2-1b-instruct",
    # "llama3.2-3b-instruct",
    # "llama3.1-70b-instruct",
    # "llama3.1-405b-instruct",
]

def sanitize_model_name(model_name):
    """
    Converts special characters in the model name to a format suitable for file names.
    
    Parameters:
        model_name (str): The original model name.
    
    Returns:
        str: The sanitized model name.
    """
    return model_name.replace("/", "_").replace("-", "_")

# Configure OpenAI client (LLAMA model API)
client = openai.OpenAI(
    # It's recommended not to store the API Key in the code directly. Make sure it's loaded via environment variables.
    api_key="",  # Replace with actual API key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def call_llama_api(infix_expr, prefix_expr, model):
    """
    Calls the specified LLAMA model API to determine if two expressions are equivalent.
    
    Parameters:
        infix_expr (str): The infix expression.
        prefix_expr (str): The prefix expression.
        model (str): The model name to use.
    
    Returns:
        str or None: "Yes" or "No", indicating whether the expressions are equivalent, or None if failed.
    """
    prompt = (
        "You are a helpful assistant proficient in evaluating mathematical expressions.\n"
        "Determine whether the following two expressions are mathematically equivalent.\n\n"
        "Infix Expression 1 : {}\n"
        "Prefix Expression 2: {}\n\n"
        "Are these two expressions equivalent? Respond with 'Yes' or 'No' only."
    ).format(infix_expr, prefix_expr)

    try:
        completion = client.chat.completions.create(
            model=model,  # Dynamically using different models
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.5,  # Set to 0 for deterministic output
            max_tokens=250  # Short length to get only "Yes" or "No"
        )

        # Extract the generated response
        response = completion.choices[0].message.content.strip().lower()
        
        return response

    except Exception as e:
        logging.error(f"API call failed, model: {model}, expressions: Infix={infix_expr}, Prefix={prefix_expr}, error: {e}")
        return None

def main():
    # Read the dataset
    input_csv_path = r'infix_prefix.csv'

    try:
        df = pd.read_csv(input_csv_path)
        logging.info(f"Successfully loaded dataset with {len(df)} records.")
    except Exception as e:
        logging.error(f"Failed to read dataset, error: {e}")
        return

    # Define expression types
    expr_types = ['Infix', 'Prefix']

    # Iterate through each model
    for model in model_list:
        logging.info(f"Starting processing for model: {model}")
        sanitized_model = sanitize_model_name(model)
        output_csv_path = rf'{sanitized_model}_task2_equivalence_results.csv'

        # Create a dictionary to store computation results
        results = {
            'Equivalence_Result': []
        }

        # Iterate through each record
        for index, row in df.iterrows():
            logging.info(f"Model: {model} - Processing record {index + 1}/{len(df)}.")
            infix_expr = str(row['Infix']).strip()
            prefix_expr = str(row['Prefix']).strip()

            # Check if the expressions are empty
            if pd.isna(infix_expr) or infix_expr == '' or pd.isna(prefix_expr) or prefix_expr == '':
                logging.warning(f"Model: {model} - Expression is empty for record {index + 1}.")
                results['Equivalence_Result'].append(None)
                continue

            # Call API for calculation
            equivalence = call_llama_api(infix_expr, prefix_expr, model)

            # Append the result to the dictionary
            results['Equivalence_Result'].append(equivalence)

        # Merge results with the original DataFrame
        df_model = df.copy()
        df_model['Equivalence_Result'] = results['Equivalence_Result']

        # Save the results to a CSV file
        try:
            df_model.to_csv(output_csv_path, index=False)
            logging.info(f"Results for model: {model} have been saved to '{output_csv_path}'.")
        except Exception as e:
            logging.error(f"Failed to save results to CSV for model: {model}, error: {e}")

if __name__ == "__main__":
    main()
