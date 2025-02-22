import os
import re
import pandas as pd

def extract_accuracy(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"Accuracy:\s*([\d.]+)%", content)
    return float(match.group(1)) if match else None

def get_model_info(file_path, result_dir):
    rel_path = os.path.relpath(os.path.dirname(file_path), result_dir)
    path_parts = rel_path.split(os.sep)
    model_info = path_parts[1:]
    return model_info

def collect(result_dir):
    task_data = {}

    for task in os.listdir(result_dir):
        task_path = os.path.join(result_dir, task)
        if not os.path.isdir(task_path):
            continue
        
        task_data[task] = []

        for root, _, files in os.walk(task_path):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    model_info = get_model_info(file_path, result_dir)
                    file_name = os.path.splitext(file)[0]
                    param_pairs = file_name.split("_")[2:][:-2]
                    # FUCK THE INFORMAL FILE NAME SETTINGS, ESPECIALLY JSON and FORMULA.
                    if task == 'Fundamental':
                        params = param_pairs[-12:]
                        params = {params[i]: params[i + 1] for i in range(0, len(params), 2)}
                        params['SubTask'] = '_'.join(param_pairs[1:-12])
                    elif task == 'JSON':
                        params = {f'params_{i}': param_pairs[i] for i in range(0, len(param_pairs))}
                    elif task == 'Paper':
                        try:
                            params = dict()
                            params['SubTask'] = '_'.join(param_pairs[1:3])
                            params['Mode'] = param_pairs[4]
                            params['Example'] = param_pairs[6]
                        except IndexError:
                            params = {f'params_{i}': param_pairs[i] for i in range(0, len(param_pairs))}
                    elif task == 'Formula':
                        params = dict()
                        params['SubTask'] = param_pairs[1]
                        params['Symbol'] = param_pairs[4]
                        params['Value'] = param_pairs[7]
                        params['Length'] = param_pairs[10]
                        params['Format'] = '_'.join(param_pairs[11:-2])
                        params['Example'] = '_'.join(param_pairs[-2:])
                    elif task == 'Code':
                        params = {param_pairs[i]: param_pairs[i + 1] for i in range(0, len(param_pairs), 2)}
                    # FUCK OFF
                    else:
                        raise ValueError(f'unknown task {task}')
                    accuracy = extract_accuracy(file_path)
                    entry = {
                        "Task": task,
                        "Accuracy": accuracy,
                        **params
                    }
                    for i, level in enumerate(model_info):
                        entry[f"Model_Info_{i+1}"] = level
                    task_data[task].append(entry)

    for task, data in task_data.items():
        df = pd.DataFrame(data)
        column_order = sum([
            ["Task"], 
            sorted([col for col in df.columns if col.startswith("Model_Level_")]),
            sorted([col for col in df.columns if col not in ["Task", "Accuracy"] and not col.startswith("Model_Level_")]),
            ["Accuracy"]
        ], [])
        df = df[column_order]
        csv_path = os.path.join(result_dir, f"{task}_collection.csv")
        df.to_csv(csv_path, index=False)
        print(f"save result to: {csv_path}")
        

if __name__ == '__main__':
    result_directory = "./Results"
    collect(result_directory)
