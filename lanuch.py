from dataloader import *
from call_llms import *
from tqdm import tqdm
import os
def main():

    EvalList = [{'Task':'Code', 'SubTask': 'CodeMissing', 'type': 'c++'},
                {'Task':'Code', 'SubTask': 'SpaceComplexity', 'type': 'python'}]
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
            

    
if __name__ == '__main__':
    os.execl('/bin/bash', '/bin/bash', '-c', './Hibench.sh')
    main()