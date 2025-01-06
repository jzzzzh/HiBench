# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 16:43:44 2024

@author: JC TU
"""

import openai
import pandas as pd
import logging
import os
from dotenv import load_dotenv

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

# Configure OpenAI client (NVIDIA's LLaMa model API)
client = openai.OpenAI(
    api_key="",  # Replace this with your actual API key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# Define model list
model_list = [
    # "qwen2.5-0.5b-instruct",
    # "qwen2.5-1.5b-instruct",
    # "qwen2.5-3b-instruct",
    # "qwen2.5-7b-instruct",
    "qwen2.5-14b-instruct",
    "qwen2.5-32b-instruct",
    # "qwen2.5-72b-instruct",
    # "llama3.1-8b-instruct",
    # "llama3.2-1b-instruct",
    # "llama3.2-3b-instruct",
    # "llama3.1-70b-instruct",
    # "llama3.1-405b-instruct",
]

def call_llama_api(expression, source_type, target_type):
    """
    Call the NVIDIA LLaMa model API to convert one type of expression to another.

    Parameters:
        expression (str): The source expression.
        source_type (str): The source expression type (Prefix, Infix, Postfix).
        target_type (str): The target expression type (Prefix, Infix, Postfix).

    Returns:
        str: The converted target expression, or None if the conversion fails.
    """
    prompt = f"Convert the following {source_type} expression to a {target_type} expression, and only return the {target_type} expression without any additional text:\n{source_type}: {expression}\n{target_type}:"
  
    try:
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",  # Replace with the actual model you want to use
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,  # Set to 0 for deterministic output
            top_p=1,
            max_tokens=100,
            stream=False  # Get full response
        )

        # Extract the generated target expression
        target_expression = completion.choices[0].message.content.strip()
        print('target_expression:', target_expression)

        # Remove the target type prefix if it exists
        prefix = f"{target_type.lower()}:"
        if target_expression.lower().startswith(prefix):
            target_expression = target_expression[len(prefix):].strip()

        return target_expression

    except Exception as e:
        logging.error(f"API call failed for source expression: {expression} converting to {target_type}, error: {e}")
        return None

def main():
    # Supported expression types
    expr_types = ['Prefix', 'Infix', 'Postfix']

    # Define all possible conversion pairs
    conversion_pairs = []
    for source in expr_types:
        for target in expr_types:
            if source != target:
                conversion_pairs.append((source, target))

    # Read the dataset
    try:
        df = pd.read_csv('expression_dataset_with_results_task11.csv')
        logging.info(f"Successfully loaded dataset with {len(df)} records.")
    except Exception as e:
        logging.error(f"Failed to read dataset, error: {e}")
        return

    # Create a list to store conversion results
    results = []

    # Iterate through each record
    for index, row in df.iterrows():
        for source_type, target_type in conversion_pairs:
            source_expr = str(row[source_type]).strip()

            logging.info(f"Processing record {index + 1}/{len(df)}, conversion: {source_type} -> {target_type}, source expression: {source_expr}")

            # Call the API for conversion
            converted_expr = call_llama_api(source_expr, source_type, target_type)
            print(f"Converted {target_type} expression:", converted_expr)

            # Add the result to the list
            results.append({
                'Source Type': source_type,
                'Source Expression': source_expr,
                'Target Type': target_type,
                'Converted Expression': converted_expr
            })

    # Save the results to a CSV file
    results_df = pd.DataFrame(results)
    results_df.to_csv('converted_expressions.csv', index=False)
    logging.info("Conversion results have been saved to 'converted_expressions.csv'.")

if __name__ == "__main__":
    main()
