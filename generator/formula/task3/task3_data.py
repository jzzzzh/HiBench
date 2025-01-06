# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 19:05:53 2024

@author: JC TU
"""

import random
import csv
from typing import List, Tuple

# Define operators and their precedence
OPERATORS = {
    '+': {'precedence': 1, 'associativity': 'L'},
    '-': {'precedence': 1, 'associativity': 'L'},
    '*': {'precedence': 2, 'associativity': 'L'},
    '/': {'precedence': 2, 'associativity': 'L'},
    '^': {'precedence': 3, 'associativity': 'R'}
}

# Define operand generation
def generate_operand() -> str:
    # Generate decimal with certain probability
    if random.random() < 0.3:  # 30% probability of generating a decimal
        return f"{random.randint(1, 999)}.{random.randint(0, 99)}"  # Generate decimal
    else:
        return str(random.randint(1, 999))  # Generate integer

# Modify operand generation logic
OPERANDS = [generate_operand() for _ in range(1000)]

# Define operator count per category
CATEGORY_OPERATOR_COUNT = {
    'Simple': (2, 5),
    'Medium': (6, 10),
    'Hard': (11, 15)
}

# Expression categories
CATEGORIES = ['Simple', 'Medium', 'Hard']

# Expression Generator Class
class ExpressionGenerator:
    def __init__(self):
        pass

    def generate_expression(self, num_operators: int) -> str:
        if num_operators == 0:
            return generate_operand()  # Use the new operand generation function
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

# Infix to postfix (Postfix) conversion using Shunting Yard algorithm
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

# Infix to prefix conversion
def infix_to_prefix(expression: str) -> str:
    # First reverse the expression
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
    # Convert postfix to prefix
    prefix = ' '.join(postfix.split()[::-1])
    return prefix

# Evaluate the postfix expression result
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
        return a / b  # Assume the divisor is non-zero
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
            # Normalize the expression (remove extra spaces)
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
                # If the expression is invalid (e.g., division by zero), skip it and generate a new expression
                continue
    return dataset

# Save dataset to CSV file
def save_dataset_to_csv(dataset: List[Tuple[str, str, str, str, float]], filename: str = 'expression_dataset_with_results.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Infix', 'Prefix', 'Postfix', 'Category', 'Result'])
        for data in dataset:
            writer.writerow(data)

# Main function
if __name__ == "__main__":
    dataset = generate_dataset(expressions_per_category=1000)  # Generate 1000 expressions per category
    save_dataset_to_csv(dataset, 'expression_dataset_with_results.csv')
    print("Dataset has been generated and saved as 'expression_dataset_with_results.csv'")
