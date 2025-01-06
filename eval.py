import re
import os
import json


results_folder = f"./task_basic/normal/results"
# results_folder = f"task_basic/normal/results/test"


def extract_string_from_dict(string: str, key: str) -> str:
    pattern = (
        r'"?' + re.escape(key) + r'"?\s*[:=]\s*'  # Match the key with optional quotes, followed by ':' or '='
        r'(?:'  # Non-capturing group to handle the value
        r'"([^"]*)"'  # Match everything inside double quotes
        r'|'  # OR
        r'([^}\]]*)'  # Match unquoted values up to a closing brace or bracket
        r')'
    )
    match = re.search(pattern, string)
    if not match:
        return None
    
    ret = match.group(1) or match.group(2)
    if not ret:
        return None
    return ret.strip()


def string_match(source: str, target: str) -> bool:
    source = source.lower()
    target = target.lower()
    source = re.sub(r'\s+', ' ', source)
    target = re.sub(r'\s+', ' ', target)
    source = re.sub(r'[^a-zA-Z0-9]', '', source)
    target = re.sub(r'[^a-zA-Z0-9]', '', target)
    if target is None or target == '':
        return False
    if target == source: # or target in source or source in target:
        return True
    else:
        return False

def calculate_accuracy(results_folder):
    for root, _, files in os.walk(results_folder):
        for file in files:
            if file.endswith(".json"):
                input_path = os.path.join(root, file)
                output_path = os.path.join(root, os.path.splitext(file)[0] + ".txt")

                with open(input_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                total_questions = 0
                correct_answers = 0

                for question in data:
                    total_questions += 1
                    ans = str(question.get("llm-answer"))
                    ans = extract_string_from_dict(ans, 'answer')
                    ans = str(ans)
                    print(ans)
                    ref_ans = str(question.get("ref_ans"))
                    print(ref_ans)
                    if string_match(ans, ref_ans):
                        correct_answers += 1

                accuracy = correct_answers / total_questions if total_questions > 0 else 0

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(f"Total Questions: {total_questions}\n")
                    f.write(f"Correct Answers: {correct_answers}\n")
                    f.write(f"Accuracy: {accuracy:.2%}\n")

                print(f"Accuracy for {input_path} calculated and saved to {output_path}.")


if __name__ == '__main__':
    calculate_accuracy(results_folder)