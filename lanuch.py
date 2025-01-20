from dataloader import *
from call_llms import *
from tqdm import tqdm
import os
import itertools
import time
def main():

    EvalList = [{'Task':'Code', 'SubTask': 'CodeMissing', 'type': 'c++', 'ExampleType':'OneShot'},
                {'Task':'Code', 'SubTask': 'SpaceComplexity', 'type': 'python', 'ExampleType':'FewShot'},
                {'Task':'Code', 'SubTask': 'TimeComplexity', 'type': 'java', 'ExampleType':'ZeroShot'}]
    # EvalList = [{'Task':'Code', 'SubTask': 'CodeMissing', 'type': 'c++'},
    #             {'Task': 'JSON', 'SubTask': 'type_1', 'Domain': 'university'},
    #             {'Task': 'Formula', 'SubTask': 'convert', 'Mode': 'Simple', 'format1':'Infix', 'format2':'Postfix'},
    #             {'Task': 'Formula', 'SubTask': 'convert', 'Mode': 'Simple', 'format1':'Infix', 'format2':'Prefix'},
    #             {'Task': 'Paper', 'SubTask': 'contextual_qa', 'Mode': 'dev'}]
    
    model_list = ["Qwen/Qwen2.5-0.5B-Instruct", "meta-llama/Meta-Llama-3.1-8B-Instruct"]
    for model in model_list:
        print(model)
        llm = LLMModel(model, api_key=None)
        for Eval in EvalList:
            print(Eval)
            Hibenchdataloader = HibenchDataLoder(Eval)
            data = Hibenchdataloader.load_data()
            for i in tqdm(range(len(data))):
                SystemPrompt = data[i]['SystemPrompt']
                UserPrompt = data[i]['UserPrompt']
                TrueAnswer = data[i]['TrueAnswer']
                # prompt = data[i]['prompt']
                ans = llm.get_response(SystemPrompt, UserPrompt)
                data[i]['response'] = ans
            Hibenchdataloader.save_data(data, model_name=model, args=Eval)
            


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
        if i >= 10:
            break
        os.system('clear')
        for line in text.split('\n'):
            print(f"{color}{line.center(columns)}\033[0m")
        time.sleep(0.5)

if __name__ == '__main__':
    Logo()
    main()