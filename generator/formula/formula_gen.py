import formula_config
import random
import re
from tqdm import tqdm
import csv
import os

def generate_formula(symbol_complexity, value_complexity, length):
    formula = ""
    formula_list = []
    previous_symbol = ""
    left_bracket = 0
    divide = False
    for i in range(length):
        symbol = random.choice(symbol_complexity)
        value = random.choice(value_complexity)
        while previous_symbol == "/" and value == 0:
            value = random.choice(value_complexity)
        while divide == True and left_bracket > 0 and value == 0 and previous_symbol == "*":
            value = random.choice(value_complexity)
        if previous_symbol == "^":
            value = int(random.choice(range(1, 3)))
            while symbol == "(" or symbol == ")" or symbol == "^" or symbol == "/" or symbol == "*":
                symbol = random.choice(symbol_complexity)
        if previous_symbol == "(":
            while symbol == "(":
                symbol = random.choice(symbol_complexity)

        if symbol == "(":
            left_bracket += 1
            formula += symbol
            formula_list.append(symbol)
            formula += str(value)
            formula_list.append(str(value))
            symbol = random.choice(symbol_complexity)
            while symbol == "(" or symbol == ")":
                symbol = random.choice(symbol_complexity)
            if i < length - 1:
                formula += symbol
                formula_list.append(symbol)
                previous_symbol = symbol
        elif symbol == ")":
            if left_bracket > 0:
                left_bracket -= 1
                if left_bracket == 0:
                    divide = False
                formula += str(value)
                formula_list.append(str(value))
                formula += symbol
                formula_list.append(symbol)
                symbol = random.choice(symbol_complexity)
                while symbol == "(" or symbol == ")":
                    symbol = random.choice(symbol_complexity)
                if i < length - 1:
                    formula += symbol
                    formula_list.append(symbol)
                    previous_symbol = symbol
            elif left_bracket == 0:
                while symbol == ")" or symbol == "(":
                    symbol = random.choice(symbol_complexity)
                formula += str(value)
                formula_list.append(str(value))
                if i < length - 1:
                    formula += symbol
                    formula_list.append(symbol)
                    previous_symbol = symbol
        else:
            if symbol == "/":
                divide = True
            if i < length - 1:
                formula += str(value) 
                formula += symbol
                formula_list.append(str(value))
                formula_list.append(symbol)
                previous_symbol = symbol
            else:
                formula += str(value)
                formula_list.append(str(value))

    if left_bracket > 0:
        for i in range(left_bracket):
            formula += ")"
            formula_list.append(")")
    return formula, formula_list

def infix_to_postfix(formula_list):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    
    stack = []  
    output = []  

    for token in formula_list:

        if token.isdigit() or token[1:].isdigit(): 
            output.append(token)

        elif token == '(':
            stack.append(token)

        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop() 

        else:
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence.get(token, 0):
                output.append(stack.pop())
            stack.append(token)


    while stack:
        output.append(stack.pop())

    return output

def infix_to_prefix(formula_list):

    formula_list = formula_list[::-1]

    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    stack = []  
    output = [] 

    for token in formula_list:

        if token.isdigit() or token[1:].isdigit(): 
            output.append(token)

        elif token == ')':
            stack.append(token)

        elif token == '(':
            while stack and stack[-1] != ')':
                output.append(stack.pop())
            stack.pop()  

        else:
            while stack and stack[-1] != ')' and precedence.get(stack[-1], 0) > precedence.get(token, 0):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())


    return output[::-1]

def convert_to_string(formula_list):
    formula = ""
    for i in range(len(formula_list)):
        formula += formula_list[i]
        if i < len(formula_list) - 1:
            formula += " "
    return formula

def random_change(formula_list1, formula_list2, symbol_complexity, value_complexity):
    tmp1 = formula_list1.copy()
    tmp2 = formula_list2.copy()
    if random.choice([True, False]):
        flag = False
        index = random.randint(0, len(formula_list1) - 1)
        while formula_list1[index] == "(" or formula_list1[index] == ")":
            index = random.randint(0, len(formula_list1) - 1)
        if formula_list1[index].isdigit() or formula_list1[index][1:].isdigit():
            original = formula_list1[index]
            new = random.choice(value_complexity)
            while new == original:
                new = random.choice(value_complexity)
            tmp1[index] = str(new)
        else:
            original = formula_list1[index]
            new = random.choice([s for s in symbol_complexity if s not in ["(", ")"]])
            while new == original:
                new = random.choice([s for s in symbol_complexity if s not in ["(", ")"]])
            tmp1[index] = new
        return [convert_to_string(tmp1), convert_to_string(formula_list2), flag]
    else:
        flag = True
        return [convert_to_string(tmp1), convert_to_string(formula_list2), flag]






def gen_dataset(symbol_complexity, value_complexity, length, num_samples):
    dataset = []
    i = 0
    while i < num_samples: 
        formula, formula_list = generate_formula(symbol_complexity, value_complexity, length)
        postfix_list = infix_to_postfix(formula_list)
        prefix_list = infix_to_prefix(formula_list)
        try:
            formula = re.sub(r"\^", "**", formula)
            postfixEq2Prefix = random_change(postfix_list, prefix_list, symbol_complexity, value_complexity)
            postfixEq2Infix = random_change(postfix_list, formula_list, symbol_complexity, value_complexity)
            postfixEq2postfix = random_change(postfix_list, postfix_list, symbol_complexity, value_complexity)
            prefixEq2Infix = random_change(prefix_list, formula_list, symbol_complexity, value_complexity)
            prefixEq2Postfix = random_change(prefix_list, postfix_list, symbol_complexity, value_complexity)
            prefixEq2Prefix = random_change(prefix_list, prefix_list, symbol_complexity, value_complexity)
            infixEq2Postfix = random_change(formula_list, postfix_list, symbol_complexity, value_complexity)
            infixEq2Prefix = random_change(formula_list, prefix_list, symbol_complexity, value_complexity)
            infixEq2Infix = random_change(formula_list, formula_list, symbol_complexity, value_complexity)
            ans = eval(formula)
            if abs(ans) < 10**6:
                ans = round(ans, 2)
                dataset.append((convert_to_string(formula_list), convert_to_string(postfix_list), convert_to_string(prefix_list), ans, postfixEq2Prefix, postfixEq2Infix,postfixEq2postfix, prefixEq2Infix, prefixEq2Postfix, prefixEq2Prefix, infixEq2Postfix, infixEq2Prefix, infixEq2Infix))
                i += 1
        except:
            i = i

    return dataset


def save_dataset(dataset, save_path, column_names):
    with open(save_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        for data in dataset:
            writer.writerow(data)


def gen_all_datasets():
    symbol_complexity_list = ["easy" , "medium", "hard"]
    value_complexity_list = ["easy", "easy_float", "medium", "medium_float", "hard", "hard_float"]
    length_list = ["easy", "medium", "hard"]
    num_samples = formula_config.formula_config["dataset_size"]
    save_path = "./dataset/Formula_tune/" 
    for symbol_complexity in symbol_complexity_list:
        for value_complexity in value_complexity_list:
            for length in length_list:
                print(f"Generating dataset for {symbol_complexity} {value_complexity} {length}")
                infix_cal = []
                postfix_cal = []
                prefix_cal = []
                infix2postfix = []
                infix2prefix = []
                postfix2infix = []
                postfix2prefix = []
                prefix2infix = []
                prefix2postfix = []
                postfixEq2PrefixList = []
                postfixEq2InfixList = []
                postfixEq2postfixList = []
                prefixEq2InfixList = []
                prefixEq2PostfixList = []
                prefixEq2PrefixList = []
                infixEq2PostfixList = []
                infixEq2PrefixList = []
                infixEq2InfixList = []

                dataset = gen_dataset(formula_config.formula_config["symbol complexity"][symbol_complexity], 
                                      formula_config.formula_config["value complexity"][value_complexity], 
                                      formula_config.formula_config["length"][length], num_samples)
                for i, data in enumerate(dataset):
                    formula, postfix_list, prefix_list, result, postfixEq2Prefix, postfixEq2Infix,postfixEq2postfix, prefixEq2Infix, prefixEq2Postfix, prefixEq2Prefix, infixEq2Postfix, infixEq2Prefix, infixEq2Infix = data         
                    infix_cal.append([formula, result])
                    postfix_cal.append([postfix_list, result])
                    prefix_cal.append([prefix_list, result])
                    infix2postfix.append([formula, postfix_list])
                    infix2prefix.append([formula, prefix_list])
                    postfix2infix.append([postfix_list, formula])
                    postfix2prefix.append([postfix_list, prefix_list])
                    prefix2infix.append([prefix_list, formula])
                    prefix2postfix.append([prefix_list, postfix_list])
                    postfixEq2PrefixList.append(postfixEq2Prefix)
                    postfixEq2InfixList.append(postfixEq2Infix)
                    postfixEq2postfixList.append(postfixEq2postfix)
                    prefixEq2InfixList.append(prefixEq2Infix)
                    prefixEq2PostfixList.append(prefixEq2Postfix)
                    prefixEq2PrefixList.append(prefixEq2Prefix)
                    infixEq2PostfixList.append(infixEq2Postfix)
                    infixEq2PrefixList.append(infixEq2Prefix)
                    infixEq2InfixList.append(infixEq2Infix)

                CalculateColumnNames = ["Formula", "Result"]
                ConvertColumnNames = ["Formula", "Result"]
                EqualColumnNames = ["Original","Perturbed","Is_Equivalent"]
                os.makedirs(save_path + "calculate", exist_ok=True)
                os.makedirs(save_path + "convert", exist_ok=True)
                os.makedirs(save_path + "equivalent", exist_ok=True)
                save_dataset(infix_cal, save_path + f"calculate/infix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", CalculateColumnNames)
                save_dataset(postfix_cal, save_path + f"calculate/postfix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", CalculateColumnNames)
                save_dataset(prefix_cal, save_path + f"calculate/prefix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", CalculateColumnNames)
                
                save_dataset(infix2postfix, save_path + f"convert/infix2postfix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", ConvertColumnNames)
                save_dataset(infix2prefix, save_path + f"convert/infix2prefix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", ConvertColumnNames)
                save_dataset(postfix2infix, save_path + f"convert/postfix2infix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", ConvertColumnNames)
                save_dataset(postfix2prefix, save_path + f"convert/postfix2prefix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", ConvertColumnNames)
                save_dataset(prefix2infix, save_path + f"convert/prefix2infix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", ConvertColumnNames)
                save_dataset(prefix2postfix, save_path + f"convert/prefix2postfix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", ConvertColumnNames)
                
                save_dataset(postfixEq2PrefixList, save_path + f"equivalent/postfixEq2prefix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", EqualColumnNames)
                save_dataset(postfixEq2InfixList, save_path + f"equivalent/postfixEq2infix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", EqualColumnNames)
                save_dataset(postfixEq2postfixList, save_path + f"equivalent/postfixEq2postfix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", EqualColumnNames)
                save_dataset(prefixEq2InfixList, save_path + f"equivalent/prefixEq2infix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", EqualColumnNames)
                save_dataset(prefixEq2PostfixList, save_path + f"equivalent/prefixEq2postfix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", EqualColumnNames)
                save_dataset(prefixEq2PrefixList, save_path + f"equivalent/prefixEq2prefix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", EqualColumnNames)
                save_dataset(infixEq2PostfixList, save_path + f"equivalent/infixEq2postfix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", EqualColumnNames)
                save_dataset(infixEq2PrefixList, save_path + f"equivalent/infixEq2prefix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", EqualColumnNames)
                save_dataset(infixEq2InfixList, save_path + f"equivalent/infixEq2infix_symbol_{symbol_complexity}_value_{value_complexity}_length_{length}.csv", EqualColumnNames)

                




if __name__ == "__main__":
    gen_all_datasets()