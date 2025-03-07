import os
import re
import pandas as pd

def extract_accuracy(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"Accuracy:\s*([\d.]+)%", content)
    return float(match.group(1)) if match else None

def collect(result_dir):
    task_data = dict()
    for root, _, files in os.walk(result_dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                file_name = os.path.splitext(file)[0]
                task = file_name.split("_")[0]
                accuracy = extract_accuracy(file_path)
                entry = {
                    "Task": task,
                    "Name": file_name,
                    "Accuracy": accuracy
                }
                try:
                    task_data[task].append(entry)
                except KeyError:
                    task_data[task] = list()
                    task_data[task].append(entry)

    for task, data in task_data.items():
        df = pd.DataFrame(data)
        csv_path = os.path.join(result_dir, 'collection', f"{task}_collection.csv")
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df.to_csv(csv_path, index=False)
        print(f"save result to: {csv_path}")
        

if __name__ == '__main__':
    result_directory = "./finetune-results/qwen_0221"
    collect(result_directory)
