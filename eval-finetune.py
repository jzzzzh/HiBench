import glob
import os
import re
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

    files = glob.glob(os.path.join(result_path, f'{task}_{subtask}_*.json'))
    for file in files:
        eval_path = file.replace('.json', '.txt')
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        total_questions = 0
        correct_answers = 0
        for result in data:
            total_questions += 1
            answer = str(result.get("response"))
            ref    = str(result.get("TrueAnswer"))
            ref    = evaluate._extract_answer(ref) if task != 'Paper' else ref
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
    finetune_result_path = './finetune-results/qwen_0221'
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
                calculate_accuracy(finetune_result_path, task, subtask)
            except AttributeError as e:
                print(f'subtask name error: {task} {subtask}')
                print(e)