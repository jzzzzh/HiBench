import os
import json

def process_json_files(folder_path):
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        if not isinstance(data, list):
                            print(f"Skipping {filename}: Not a list of dictionaries.")
                            continue
                    except json.JSONDecodeError:
                        print(f"Skipping {filename}: Invalid JSON format.")
                        continue
                
                for item in data:
                    if isinstance(item, dict) and 'TrueAnswer' in item:
                        value = item['TrueAnswer']
                        if isinstance(value, str) and ': ' in value:
                            item['TrueAnswer'] = value.split(': ', 1)[1]
                            
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

                print(f"Processed {file_path}")


folder_path = "Results/JSON/node_relationship"
process_json_files(folder_path)