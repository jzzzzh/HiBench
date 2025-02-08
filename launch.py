import itertools
import time
import os

from dataloader import *
from call_llms import *
from tqdm import tqdm
import logging

class ArgumentGenerator:
    def __init__(self):
        pass
    def generate_fundamental_eval(self, ExampleType='ALL', NormalSubTask='ALL', BinarySubTask='ALL'):
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
        if ExampleType != 'ALL':
            fundamental_parameter['ExampleType'] = [ExampleType]
        
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
        return EvalList

    def generate_code_eval(self, ExampleType='ALL', SubTask='ALL', Type='ALL'):
        code_parameter = {
            'Task': 'Code',
            'SubTask': ['SpaceComplexity', 'TimeComplexity'],
            'Type': ['c++', 'python'],
            'ExampleType': ['ZeroShot', 'FewShot', 'OneShot']
        }
        if ExampleType != 'ALL':
            code_parameter['ExampleType'] = [ExampleType]
        if SubTask != 'ALL':
            code_parameter['SubTask'] = [SubTask]
        if Type != 'ALL':
            code_parameter['Type'] = [Type]
        EvalList = list()
        for subtask in code_parameter['SubTask']:
            for code_type in code_parameter['Type']:
                for example_type in code_parameter['ExampleType']:
                    EvalList.append({'Task': 'Code', 'SubTask':subtask, 'type': code_type, 'ExampleType': example_type})
        return EvalList

    def generate_json_eval(self, ExampleType='ALL', SubTask='ALL', Domain='ALL'):
        json_parameter = {
            'Task': 'JSON',
            'SubTask': ['type_1', 'type_2', 'type_3', 'type_4', 'type_5'],
            'Domain': ['university', 'company'],
            'ExampleType': ['ZeroShot', 'FewShot', 'OneShot']
        }
        if ExampleType != 'ALL':
            json_parameter['ExampleType'] = [ExampleType]
        if SubTask != 'ALL':
            json_parameter['SubTask'] = [SubTask]
        if Domain != 'ALL':
            json_parameter['Domain'] = [Domain]
        EvalList = list()
        for subtask in json_parameter['SubTask']:
            for domain in json_parameter['Domain']:
                for example_type in json_parameter['ExampleType']:
                    EvalList.append({'Task': 'JSON', 'SubTask':subtask, 'Domain': domain, 'ExampleType': example_type})
        return EvalList

    def generate_formula_eval(self, ExampleType='ALL', SubTask='ALL', Symbol_Mode='ALL', Value_Mode='ALL', Length_Mode='ALL'):
        formula_parameter = {
            'Task': 'Formula',
            'SubTask': ['convert', 'calculate', 'equivalent'],
            'Symbol_Mode': ['easy', 'medium', 'hard'],
            'Value_Mode': ['easy', 'medium', 'hard'],
            'Length_Mode': ['easy', 'medium', 'hard'],
            'Format1': ['infix', 'postfix', 'prefix'],
            'Format2': ['infix', 'postfix', 'prefix'],
            'ExampleType': ['ZeroShot', 'FewShot', 'OneShot']
        }
        if ExampleType != 'ALL':
            formula_parameter['ExampleType'] = [ExampleType]
        if SubTask != 'ALL':
            formula_parameter['SubTask'] = [SubTask]
        if Symbol_Mode != 'ALL':
            formula_parameter['Symbol_Mode'] = [Symbol_Mode]
        if Value_Mode != 'ALL':
            formula_parameter['Value_Mode'] = [Value_Mode]
        if Length_Mode != 'ALL':
            formula_parameter['Length_Mode'] = [Length_Mode]
        # args = {'Task': 'Formula', 'SubTask': 'convert', 'Symbol_Mode': 'easy', 'Value_Mode':'easy', 'Length_Mode':'easy', 'format1':'infix', 'format2':'postfix', 'ExampleType':'FewShot'}
        EvalList = list()
        for subtask in formula_parameter['SubTask']:
            for symbol_mode in formula_parameter['Symbol_Mode']:
                for value_mode in formula_parameter['Value_Mode']:
                    for length_mode in formula_parameter['Length_Mode']:
                        for format1 in formula_parameter['Format1']:
                            for format2 in formula_parameter['Format2']:
                                for example_type in formula_parameter['ExampleType']:
                                    if subtask == 'convert':
                                        if format1 == format2:
                                            continue
                                        EvalList.append({'Task': 'Formula', 'SubTask':subtask, 'Symbol_Mode': symbol_mode, 'Value_Mode': value_mode, 'Length_Mode': length_mode, 'format1': format1, 'format2': format2, 'ExampleType': example_type})
                                    elif subtask == 'equivalent':
                                        EvalList.append({'Task': 'Formula', 'SubTask':subtask, 'Symbol_Mode': symbol_mode, 'Value_Mode': value_mode, 'Length_Mode': length_mode, 'format1': format1, 'format2': format2, 'ExampleType': example_type})

                            for example_type in formula_parameter['ExampleType']:
                                if subtask == 'calculate':
                                    EvalList.append({'Task': 'Formula', 'SubTask':subtask, 'Symbol_Mode': symbol_mode, 'Value_Mode': value_mode, 'Length_Mode': length_mode, 'format': format1, 'ExampleType': example_type})
        return EvalList

    def generate_paper_eval(self, ExampleType='ALL', SubTask='ALL', Mode='ALL'):
        paper_parameter = {
            'Task': 'Paper',
            'SubTask': ['contextual_qa', 'disordered_section', 'outline_extraction'],
            'Mode': ['dev', 'test'],
            'ExampleType': ['ZeroShot', 'FewShot', 'OneShot']
        }
        if ExampleType != 'ALL':
            paper_parameter['ExampleType'] = [ExampleType]
        if SubTask != 'ALL':
            paper_parameter['SubTask'] = [SubTask]
        if Mode != 'ALL':
            paper_parameter['Mode'] = [Mode]
        EvalList = list()
        for subtask in paper_parameter['SubTask']:
            for mode in paper_parameter['Mode']:
                for example_type in paper_parameter['ExampleType']:
                    EvalList.append({'Task': 'Paper', 'SubTask':subtask, 'Mode': mode, 'ExampleType': example_type})
        return EvalList
    def generate_all_eval(self, Task_list = ['Fundamental', 'Code', 'JSON', 'Formula', 'Paper'], ExampleType='ALL'):
        EvalList = list()
        if 'Fundamental' in Task_list:
            EvalList += self.generate_fundamental_eval(ExampleType=ExampleType)
        if 'Code' in Task_list:
            EvalList += self.generate_code_eval(ExampleType=ExampleType)
        if 'JSON' in Task_list:
            EvalList += self.generate_json_eval(ExampleType=ExampleType)
        if 'Formula' in Task_list:
            EvalList += self.generate_formula_eval(ExampleType=ExampleType)
        if 'Paper' in Task_list:
            EvalList += self.generate_paper_eval(ExampleType=ExampleType)
        return EvalList
    def test_dataloader(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        
        EvalList = self.generate_fundamental_eval()
        logger.info("check fundamental dataloader")
        for Eval in tqdm(EvalList):
            Hibenchdataloader = HibenchDataLoder(Eval)
            Hibenchdataloader.load_data()
        logger.info("fundamental pass")
        
        EvalList = self.generate_formula_eval()
        logger.info("check formula dataloader")
        for Eval in tqdm(EvalList):
            Hibenchdataloader = HibenchDataLoder(Eval)
            Hibenchdataloader.load_data()
        logger.info("formula pass")

        EvalList = self.generate_json_eval()
        logger.info("check json dataloader")
        for Eval in tqdm(EvalList):
            Hibenchdataloader = HibenchDataLoder(Eval)
            Hibenchdataloader.load_data()
        logger.info("json pass")

        EvalList = self.generate_code_eval()
        logger.info("check code dataloader")
        for Eval in tqdm(EvalList):
            Hibenchdataloader = HibenchDataLoder(Eval)
            Hibenchdataloader.load_data()
        logger.info("code pass")

        EvalList = self.generate_paper_eval()
        logger.info("check paper dataloader")
        for Eval in tqdm(EvalList):
            Hibenchdataloader = HibenchDataLoder(Eval)
            Hibenchdataloader.load_data()
        logger.info("paper pass")

def main():
    argument_generator = ArgumentGenerator()
    EvalList = argument_generator.generate_all_eval(Task_list = ['Fundamental', 'Code', 'JSON', 'Formula'], ExampleType='ZeroShot')
    # model_list = ["meta-llama/Meta-Llama-3.1-8B-Instruct"] # ["Qwen/Qwen2.5-0.5B-Instruct"] #, "meta-llama/Meta-Llama-3.1-8B-Instruct"]
    # model_list = ["meta-llama/Meta-Llama-3.1-8B-Instruct", "meta-llama/Llama-3.2-1B-Instruct","meta-llama/Llama-3.2-3B-Instruct", "Qwen/Qwen2.5-0.5B-Instruct", "Qwen/Qwen2.5-1.5B-Instruct", "Qwen/Qwen2.5-3B-Instruct", "Qwen/Qwen2.5-7B-Instruct"]
    model_list = ["Qwen/Qwen2.5-0.5B-Instruct"]
    
    for model in model_list:
        llm = LLMModel(model, api_key=None)
        length = len(EvalList)
        for idx, Eval in enumerate(EvalList):
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            logger = logging.getLogger(__name__)
            
            logger.info(f"\033[93mProcessing task: {Eval} | Model: {model} | Progress: {idx}/{length}\033[0m")
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