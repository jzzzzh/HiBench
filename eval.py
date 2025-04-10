import glob
import os
import json

import yaml

from evaluator import FundamentalEvaluator, CodeEvaluator, FormulaEvaluator, JsonEvaluator, PaperEvaluator


def calculate_accuracy(result_path, task, subtask):
    if task == 'Fundamental':
        evaluate = FundamentalEvaluator()
    elif task == 'Code':
        evaluate = CodeEvaluator()
    elif task == 'Formula':
        evaluate = FormulaEvaluator()
    elif task == 'JSON':
        evaluate = JsonEvaluator()
    elif task == 'Paper':
        evaluate = PaperEvaluator()
    else:
        raise ValueError(f'unknown task {task}')

    
    result_path = os.path.join(result_path, task, subtask)
    files =  glob.glob(os.path.join(result_path, '*', '*', '*.json'))
    files += glob.glob(os.path.join(result_path, '*', '*.json'))
    for file in files:
        eval_path = file.replace('.json', '.txt')
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        total_questions = 0
        correct_answers = 0
        for result in data:
            total_questions += 1
            answer = result.get("response", None)
            ref    = result.get("TrueAnswer", None)
            if answer:
                answer = str(answer)
                ref    = str(ref)
            else:
                continue
            # >>>> Temp adaptation for represent_mode of fundamental tasks.
            kwargs = dict()
            if subtask in ['add_node', 'remove_node', 'mirror_tree']:
                kwargs = dict(represent_mode='edge') if 'InputMode_edge' in file else dict(represent_mode='hierarchy')
            # <<<< Temp adaptation for represent_mode of fundamental tasks.
            correct_answers += float(evaluate(subtask, source=answer, target=ref, **kwargs))
        accuracy = correct_answers / total_questions if total_questions > 0 else 0
        with open(eval_path, "w", encoding="utf-8") as f:
            f.write(f"Total Questions: {total_questions}\n")
            f.write(f"Correct Answers: {correct_answers}\n")
            f.write(f"Accuracy: {accuracy:.2%}\n")

        print(f"Accuracy for {file} calculated and saved to {eval_path}.")
        
        
if __name__ == '__main__':
    with open('./config/config.yaml', 'r') as file:
        configs = yaml.safe_load(file)
    for task in configs['Dataset']:
        print(f'{task = }')
        subtasks = configs['Dataset'][task]['SubTask']
        if isinstance(subtasks, dict):
            subtasks = sum(subtasks.values(), [])
        for subtask in subtasks:
            print(f'{subtask = }')
            try:
                calculate_accuracy('cot-results', task, subtask)
                # calculate_accuracy(configs['Eval']['SaveDir'], task, subtask)
            except AttributeError as e:
                print(f'subtask name error: {task} {subtask}')
                print(e)