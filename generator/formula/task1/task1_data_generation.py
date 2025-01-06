# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 11:48:30 2024

@author: JC TU
"""

import random
import csv
from typing import List, Tuple
import copy

# Define operators and their precedence
OPERATORS = {
    '+': {'precedence': 1, 'associativity': 'L'},
    '-': {'precedence': 1, 'associativity': 'L'},
    '*': {'precedence': 2, 'associativity': 'L'},
    '/': {'precedence': 2, 'associativity': 'L'},
    '^': {'precedence': 3, 'associativity': 'R'}
}

# Define operands
OPERANDS = [str(i) for i in range(1, 1000)]

# Define operator count by category
CATEGORY_OPERATOR_COUNT = {
    'Simple': (2, 5),
    'Medium': (6, 10),
    'Hard': (11, 15)
}

# Expression categories
CATEGORIES = ['Simple', 'Medium', 'Hard']

# Expression generator class
class ExpressionGenerator:
    def __init__(self):
        pass

    def generate_expression(self, num_operators: int) -> str:
        if num_operators == 0:
            return random.choice(OPERANDS)
        else:
            op = random.choice(list(OPERATORS.keys()))
            left_operators = random.randint(0, num_operators - 1)
            right_operators = num_operators - 1 - left_operators
            left = self.generate_expression(left_operators)
            right = self.generate_expression(right_operators)
            # Randomly decide whether to add parentheses
            if random.choice([True, False]):
                return f"( {left} {op} {right} )"
            else:
                return f"{left} {op} {right}"

# Infix to postfix (Postfix) using the Shunting Yard algorithm
def infix_to_postfix(expression: str) -> str:
    stack = []
    output = []
    tokens = expression.split()
    for token in tokens:
        if token in OPERATORS:
            while stack and stack[-1] != '(':
                top = stack[-1]
                if (OPERATORS[top]['precedence'] > OPERATORS[token]['precedence']) or \
                   (OPERATORS[top]['precedence'] == OPERATORS[token]['precedence'] and OPERATORS[token]['associativity'] == 'L'):
                    output.append(stack.pop())
                else:
                    break
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Pop '('
        else:
            # Operand
            output.append(token)
    while stack:
        output.append(stack.pop())
    return ' '.join(output)

# Infix to prefix
def infix_to_prefix(expression: str) -> str:
    # Reverse the expression first
    tokens = expression.split()[::-1]
    reversed_expr = []
    for token in tokens:
        if token == '(':
            reversed_expr.append(')')
        elif token == ')':
            reversed_expr.append('(')
        else:
            reversed_expr.append(token)
    reversed_expr_str = ' '.join(reversed_expr)
    # Use infix to postfix
    postfix = infix_to_postfix(reversed_expr_str)
    # Postfix to prefix
    prefix = ' '.join(postfix.split()[::-1])
    return prefix

# Evaluate postfix expression
def evaluate_postfix(postfix_expr: str) -> float:
    stack = []
    tokens = postfix_expr.split()
    for token in tokens:
        if token in OPERATORS:
            if len(stack) < 2:
                raise ValueError("Invalid postfix expression")
            b = stack.pop()
            a = stack.pop()
            result = apply_operator(a, b, token)
            stack.append(result)
        else:
            stack.append(float(token))
    if len(stack) != 1:
        raise ValueError("Invalid postfix expression after evaluation")
    return stack[0]

def apply_operator(a: float, b: float, operator: str) -> float:
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return a / b
    elif operator == '^':
        return a ** b
    else:
        raise ValueError(f"Unsupported operator: {operator}")

# Generate dataset
def generate_dataset(expressions_per_category: int = 100) -> List[Tuple[str, str, str, str, float]]:
    generator = ExpressionGenerator()
    dataset = []
    for category in CATEGORIES:
        min_ops, max_ops = CATEGORY_OPERATOR_COUNT[category]
        generated = 0
        while generated < expressions_per_category:
            num_operators = random.randint(min_ops, max_ops)
            infix = generator.generate_expression(num_operators)
            # Standardize the expression (remove extra spaces)
            infix_tokens = infix.replace('(', '( ').replace(')', ' )').split()
            infix_standard = ' '.join(infix_tokens)
            try:
                postfix = infix_to_postfix(infix_standard)
                prefix = infix_to_prefix(infix_standard)
                result = evaluate_postfix(postfix)
                # Round the result to 2 decimal places
                result = round(result, 2)
                dataset.append((infix_standard, prefix, postfix, category, result))
                generated += 1
            except Exception as e:
                # If the expression is invalid (e.g., division by zero), skip and generate a new expression
                continue
    return dataset

# Save dataset to CSV file
def save_dataset_to_csv(dataset: List[Tuple[str, str, str, str, float]], filename: str = 'expression_dataset_with_results.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Infix', 'Prefix', 'Postfix', 'Category', 'Result'])
        for data in dataset:
            writer.writerow(data)

# Define perturbation methods
def perturb_expression(expression: str, perturb_type: str = 'swap') -> str:
    """
    Perturb the operator position in the expression based on perturbation type
    perturb_type: 'swap' or 'replace'
    """
    tokens = expression.split()
    # Get all the operator positions
    op_positions = [i for i, token in enumerate(tokens) if token in OPERATORS]
    if not op_positions:
        # No operators in the expression, cannot perturb
        return expression
    if perturb_type == 'swap':
        if len(op_positions) < 2:
            # Cannot swap, return original expression
            return expression
        # Randomly swap two operator positions
        pos1, pos2 = random.sample(op_positions, 2)
        tokens[pos1], tokens[pos2] = tokens[pos2], tokens[pos1]
    elif perturb_type == 'replace':
        # Randomly replace an operator position
        pos = random.choice(op_positions)
        original_op = tokens[pos]
        possible_ops = list(OPERATORS.keys())
        possible_ops.remove(original_op)
        new_op = random.choice(possible_ops)
        tokens[pos] = new_op
    else:
        # Undefined perturbation method, return original expression
        return expression
    perturbed_expression = ' '.join(tokens)
    return perturbed_expression

# Load original dataset
def load_original_dataset(filename: str = 'expression_dataset_with_results.csv') -> List[Tuple[str, str, str, str, float]]:
    dataset = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            infix = row['Infix']
            prefix = row['Prefix']
            postfix = row['Postfix']
            category = row['Category']
            result = float(row['Result'])
            dataset.append((infix, prefix, postfix, category, result))
    return dataset

# Generate perturbed dataset
def generate_perturbed_dataset(original_dataset: List[Tuple[str, str, str, str, float]],
                               perturb_ratio: float = 0.3,
                               perturb_types: List[str] = ['swap', 'replace']) -> List[Tuple]:
    """
    Perturb the original dataset to generate a new dataset
    perturb_ratio: The ratio of expressions to perturb (e.g., 0.3 means 30%)
    perturb_types: List of perturbation types
    """
    perturbed_dataset = []
    num_to_perturb = int(len(original_dataset) * perturb_ratio)
    indices = random.sample(range(len(original_dataset)), num_to_perturb)
    for i, data in enumerate(original_dataset):
        infix, prefix, postfix, category, original_result = data
        if i in indices:
            perturb_type = random.choice(perturb_types)
            # Perturb the infix expression
            perturbed_infix = perturb_expression(infix, perturb_type)
            try:
                perturbed_postfix = infix_to_postfix(perturbed_infix)
                perturbed_prefix = infix_to_prefix(perturbed_infix)
                perturbed_result = evaluate_postfix(perturbed_postfix)
                perturbed_result = round(perturbed_result, 2)
                # Calculate equivalence between the expressions
                is_equiv_infix = (perturbed_result == original_result)
                is_equiv_prefix = (perturbed_result == original_result)
                is_equiv_postfix = (perturbed_result == original_result)
                # Equivalence between other expressions
                is_equiv_infix_prefix = (perturbed_result == original_result)  # Example, adjust as needed
                is_equiv_infix_postfix = (perturbed_result == original_result)
                is_equiv_prefix_postfix = (perturbed_result == original_result)
                # Check equivalence between all expression formats
                is_equiv_any = is_equiv_infix and is_equiv_prefix and is_equiv_postfix
                perturbed_dataset.append((
                    infix, perturbed_infix,
                    prefix, perturbed_prefix,
                    postfix, perturbed_postfix,
                    category,
                    original_result, perturbed_result,
                    is_equiv_infix,
                    is_equiv_prefix,
                    is_equiv_postfix,
                    is_equiv_infix_prefix,
                    is_equiv_infix_postfix,
                    is_equiv_prefix_postfix
                ))
            except Exception as e:
                # If the perturbed expression is invalid, skip
                continue
        else:
            # Do not perturb, keep the original data and set equivalences to True
            perturbed_dataset.append((
                infix, infix,
                prefix, prefix,
                postfix, postfix,
                category,
                original_result, original_result,
                True,  # Is_Equivalent_Infix
                True,  # Is_Equivalent_Prefix
                True,  # Is_Equivalent_Postfix
                True,  # Is_Equivalent_Infix_Prefix
                True,  # Is_Equivalent_Infix_Postfix
                True   # Is_Equivalent_Prefix_Postfix
            ))
    return perturbed_dataset

# Save perturbed dataset to CSV file
def save_perturbed_dataset_to_csv(perturbed_dataset: List[Tuple], filename: str = 'expression_dataset_with_perturbations.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Original_Infix', 'Perturbed_Infix',
            'Original_Prefix', 'Perturbed_Prefix',
            'Original_Postfix', 'Perturbed_Postfix',
            'Category',
            'Original_Result', 'Perturbed_Result',
            'Is_Equivalent_Infix',
            'Is_Equivalent_Prefix',
            'Is_Equivalent_Postfix',
            'Is_Equivalent_Infix_Prefix',
            'Is_Equivalent_Infix_Postfix',
            'Is_Equivalent_Prefix_Postfix'
        ])
        for data in perturbed_dataset:
            writer.writerow(data)

# Main function
if __name__ == "__main__":
    # Step 1: Generate and save the original dataset (if not already generated)
    original_csv = 'expression_dataset_with_results.csv'
    try:
        original_dataset = load_original_dataset(original_csv)
        print(f"Original dataset loaded with {len(original_dataset)} records.")
    except FileNotFoundError:
        print("Original dataset not found, generating...")
        original_dataset = generate_dataset(expressions_per_category=1000)  # Generate 1000 expressions per category
        save_dataset_to_csv(original_dataset, original_csv)
        print(f"Original dataset generated and saved as '{original_csv}'.")

    # Step 2: Generate the perturbed dataset
    perturbed_dataset = generate_perturbed_dataset(original_dataset, perturb_ratio=0.3, perturb_types=['swap', 'replace'])
    perturbed_csv = 'expression_dataset_with_perturbations.csv'
    save_perturbed_dataset_to_csv(perturbed_dataset, perturbed_csv)
    print(f"Perturbed dataset generated and saved as '{perturbed_csv}'.")
