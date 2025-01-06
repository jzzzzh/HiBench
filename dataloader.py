import json
import os
import yaml
import csv

class TemplateDataLoader:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config/config.yaml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def load_data(self):
        pass

class PromptGenerator:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config/prompt.yaml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)


    def generate(self):
        pass    


class FundamentalPromptGenerator(PromptGenerator):
    def __init__(self, SubTask):
        super().__init__()
        self.dataset_name = 'Fundamental'
        self.sub_task = SubTask
    def generate(self, data):
        SystemTemplate = self.config['Fundamental']['SystemTemplate']
        OutputFormatTemplate = self.config['Fundamental']['OutputFormatTemplate']
        # TODO: Implement subtasks
        if self.sub_task == 'add_node':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Fundamental']['Task']['add_node']['OutputFormatTemplate'])
            PromptTemplate = self.config['Fundamental']['Task']['add_node']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<TREE>', data['tree'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'common_ancestor':
            pass
        elif self.sub_task == 'isomorphic':
            pass
        elif self.sub_task == 'remove_node':
            pass
        elif self.sub_task == 'node_depth':
            pass
        elif self.sub_task == 'leaf':
            pass
        elif self.sub_task == 'root':
            pass
        SystemPrompt = SystemTemplate
        UserPrompt = PromptTemplate + OutputFormatTemplate
        return SystemPrompt, UserPrompt, TrueAnswer


class FundumantalDataLoader(TemplateDataLoader):
    def __init__(self, SubTask, TreeType, InputMode):
        super().__init__()
        self.dataset_name = 'Fundamental'
        self.dataset_dir = self.config['Dataset']['Fundamental']['Dir']
        self.data_generator = FundamentalPromptGenerator(SubTask)
        self.sub_task = SubTask
        self.tree_type = TreeType
        self.input_mode = InputMode

    def load_data(self):
        # TODO: Implement input_mode
        # with open(os.path.join(self.dataset_dir, f"{self.tree_type}_{self.Input_mode}.json"), 'r') as file:
        #     train_data = json.load(file)
        # for data in train_data:
        #     SystemPrompt, UserPrompt, TrueAnswer = self.data_generator.generate(data)
        #     print(SystemPrompt)
        #     print(UserPrompt)
        #     print(TrueAnswer)
        return 

class JSONPromptGenerator(PromptGenerator):
    def __init__(self, SubTask):
        super().__init__()
        self.dataset_name = 'JSON'
        self.sub_task = SubTask
    def generate(self, data):
        SystemTemplate = self.config['JSON']['SystemTemplate']
        OutputFormatTemplate = self.config['JSON']['OutputFormatTemplate']
        if self.sub_task == 'type_1':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['Task1']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['Task1']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', json.dumps(data['json']))
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'type_2':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['Task1']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['Task2']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', json.dumps(data['json']))
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'type_3':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['Task1']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['Task3']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', json.dumps(data['json']))
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'type_4':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['Task1']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['Task4']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', json.dumps(data['json']))
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'type_5':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['JSON']['Task']['Task1']['OutputFormatTemplate'])
            PromptTemplate = self.config['JSON']['Task']['Task5']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<JSON>', json.dumps(data['json']))
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        SystemPrompt = SystemTemplate
        UserPrompt = PromptTemplate + OutputFormatTemplate
        return SystemPrompt, UserPrompt, TrueAnswer


class JSONDataLoader(TemplateDataLoader):
    def __init__(self, args):
        super().__init__()
        self.dataset_name = 'JSON'
        SubTask = args['SubTask']
        Domain = args['Domain']
        self.dataset_dir = self.config['Dataset']['JSON']['Dir']
        self.data_generator = JSONPromptGenerator(SubTask)
        self.sub_task = SubTask
        self.domain = Domain
        self.data = []
    def load_data(self):
        ans_json_file = os.path.join(self.dataset_dir, f"{self.domain}/{self.sub_task}.json")
        json_file = os.path.join(self.dataset_dir, f"{self.domain}_structure.json")
        with open(json_file, 'r') as file:
            reference_data = json.load(file)
        with open(ans_json_file, 'r') as file:
            train_data = json.load(file)
        for data in train_data:
            input_data = {}
            input_data['json'] = reference_data
            input_data['question'] = data['question']
            input_data['true_answer'] = data['answer']
            SystemPrompt, UserPrompt, TrueAnswer = self.data_generator.generate(input_data)
            self.data.append({'SystemPrompt': SystemPrompt, 'UserPrompt': UserPrompt, 'TrueAnswer': TrueAnswer})
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
        Mode = args['Mode']
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

        self.Mode = Mode
        self.data = []
    
    def load_data(self):

        if self.sub_task == 'calculate':
            ans_json_file = os.path.join(self.dataset_dir, f"{self.sub_task}/{self.format}_{self.Mode}.csv")
            with open(ans_json_file, 'r') as file:
                reader = csv.DictReader(file)
                train_data = [row for row in reader]
            print(train_data[0])
            for data in train_data:
                input_data = {}
                input_data['formula'] = data['Formula']
                input_data['true_answer'] = data['Result']
                SystemPrompt, UserPrompt, TrueAnswer = self.data_generator.generate(input_data)
                self.data.append({'SystemPrompt': SystemPrompt, 'UserPrompt': UserPrompt, 'TrueAnswer': TrueAnswer})
        elif self.sub_task == 'convert':
            ans_json_file = os.path.join(self.dataset_dir, f"{self.sub_task}/{self.format1}_{self.format2}_{self.Mode}.csv")
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
                self.data.append({'SystemPrompt': SystemPrompt, 'UserPrompt': UserPrompt, 'TrueAnswer': TrueAnswer})
        elif self.sub_task == 'equivalent':
            if self.format1 != self.format2:
                ans_json_file = os.path.join(self.dataset_dir, f"{self.sub_task}/{self.Mode}_Equivalent_{self.format1}_{self.format2}.csv")
            if  self.format1 == self.format2:
                ans_json_file = os.path.join(self.dataset_dir, f"{self.sub_task}/{self.Mode}_Equivalent_{self.format1}.csv")
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
        self.data = []
    
    def load_data(self):
        if self.sub_task == 'SpaceComplexity' or self.sub_task == 'TimeComplexity':
            ans_json_file = os.path.join(self.dataset_dir, f"{self.Domain}Selected/answer.json")
            with open(ans_json_file, 'r') as file:
                train_data = json.load(file)
            for data in train_data:
                code_num = data['questio_no']
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
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'disordered_section':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Paper']['Task']['disordered_section']['OutputFormatTemplate'])
            PromptTemplate = self.config['Paper']['Task']['disordered_section']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        elif self.sub_task == 'outline_extraction':
            OutputFormatTemplate = OutputFormatTemplate.replace('<OUTPUTFORMATE>', self.config['Paper']['Task']['outline_extraction']['OutputFormatTemplate'])
            PromptTemplate = self.config['Paper']['Task']['outline_extraction']['PromptTemplate']
            PromptTemplate = PromptTemplate.replace('<QUESTION>', data['question'])
            TrueAnswer = data['true_answer']
        SystemPrompt = SystemTemplate
        UserPrompt = PromptTemplate + OutputFormatTemplate
        return SystemPrompt, UserPrompt, TrueAnswer


class PaperDataLoder(TemplateDataLoader):
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
                self.data.append({'SystemPrompt': SystemPrompt, 'UserPrompt': UserPrompt, 'TrueAnswer': TrueAnswer})
        return self.data
    
    def get_data(self):
        return self.data
    def length(self):
        return len(self.data)


class HibenchDataLoder(TemplateDataLoader):
    def __init__(self, args):
        super().__init__()
        Task = args['Task']
        if Task == "Code":
            self.data_loader = CodeDataLoader(args)
        elif Task == "JSON":
            self.data_loader = JSONDataLoader(args)
        elif Task == "Formula":
            self.data_loader = FormulaDataLoader(args) 
        elif Task == "Paper":
            self.data_loader = PaperDataLoder(args)
    def load_data(self):
        return self.data_loader.load_data()

if __name__ == '__main__':
    print("This is dataloader.py")