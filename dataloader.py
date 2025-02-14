import glob
import json
import os
import yaml
import csv
from datetime import datetime
import random
class TemplateDataLoader:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config/config.yaml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        prompt_config_path = os.path.join(os.path.dirname(__file__), 'config/prompt.yaml')
        with open(prompt_config_path, 'r') as file:
            self.prompt_config = yaml.safe_load(file)
        self.fewshot_example_prompt = self.prompt_config['FewshotExamplePrompt']
        self.oneshot_example_prompt = self.prompt_config['OneshotExamplePrompt']
    def load_data(self):
        pass

class PromptGenerator:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config/prompt.yaml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)


    def generate(self):
        pass    


class FundamentalNormalPromptGenerator(PromptGenerator):
    def __init__(self, SubTask, InputMode):
        super().__init__()
        self.dataset_name = 'Fundamental'
        self.sub_task = SubTask
        self.input_mode = InputMode
    
    def generate(self, data):
        SystemTemplate = self.config['Fundamental']['SystemTemplate']
        OutputFormatTemplate = self.config['Fundamental']['OutputFormatTemplate']
        if self.sub_task == 'leaf':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Normal']['leaf']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Normal']['leaf']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['leaf_Q'])
            TrueAnswer = data[f'leaf_A']
        elif self.sub_task == 'root':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Normal']['root']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Normal']['root']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['root_Q'])
            TrueAnswer = data[f'root_A']
        elif self.sub_task == 'all_ancestor':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Normal']['all_ancestor']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Normal']['all_ancestor']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['all_ancestor_Q'])
            TrueAnswer = data[f'all_ancestor_A']
        elif self.sub_task == 'all_children':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Normal']['all_children']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Normal']['all_children']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['all_children_Q'])
            TrueAnswer = data[f'all_children_A']
        elif self.sub_task == 'isomorphic':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Normal']['isomorphic']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Normal']['isomorphic']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data[f'isomorphic_Q_{self.input_mode[0].upper()}'])
            TrueAnswer = data[f'isomorphic_A']
        elif self.sub_task == 'node_depth':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Normal']['node_depth']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Normal']['node_depth']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['node_depth_Q'])
            TrueAnswer = data[f'node_depth_A']
        elif self.sub_task == 'add_node':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Normal']['add_node']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Normal']['add_node']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['add_node_Q'])
            TrueAnswer = data[f'add_node_A_{self.input_mode[0].upper()}']
        elif self.sub_task == 'remove_node':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Normal']['remove_node']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Normal']['remove_node']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['remove_node_Q'])
            TrueAnswer = data[f'remove_node_A_{self.input_mode[0].upper()}']
        elif self.sub_task == 'common_ancestor':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Normal']['common_ancestor']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Normal']['common_ancestor']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['common_ancestor_Q'])
            TrueAnswer = data[f'common_ancestor_A']
        else:
            raise ValueError(f'unknown subtask {self.sub_task}')
        SystemPrompt = SystemTemplate
        UserPrompt = PromptTemplate + '\n' + OutputFormatTemplate
        return SystemPrompt, UserPrompt, TrueAnswer
    

class FundamentalBinaryPromptGenerator(PromptGenerator):
    def __init__(self, SubTask, InputMode):
        super().__init__()
        self.dataset_name = 'Fundamental'
        self.sub_task = SubTask
        self.input_mode = InputMode
    
    def generate(self, data):
        SystemTemplate = self.config['Fundamental']['SystemTemplate']
        OutputFormatTemplate = self.config['Fundamental']['OutputFormatTemplate']
        if self.sub_task == 'balance':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Binary']['balance']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Binary']['balance']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['balance_Q'])
            TrueAnswer = data[f'balance_A']
        elif self.sub_task == 'prefix_traversal':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Binary']['prefix_traversal']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Binary']['prefix_traversal']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['prefix_traversal_Q'])
            TrueAnswer = data[f'prefix_traversal_A']
        elif self.sub_task == 'infix_traversal':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Binary']['infix_traversal']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Binary']['infix_traversal']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['infix_traversal_Q'])
            TrueAnswer = data[f'infix_traversal_A']
        elif self.sub_task == 'postfix_traversal':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Binary']['postfix_traversal']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Binary']['postfix_traversal']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['postfix_traversal_Q'])
            TrueAnswer = data[f'postfix_traversal_A']
        elif self.sub_task == 'traversal_order_verification':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Binary']['traversal_order_verification']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Binary']['traversal_order_verification']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['traversal_order_verification_Q'])
            TrueAnswer = data[f'traversal_order_verification_A']
        elif self.sub_task == 'mirror_tree':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['Binary']['mirror_tree']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['Binary']['mirror_tree']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<STRUCTURE>', data[f'{self.input_mode.lower()}_presentation'])
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['mirror_tree_Q'])
            TrueAnswer = data[f'mirror_tree_A_{self.input_mode[0].upper()}']
        else:
            raise ValueError(f'unknown subtask {self.sub_task}')
        SystemPrompt = SystemTemplate
        UserPrompt = PromptTemplate + '\n' + OutputFormatTemplate
        return SystemPrompt, UserPrompt, TrueAnswer


class FundamentalDataLoader(TemplateDataLoader):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.dataset_name = 'Fundamental'
        self.tree_type = args['TreeType'] # 'normal' or 'binary'
        self.dataset_dir = os.path.join(self.config['Dataset']['Fundamental']['Dir'], self.tree_type.lower())
        self.sub_task = args["SubTask"]
        self.balance = args['Balance']
        self.weight = args['Weight']
        self.difficulty = args['Difficulty']
        if self.tree_type.capitalize() == 'Normal':
            self.data_generator = FundamentalNormalPromptGenerator(args["SubTask"], args["InputMode"])
        else:
            self.data_generator = FundamentalBinaryPromptGenerator(args["SubTask"], args["InputMode"])
        if 'ExampleType' in args:
            self.example_type = args['ExampleType']
        else:
            self.example_type = "None"
        self.data = list()
        
    def load_data(self):
        dataset_path  = os.path.join(self.dataset_dir, f"{self.balance}-{self.weight}-{self.difficulty}*.json")
        dataset_paths = glob.glob(dataset_path)
        if not dataset_paths:
            print(f'warning: no dataset found for {dataset_path}')
            return self.data
        for path in dataset_paths:
            with open(path, 'r') as f:
                dataset = json.load(f)
            for data in dataset:
                SystemPrompt, UserPrompt, TrueAnswer = self.data_generator.generate(data)
                if self.example_type == "OneShot":
                    one_shot_question = self.prompt_config['Fundamental']['Task'][self.tree_type.capitalize()][f'{self.sub_task}']['Example']['Question1']
                    one_shot_anwsers = self.prompt_config['Fundamental']['Task'][self.tree_type.capitalize()][f'{self.sub_task}']['Example']['Answer1']
                    ExamplePrompt = self.oneshot_example_prompt.replace('<QUESTION1>', one_shot_question).replace('<ANSWER1>', one_shot_anwsers)
                    UserPrompt = ExamplePrompt + '\n' + UserPrompt
                elif self.example_type == "FewShot":
                    few_shot_question1 = self.prompt_config['Fundamental']['Task'][self.tree_type.capitalize()][f'{self.sub_task}']['Example']['Question1']
                    few_shot_anwsers1 = self.prompt_config['Fundamental']['Task'][self.tree_type.capitalize()][f'{self.sub_task}']['Example']['Answer1']
                    few_shot_question2 = self.prompt_config['Fundamental']['Task'][self.tree_type.capitalize()][f'{self.sub_task}']['Example']['Question2']
                    few_shot_anwsers2 = self.prompt_config['Fundamental']['Task'][self.tree_type.capitalize()][f'{self.sub_task}']['Example']['Answer2']
                    few_shot_question3 = self.prompt_config['Fundamental']['Task'][self.tree_type.capitalize()][f'{self.sub_task}']['Example']['Question3']
                    few_shot_anwsers3 = self.prompt_config['Fundamental']['Task'][self.tree_type.capitalize()][f'{self.sub_task}']['Example']['Answer3']
                    ExamplePrompt = self.fewshot_example_prompt.replace('<QUESTION1>', few_shot_question1).replace('<ANSWER1>', few_shot_anwsers1)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION2>', few_shot_question2).replace('<ANSWER2>', few_shot_anwsers2)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION3>', few_shot_question3).replace('<ANSWER3>', few_shot_anwsers3)
                    UserPrompt = ExamplePrompt + '\n' + UserPrompt
                elif self.example_type == "ZeroShot" or self.example_type == "None":
                    pass
                self.data.append({'SystemPrompt': SystemPrompt, 'UserPrompt': UserPrompt, 'TrueAnswer': TrueAnswer})
        return self.data
    def get_data(self):
        return self.data
    def length(self):
        return len(self.data)

class JSONPromptGenerator(PromptGenerator):
    def __init__(self, SubTask):
        super().__init__()
        self.dataset_name = 'JSON'
        self.sub_task = SubTask
        
    def generate(self, structure, data):
        SystemTemplate = self.config['JSON']['SystemTemplate']
        OutputFormatTemplate = self.config['JSON']['OutputFormatTemplate']

        # Map subtasks to their config task numbers and templates
        if self.sub_task == 'child_count':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['child_count']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['child_count']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', structure)
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'node_depth':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['node_depth']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['node_depth']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', structure)
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'level_count':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['level_count']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['level_count']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', structure)
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'node_attribute':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['node_attribute']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['node_attribute']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', structure)
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'level_nodes':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['level_nodes']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['level_nodes']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', structure)
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'path_down_to_up':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['path_down_to_up']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['path_down_to_up']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', structure)
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'path_up_to_down':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['path_up_to_down']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['path_up_to_down']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', structure)
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'shared_ancestor_same_level':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['shared_ancestor_same_level']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['shared_ancestor_same_level']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', structure)
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'shared_ancestor_diff_level':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['shared_ancestor_diff_level']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['shared_ancestor_diff_level']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', structure)
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'path_between_nodes':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['path_between_nodes']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['path_between_nodes']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', structure)
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        else:
            raise ValueError(f'unknown subtask {self.sub_task}')
        
        SystemPrompt = SystemTemplate
        UserPrompt = PromptTemplate + '\n' + OutputFormatTemplate
        return SystemPrompt, UserPrompt, TrueAnswer


class JSONDataLoader(TemplateDataLoader):
    def __init__(self, args):
        super().__init__()
        self.dataset_name = 'JSON'
        self.sub_task = args['SubTask']
        self.domain = args['Domain']
        # Update the dataset directory to point to dataset/JSON in project root
        self.dataset_dir = os.path.join(
            os.path.dirname(__file__),
            "dataset",
            "JSON"
        )
        self.data_generator = JSONPromptGenerator(self.sub_task)
        
        # Map descriptive names to task numbers for prompt config

        if 'ExampleType' in args:
            self.example_type = args['ExampleType']
        else:
            self.example_type = "None"
        self.data = []

    def load_data(self):
        # Load from dataset/JSON/QA directory
        dataset_path = os.path.join(
            self.dataset_dir,
            "dataset",
            f"{self.domain}.json"
        )
        question_path = os.path.join(
            self.dataset_dir,
            "QA",
            self.sub_task,
            f"{self.sub_task}_{self.domain}.json"
        )
        
        with open(dataset_path, 'r') as file:
            structure_data = str(json.load(file))
        
        with open(question_path, 'r') as file:
            train_data = json.load(file)

        for data in train_data:
            input_data = {}
            input_data['question'] = data['question']
            input_data['true_answer'] = data['answer']
            
            SystemPrompt, UserPrompt, TrueAnswer = self.data_generator.generate(structure_data, input_data)

            if self.example_type == "OneShot":
                one_shot_question = self.prompt_config['JSON']['Task'][self.sub_task]['Example']['Question1']
                one_shot_answers = self.prompt_config['JSON']['Task'][self.sub_task]['Example']['Answer1']
                ExamplePrompt = self.oneshot_example_prompt.replace('<QUESTION1>', one_shot_question).replace('<ANSWER1>', one_shot_answers)
                UserPrompt = ExamplePrompt + UserPrompt

            elif self.example_type == "FewShot":
                few_shot_question1 = self.prompt_config['JSON']['Task'][self.sub_task]['Example']['Question1']
                few_shot_answers1 = self.prompt_config['JSON']['Task'][self.sub_task]['Example']['Answer1']
                few_shot_question2 = self.prompt_config['JSON']['Task'][self.sub_task]['Example']['Question2']
                few_shot_answers2 = self.prompt_config['JSON']['Task'][self.sub_task]['Example']['Answer2']
                few_shot_question3 = self.prompt_config['JSON']['Task'][self.sub_task]['Example']['Question3']
                few_shot_answers3 = self.prompt_config['JSON']['Task'][self.sub_task]['Example']['Answer3']
                
                ExamplePrompt = self.fewshot_example_prompt.replace('<QUESTION1>', few_shot_question1).replace('<ANSWER1>', few_shot_answers1)
                ExamplePrompt = ExamplePrompt.replace('<QUESTION2>', few_shot_question2).replace('<ANSWER2>', few_shot_answers2)
                ExamplePrompt = ExamplePrompt.replace('<QUESTION3>', few_shot_question3).replace('<ANSWER3>', few_shot_answers3)
                UserPrompt = ExamplePrompt + UserPrompt

            self.data.append({
                'SystemPrompt': SystemPrompt,
                'UserPrompt': UserPrompt,
                'TrueAnswer': TrueAnswer
            })

        return self.data

    def get_data(self):
        return self.data
    def length(self):
        return len(self.data)
    

class FormulaPromptGenerator(PromptGenerator):
    def __init__(self, SubTask):
        super().__init__()
        self.dataset_name = 'Formula'
        self.sub_task = SubTask
    def generate(self, data):
        SystemTemplate = self.config['Formula']['SystemTemplate']
        OutputFormatTemplate = self.config['Formula']['OutputFormatTemplate']
        if self.sub_task == 'calculate':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Formula']['Task']['Calculation']['OutputFormatTemplate'])
            PromptTemplate = self.config['Formula']['Task']['Calculation']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<FORMULA>', data['formula'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'convert':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Formula']['Task']['Convert']['OutputFormatTemplate'])
            PromptTemplate = self.config['Formula']['Task']['Convert']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<FORMAT1>', data['format1'])
            PromptTemplate = PromptTemplate.replace('<FORMAT2>', data['format2'])
            PromptTemplate = PromptTemplate.replace('<FORMULA>', data['formula'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'equivalent':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Formula']['Task']['Equation']['OutputFormatTemplate'])
            PromptTemplate = self.config['Formula']['Task']['Equation']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<FORMULA1>', data['formula1'])
            PromptTemplate = PromptTemplate.replace('<FORMULA2>', data['formula2'])
            TrueAnswer = data['true_answer']
        SystemPrompt = SystemTemplate
        UserPrompt = PromptTemplate + OutputFormatTemplate
        return SystemPrompt, UserPrompt, TrueAnswer

class FormulaDataLoader(TemplateDataLoader):
    def __init__(self, args):
        super().__init__()
        SubTask = args['SubTask']
        Symbol_Mode = args['Symbol_Mode']
        Value_Mode = args['Value_Mode']
        Length_Mode = args['Length_Mode']
        self.dataset_name = 'Formula'
        self.dataset_dir = self.config['Dataset']['Formula']['Dir']
        self.data_generator = FormulaPromptGenerator(SubTask)
        self.sub_task = SubTask
        if SubTask == 'convert':
            self.format1 = args['format1']
            self.format2 = args['format2']
        elif SubTask == 'equivalent':
            self.format1 = args['format1']
            self.format2 = args['format2']
        elif SubTask == 'calculate':
            self.format = args['format']
        self.dict = {"calculate":"Calculation", "convert":"Convert", "equivalent":"Equation"}
        if 'ExampleType' in args:
            self.example_type = args['ExampleType']
        else:
            self.example_type = "None"
        
        self.Mode = f"_symbol_{Symbol_Mode}_value_{Value_Mode}_length_{Length_Mode}"
        self.data = []
    
    def load_data(self):
        if self.sub_task == 'calculate':
            ans_json_file = os.path.join(self.dataset_dir, f"{self.sub_task}/{self.format}{self.Mode}.csv")
            with open(ans_json_file, 'r') as file:
                reader = csv.DictReader(file)
                train_data = [row for row in reader]
            # print(train_data[0])
            for data in train_data:
                input_data = {}
                input_data['formula'] = data['Formula']
                input_data['true_answer'] = data['Result']
                SystemPrompt, UserPrompt, TrueAnswer = self.data_generator.generate(input_data)
                if self.example_type == "OneShot":
                    one_shot_question = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    one_shot_anwsers = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    ExamplePrompt = self.oneshot_example_prompt.replace('<QUESTION1>', one_shot_question).replace('<ANSWER1>', one_shot_anwsers)
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "FewShot":
                    few_shot_question1 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    few_shot_anwsers1 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    few_shot_question2 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question2']
                    few_shot_anwsers2 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer2']  
                    few_shot_question3 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question3']
                    few_shot_anwsers3 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer3']
                    ExamplePrompt = self.fewshot_example_prompt.replace('<QUESTION1>', few_shot_question1).replace('<ANSWER1>', few_shot_anwsers1)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION2>', few_shot_question2).replace('<ANSWER2>', few_shot_anwsers2)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION3>', few_shot_question3).replace('<ANSWER3>', few_shot_anwsers3)
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "ZeroShot" or self.example_type == "None":
                    pass
                self.data.append({'SystemPrompt': SystemPrompt, 'UserPrompt': UserPrompt, 'TrueAnswer': TrueAnswer})
        elif self.sub_task == 'convert':
            ans_json_file = os.path.join(self.dataset_dir, f"{self.sub_task}/{self.format1}2{self.format2}{self.Mode}.csv")
            with open(ans_json_file, 'r') as file:
                reader = csv.DictReader(file)
                train_data = [row for row in reader]
            for data in train_data:
                input_data = {}
                input_data['formula'] = data['Formula']
                input_data['true_answer'] = data['Result']
                input_data['format1'] = self.format1
                input_data['format2'] = self.format2
                SystemPrompt, UserPrompt, TrueAnswer = self.data_generator.generate(input_data)
                if self.example_type == "OneShot":
                    one_shot_question = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    one_shot_anwsers = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    ExamplePrompt = self.oneshot_example_prompt.replace('<QUESTION1>', one_shot_question).replace('<ANSWER1>', one_shot_anwsers)
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "FewShot":
                    few_shot_question1 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    few_shot_anwsers1 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    few_shot_question2 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question2']
                    few_shot_anwsers2 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer2']  
                    few_shot_question3 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question3']
                    few_shot_anwsers3 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer3']
                    ExamplePrompt = self.fewshot_example_prompt.replace('<QUESTION1>', few_shot_question1).replace('<ANSWER1>', few_shot_anwsers1)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION2>', few_shot_question2).replace('<ANSWER2>', few_shot_anwsers2)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION3>', few_shot_question3).replace('<ANSWER3>', few_shot_anwsers3)
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "ZeroShot" or self.example_type == "None":
                    pass
                self.data.append({'SystemPrompt': SystemPrompt, 'UserPrompt': UserPrompt, 'TrueAnswer': TrueAnswer})
        elif self.sub_task == 'equivalent':
            if self.format1 != self.format2:
                ans_json_file = os.path.join(self.dataset_dir, f"{self.sub_task}/{self.format1}Eq2{self.format2}{self.Mode}.csv")
            if  self.format1 == self.format2:
                ans_json_file = os.path.join(self.dataset_dir, f"{self.sub_task}/{self.format1}Eq2{self.format1}{self.Mode}.csv")
            with open(ans_json_file, 'r') as file:
                reader = csv.DictReader(file)
                train_data = [row for row in reader]
            for data in train_data:
                input_data = {}
                input_data['formula1'] = data['Original']
                input_data['formula2'] = data['Perturbed']
                input_data['format1'] = self.format1
                input_data['format2'] = self.format2
                input_data['true_answer'] = data['Is_Equivalent']
                SystemPrompt, UserPrompt, TrueAnswer = self.data_generator.generate(input_data)
                if self.example_type == "OneShot":
                    one_shot_question = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    one_shot_anwsers = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    ExamplePrompt = self.oneshot_example_prompt.replace('<QUESTION1>', one_shot_question).replace('<ANSWER1>', one_shot_anwsers)
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "FewShot":
                    few_shot_question1 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    few_shot_anwsers1 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    few_shot_question2 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question2']
                    few_shot_anwsers2 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer2']  
                    few_shot_question3 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question3']
                    few_shot_anwsers3 = self.prompt_config['Formula']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer3']
                    ExamplePrompt = self.fewshot_example_prompt.replace('<QUESTION1>', few_shot_question1).replace('<ANSWER1>', few_shot_anwsers1)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION2>', few_shot_question2).replace('<ANSWER2>', few_shot_anwsers2)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION3>', few_shot_question3).replace('<ANSWER3>', few_shot_anwsers3)
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "ZeroShot" or self.example_type == "None":
                    pass
                self.data.append({'SystemPrompt': SystemPrompt, 'UserPrompt': UserPrompt, 'TrueAnswer': TrueAnswer})
        return self.data
    
    def get_data(self):
        return self.data
    def length(self):
        return len(self.data)


class CodePromptGenerator(PromptGenerator):
    def __init__(self, SubTask):
        super().__init__()
        self.dataset_name = 'Code'
        self.sub_task = SubTask
    def generate(self, data):
        SystemTemplate = self.config['Code']['SystemTemplate']
        OutputFormatTemplate = self.config['Code']['OutputFormatTemplate']
        if self.sub_task == 'SpaceComplexity':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Code']['Task']['SpaceComplexity']['OutputFormatTemplate'])
            PromptTemplate = self.config['Code']['Task']['SpaceComplexity']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<CODE>', data['code'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'TimeComplexity':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Code']['Task']['TimeComplexity']['OutputFormatTemplate'])
            PromptTemplate = self.config['Code']['Task']['TimeComplexity']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<CODE>', data['code'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'CodeMissing':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Code']['Task']['CodeMissing']['OutputFormatTemplate'])
            PromptTemplate = self.config['Code']['Task']['CodeMissing']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<CODE>', data['code'])
            TrueAnswer = data['true_answer']
        SystemPrompt = SystemTemplate
        UserPrompt = PromptTemplate + OutputFormatTemplate
        return SystemPrompt, UserPrompt, TrueAnswer


class CodeDataLoader(TemplateDataLoader):
    def __init__(self, args):
        super().__init__()
        self.dataset_name = 'Code'
        SubTask = args['SubTask']
        Domain = args['type']
        self.dataset_dir = self.config['Dataset']['Code']['Dir']
        self.data_generator = CodePromptGenerator(SubTask)
        self.sub_task = SubTask
        self.Domain = Domain
        self.dict = {"SpaceComplexity":"SpaceComplexity", "TimeComplexity":"TimeComplexity", "CodeMissing":"CodeMissing"}
        self.data = []
        if 'ExampleType' in args:
            self.example_type = args['ExampleType']
        else:
            self.example_type = "None"

    def load_data(self):
        if self.sub_task == 'SpaceComplexity' or self.sub_task == 'TimeComplexity':
            ans_json_file = os.path.join(self.dataset_dir, f"{self.Domain}Selected/answer.json")
            with open(ans_json_file, 'r') as file:
                train_data = json.load(file)
            for data in train_data:
                code_num = data['question_no']
                if self.Domain == 'c++':
                    code_dir = os.path.join(self.dataset_dir, f"{self.Domain}Selected/{code_num}.cpp")
                elif self.Domain == 'python':
                    code_dir = os.path.join(self.dataset_dir, f"{self.Domain}Selected/{code_num}.py")
                with open(code_dir, 'r') as file:
                    code = file.read()
                input_data = {}
                input_data['code'] = code
                if self.sub_task == 'SpaceComplexity':
                    input_data['true_answer'] = data['space']
                elif self.sub_task == 'TimeComplexity':
                    input_data['true_answer'] = data['time']
                SystemPrompt, UserPrompt, TrueAnswer = self.data_generator.generate(input_data)
                if self.example_type == "OneShot":
                    one_shot_question = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    one_shot_anwsers = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    ExamplePrompt = self.oneshot_example_prompt.replace('<QUESTION1>', one_shot_question).replace('<ANSWER1>', one_shot_anwsers)         
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "FewShot":
                    few_shot_question1 = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    few_shot_anwsers1 = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    few_shot_question2 = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question2']
                    few_shot_anwsers2 = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer2']
                    few_shot_question3 = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question3']
                    few_shot_anwsers3 = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer3']
                    ExamplePrompt = self.fewshot_example_prompt.replace('<QUESTION1>', few_shot_question1).replace('<ANSWER1>', few_shot_anwsers1)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION2>', few_shot_question2).replace('<ANSWER2>', few_shot_anwsers2)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION3>', few_shot_question3).replace('<ANSWER3>', few_shot_anwsers3)
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "ZeroShot" or self.example_type == "None":
                    pass
                self.data.append({'SystemPrompt': SystemPrompt, 'UserPrompt': UserPrompt, 'TrueAnswer': TrueAnswer})
        elif self.sub_task == 'CodeMissing':
            code_dir = os.path.join(self.dataset_dir, f"{self.Domain}Missing/code")
            missing_code_dir = os.path.join(self.dataset_dir, f"{self.Domain}Missing/log")
            code_num = len(os.listdir(code_dir))
            for idx in range(code_num):
                if self.Domain == 'c++':
                    with open(os.path.join(code_dir, f"modified_{idx+1}.cpp"), 'r') as file:
                        code = file.read()
                elif self.Domain == 'python':
                    with open(os.path.join(code_dir, f"modified_{idx+1}.py"), 'r') as file:
                        code = file.read()
                with open(os.path.join(missing_code_dir, f"{idx+1}_log.txt"), 'r') as file:
                    ans = file.read()
                input_data = {}
                input_data['code'] = code
                input_data['true_answer'] = ans
                SystemPrompt, UserPrompt, TrueAnswer = self.data_generator.generate(input_data)
                if self.example_type == "OneShot":
                    one_shot_question = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    one_shot_anwsers = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    ExamplePrompt = self.oneshot_example_prompt.replace('<QUESTION1>', one_shot_question).replace('<ANSWER1>', one_shot_anwsers)         
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "FewShot":
                    few_shot_question1 = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    few_shot_anwsers1 = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    few_shot_question2 = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question2']
                    few_shot_anwsers2 = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer2']
                    few_shot_question3 = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question3']
                    few_shot_anwsers3 = self.prompt_config['Code']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer3']
                    ExamplePrompt = self.fewshot_example_prompt.replace('<QUESTION1>', few_shot_question1).replace('<ANSWER1>', few_shot_anwsers1)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION2>', few_shot_question2).replace('<ANSWER2>', few_shot_anwsers2)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION3>', few_shot_question3).replace('<ANSWER3>', few_shot_anwsers3)
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "ZeroShot" or self.example_type == "None":
                    pass
                self.data.append({'SystemPrompt': SystemPrompt, 'UserPrompt': UserPrompt, 'TrueAnswer': TrueAnswer})
        return self.data
    
    def get_data(self):
        return self.data
    def length(self):
        return len(self.data)


class PaperPromptGenerator(PromptGenerator):
    def __init__(self, SubTask):
        super().__init__()
        self.dataset_name = 'Paper'
        self.sub_task = SubTask
    def generate(self, data):
        SystemTemplate = self.config['Paper']['SystemTemplate']
        OutputFormatTemplate = self.config['Paper']['OutputFormatTemplate']
        if self.sub_task == 'contextual_qa':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Paper']['Task']['contextual_qa']['OutputFormatTemplate'])
            PromptTemplate = self.config['Paper']['Task']['contextual_qa']['PromptTemplate']
            # PromptTemplate = PromptTemplate.replace('<JSON>', structure)
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'disordered_section':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Paper']['Task']['disordered_section']['OutputFormatTemplate'])
            PromptTemplate = self.config['Paper']['Task']['disordered_section']['PromptTemplate']
            # PromptTemplate = PromptTemplate.replace('<JSON>', structure)
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'outline_extraction':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Paper']['Task']['outline_extraction']['OutputFormatTemplate'])
            PromptTemplate = self.config['Paper']['Task']['outline_extraction']['PromptTemplate']
            # PromptTemplate = PromptTemplate.replace('<JSON>', structure)
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        SystemPrompt = SystemTemplate
        UserPrompt = PromptTemplate + OutputFormatTemplate
        return SystemPrompt, UserPrompt, TrueAnswer


class PaperDataLoader(TemplateDataLoader):
    def __init__(self, args):
        super().__init__()
        self.dataset_name = 'Paper'
        SubTask = args['SubTask']
        Mode = args['Mode']
        self.dataset_dir = self.config['Dataset']['Paper']['Dir']
        self.data_generator = PaperPromptGenerator(SubTask)
        self.sub_task = SubTask
        self.Mode = Mode
        self.data = []
        if 'ExampleType' in args:
            self.example_type = args['ExampleType']
        else:
            self.example_type = "None"
        self.dict = {"contextual_qa":"contextual_qa", "disordered_section":"disordered_section", "outline_extraction":"outline_extraction"}
    def load_data(self):
        if self.sub_task == 'contextual_qa':
            ans_json_file = os.path.join(self.dataset_dir, f"contextual_qa/{self.Mode}.json")
            with open(ans_json_file, 'r') as file:
                train_data = json.load(file)
            for data in train_data:
                input_data = {}
                input_data['question'] = data['question']
                input_data['true_answer'] = "{answer:"+ str(data['answer']['references']) +"}"
                SystemPrompt, UserPrompt, TrueAnswer = self.data_generator.generate(input_data)
                if self.example_type == "OneShot":
                    one_shot_question = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    one_shot_anwsers = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    ExamplePrompt = self.oneshot_example_prompt.replace('<QUESTION1>', one_shot_question).replace('<ANSWER1>', one_shot_anwsers)           
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "FewShot":
                    few_shot_question1 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    few_shot_anwsers1 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    few_shot_question2 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question2']
                    few_shot_anwsers2 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer2']
                    few_shot_question3 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question3']
                    few_shot_anwsers3 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer3']
                    ExamplePrompt = self.fewshot_example_prompt.replace('<QUESTION1>', few_shot_question1).replace('<ANSWER1>', few_shot_anwsers1)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION2>', few_shot_question2).replace('<ANSWER2>', few_shot_anwsers2)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION3>', few_shot_question3).replace('<ANSWER3>', few_shot_anwsers3)
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "ZeroShot" or self.example_type == "None":
                    pass
                self.data.append({'SystemPrompt': SystemPrompt, 'UserPrompt': UserPrompt, 'TrueAnswer': TrueAnswer})
        elif self.sub_task == 'disordered_section':
            ans_json_file = os.path.join(self.dataset_dir, f"disordered_section/{self.Mode}.json")
            with open(ans_json_file, 'r') as file:
                train_data = json.load(file)
            for data in train_data:
                input_data = {}
                input_data['question'] = data['question']
                input_data['true_answer'] = "{answer:"+str(data['answer']['references'])+"}"
                SystemPrompt, UserPrompt, TrueAnswer = self.data_generator.generate(input_data)
                if self.example_type == "OneShot":
                    one_shot_question = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    one_shot_anwsers = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    ExamplePrompt = self.oneshot_example_prompt.replace('<QUESTION1>', one_shot_question).replace('<ANSWER1>', one_shot_anwsers)           
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "FewShot":
                    few_shot_question1 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    few_shot_anwsers1 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    few_shot_question2 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question2']
                    few_shot_anwsers2 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer2']
                    few_shot_question3 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question3']
                    few_shot_anwsers3 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer3']
                    ExamplePrompt = self.fewshot_example_prompt.replace('<QUESTION1>', few_shot_question1).replace('<ANSWER1>', few_shot_anwsers1)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION2>', few_shot_question2).replace('<ANSWER2>', few_shot_anwsers2)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION3>', few_shot_question3).replace('<ANSWER3>', few_shot_anwsers3)
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "ZeroShot" or self.example_type == "None":
                    pass
                self.data.append({'SystemPrompt': SystemPrompt, 'UserPrompt': UserPrompt, 'TrueAnswer': TrueAnswer})
        elif self.sub_task == 'outline_extraction':
            ans_json_file = os.path.join(self.dataset_dir, f"outline_extraction/{self.Mode}.json")
            with open(ans_json_file, 'r') as file:
                train_data = json.load(file)
            for data in train_data:
                input_data = {}
                input_data['question'] = data['question']
                input_data['true_answer'] = "{answer:"+ str(data['answer']['references']) + "}"
                SystemPrompt, UserPrompt, TrueAnswer = self.data_generator.generate(input_data)
                if self.example_type == "OneShot":
                    one_shot_question = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    one_shot_anwsers = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    ExamplePrompt = self.oneshot_example_prompt.replace('<QUESTION1>', one_shot_question).replace('<ANSWER1>', one_shot_anwsers)           
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "FewShot":
                    few_shot_question1 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question1']
                    few_shot_anwsers1 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer1']
                    few_shot_question2 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question2']
                    few_shot_anwsers2 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer2']
                    few_shot_question3 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Question3']
                    few_shot_anwsers3 = self.prompt_config['Paper']['Task'][f'{self.dict[self.sub_task]}']['Example']['Answer3']
                    ExamplePrompt = self.fewshot_example_prompt.replace('<QUESTION1>', few_shot_question1).replace('<ANSWER1>', few_shot_anwsers1)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION2>', few_shot_question2).replace('<ANSWER2>', few_shot_anwsers2)
                    ExamplePrompt = ExamplePrompt.replace('<QUESTION3>', few_shot_question3).replace('<ANSWER3>', few_shot_anwsers3)
                    UserPrompt = ExamplePrompt + UserPrompt
                elif self.example_type == "ZeroShot" or self.example_type == "None":
                    pass
                self.data.append({'SystemPrompt': SystemPrompt, 'UserPrompt': UserPrompt, 'TrueAnswer': TrueAnswer})
        return self.data       
        
    
    def get_data(self):
        return self.data
    def length(self):
        return len(self.data)


class HibenchDataLoader(TemplateDataLoader):
    def __init__(self, args):
        super().__init__()
        self.data_loader = self._get_data_loader(args)
        self.save_dir = self.config["Eval"]["SaveDir"]

    def _get_data_loader(self, args):
        loaders = {
            "Fundamental": FundamentalDataLoader,
            "Code": CodeDataLoader,
            "JSON": JSONDataLoader,
            "Formula": FormulaDataLoader,
            "Paper": PaperDataLoader,
        }
        return loaders.get(args['Task'], None)(args) if args['Task'] in loaders else None

    def load_data(self, num_samples=None):
        data = self.data_loader.load_data() if self.data_loader else None
        if num_samples is not None and isinstance(num_samples, int):
            num_samples = min(num_samples, len(data))
            # random.shuffle(data)
            return data[:num_samples]
        return data

    def _get_file_path(self, model_name, args):
        task, subtask = args['Task'], args['SubTask']
        base_path = os.path.join(self.save_dir, task, subtask, model_name)
        json_name = '_'.join(f"{k}_{v}" for k, v in args.items())
        return base_path, f"{json_name}_*.json"

    def is_data_exist(self, model_name, args):
        base_path, file_pattern = self._get_file_path(model_name, args)
        return bool(glob.glob(os.path.join(base_path, file_pattern)))

    def save_data(self, data, model_name, args):
        base_path, file_name = self._get_file_path(model_name, args)
        os.makedirs(base_path, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(base_path, file_name.replace('_*', f'_{timestamp}'))
        with open(save_path, 'w') as file:
            json.dump(data, file, indent=4)

def test_json_dataloader():
    """Test all JSON question types with different domains and example types"""
    # Test all JSON question types
    question_types = [
        'child_count',
        'node_depth',
        'level_count',
        'level_nodes',
        'path_down_to_up',
        'path_up_to_down',
        'shared_ancestor_same_level',
        'shared_ancestor_diff_level',
        'path_between_nodes'
    ]
    
    # Test different dataset sizes
    domains = [
        'university_structure_large_1',
        'university_structure_medium_1',
        'university_bullshit_structure_large_1',
        'university_bullshit_structure_medium_1',
        'university_structure_large_2',
        'university_structure_medium_2',
        'university_bullshit_structure_large_2',
        'university_bullshit_structure_medium_2',
        'university_structure_small',
        'university_bullshit_structure_small'
    ]
    
    # Test different example types
    example_types = ['OneShot', 'FewShot', 'ZeroShot']
    
    print("\nTesting JSON Question Types:")
    print("=" * 50)
    
    for question_type in question_types:
        print(f"\nTesting question type: {question_type}")
        print("-" * 30)
        
        for domain in domains:
            print(f"\nDomain: {domain}")
            
            for example_type in example_types:
                args = {
                    'Task': 'JSON',
                    'SubTask': question_type,
                    'Domain': domain,
                    'ExampleType': example_type
                }
                
                try:
                    data_loader = HibenchDataLoader(args)
                    data = data_loader.load_data()
                    if data and len(data) > 0:
                        print(f"✓ {example_type}: Successfully loaded {len(data)} items")
                        if example_type == 'OneShot':  # Show sample for OneShot only to keep output clean
                            print("Sample question:")
                            print(json.dumps(data[0], indent=2))
                    else:
                        print(f"✗ {example_type}: No data loaded")
                except Exception as e:
                    print(f"✗ {example_type}: Error - {str(e)}")
            print("-" * 30)

def test_dataloader():
    # args = {'Task':'Code', 'SubTask': 'SpaceComplexity', 'type': 'c++', 'ExampleType':'OneShot'}
    #args = {'Task': 'JSON', 'SubTask': 'type_1', 'Domain': 'university', 'ExampleType':'OneShot'}
    # args = {'Task': 'Fundamental', 'SubTask': 'root', 'Difficulty': 'easy', 'TreeType': 'Normal', 'Balance': 'unbalanced', 'Weight': 'unweighted', 'InputMode': 'edge', 'ExampleType': 'ZeroShot'}
    # args = {'Task': 'Formula', 'SubTask': 'convert', 'Symbol_Mode': 'easy', 'Value_Mode':'easy', 'Length_Mode':'easy', 'format1':'infix', 'format2':'postfix', 'ExampleType':'FewShot'}
    #args = {'Task': 'Formula', 'SubTask': 'equivalent', 'Symbol_Mode': 'easy', 'Value_Mode':'easy', 'Length_Mode':'easy', 'format1':'infix', 'format2':'postfix', 'ExampleType':'FewShot'}
    # args = {'Task': 'Formula', 'SubTask': 'calculate', 'Symbol_Mode': 'easy', 'Value_Mode':'easy', 'Length_Mode':'easy', 'format':'infix', 'ExampleType':'FewShot'}
    args = {'Task': 'Paper', 'SubTask': 'contextual_qa', 'Mode': 'dev', 'ExampleType':'OneShot'}
    # args = {'Task': 'Fundamental', 'TreeType': 'binary', 'SubTask': 'infix_traversal', 'InputMode': 'hierarchy', 'balance': 'unbalanced', 'weight':'unweighted', 'difficulty':'easy', 'ExampleType':'FewShot'}
    data_loader = HibenchDataLoader(args)
    data = data_loader.load_data()
    print(data[0])
    # test_json_dataset()

if __name__ == '__main__':
    print("This is dataloader.py")
    test_json_dataloader()
