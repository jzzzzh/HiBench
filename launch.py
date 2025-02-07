import itertools
import time
import os

from dataloader import *
from call_llms import *
from tqdm import tqdm


def main():

    # EvalList = [{'Task':'Code', 'SubTask': 'CodeMissing', 'type': 'c++', 'ExampleType':'OneShot'},
    #             {'Task':'Code', 'SubTask': 'SpaceComplexity', 'type': 'python', 'ExampleType':'FewShot'},
    #             {'Task':'Code', 'SubTask': 'TimeComplexity', 'type': 'java', 'ExampleType':'ZeroShot'}]
    # EvalList = [{'Task':'Code', 'SubTask': 'CodeMissing', 'type': 'c++'},
    #             {'Task': 'JSON', 'SubTask': 'type_1', 'Domain': 'university'},
    #             {'Task': 'Formula', 'SubTask': 'convert', 'Mode': 'Simple', 'format1':'Infix', 'format2':'Postfix'},
    #             {'Task': 'Formula', 'SubTask': 'convert', 'Mode': 'Simple', 'format1':'Infix', 'format2':'Prefix'},
    #             {'Task': 'Paper', 'SubTask': 'contextual_qa', 'Mode': 'dev'}]
    fundamental_parameter = {
        'Task': 'Fundamental',
        'SubTask': {
            'Normal': ['add_node', 'all_ancestor', 'all_children', 'common_ancestor', 'isomorphic', 'remove_node', 'node_depth', 'leaf', 'root'],
            'Binary': ['balance', 'prefix_traversal', 'infix_traversal', 'postfix_traversal', 'traversal_order_verification', 'mirror_tree']
        },
        'Difficulty': ['easy', 'medium', 'hard'],
        'TreeType': ['Binary', 'Normal'],
        'Balance': ['balanced', 'unbalanced'],
        'Weight': ['weighted', 'unweighted'],
        'InputMode': ['edge', 'hierarchy'],
        'ExampleType': ['ZeroShot', 'FewShot', 'OneShot']
    }
    
    EvalList = list()
    for tree_type in ['Normal', 'Binary']:
        for subtask in fundamental_parameter['SubTask'][tree_type]:
            for difficulty in fundamental_parameter['Difficulty']:
                for input_mode in fundamental_parameter['InputMode']:
                    for example_type in fundamental_parameter['ExampleType']:
                        if tree_type == 'Binary':
                            for balance in fundamental_parameter['Balance']:
                                EvalList.append({'Task': 'Fundamental', 'SubTask':subtask, 'Difficulty': difficulty, 'TreeType':tree_type, 'Balance':balance, 'Weight':'unweighted', 'InputMode': input_mode, 'ExampleType': example_type})
                        else:
                            EvalList.append({'Task': 'Fundamental', 'SubTask':subtask, 'Difficulty': difficulty, 'TreeType':tree_type, 'Balance':'unbalanced', 'Weight':'unweighted', 'InputMode': input_mode, 'ExampleType': example_type})

    # model_list = ["meta-llama/Meta-Llama-3.1-8B-Instruct"] # ["Qwen/Qwen2.5-0.5B-Instruct"] #, "meta-llama/Meta-Llama-3.1-8B-Instruct"]
    # model_list = ["meta-llama/Meta-Llama-3.1-8B-Instruct", "meta-llama/Llama-3.2-1B-Instruct","meta-llama/Llama-3.2-3B-Instruct", "Qwen/Qwen2.5-0.5B-Instruct", "Qwen/Qwen2.5-1.5B-Instruct", "Qwen/Qwen2.5-3B-Instruct", "Qwen/Qwen2.5-7B-Instruct"]
    model_list = ["Qwen/Qwen2.5-0.5B-Instruct"]
    for model in model_list:
        llm = LLMModel(model, api_key=None)
        for Eval in EvalList:
            print(f"Processing task: {Eval}")
            Hibenchdataloader = HibenchDataLoder(Eval)
            data = Hibenchdataloader.load_data()
            for i in tqdm(range(len(data))):
                SystemPrompt = data[i]['SystemPrompt']
                UserPrompt = data[i]['UserPrompt']
                TrueAnswer = data[i]['TrueAnswer']
                ans = llm.get_response(SystemPrompt, UserPrompt)
                data[i]['response'] = ans
            Hibenchdataloader.save_data(data, model_name=model, args=Eval)
            print(f"Completed task: {Eval}")
            

def Logo():
    colors = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m"]
    text = (
        "   __  ___ ____                  __  \n"
        "  / / / (_) __ )___  ____  _____/ /_ \n"
        "  / /_/ / / __  / _ \/ __ \/ ___/ __ \\ \n"
        " / __  / / /_/ /  __/ / / / /__/ / / / \n"
        "/_/ /_/_/_____/\___/_/ /_/\___/_/ /_/  "
    )
    columns = os.get_terminal_size().columns

    for i, color in enumerate(itertools.cycle(colors)):
        if i >= 50:
            break
        os.system('clear')
        for line in text.split('\n'):
            print(f"{color}{line.center(columns)}\033[0m")
        time.sleep(0.1)

if __name__ == '__main__':
    # Logo()
    main()