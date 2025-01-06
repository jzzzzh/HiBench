from decimal import Decimal, getcontext
import pandas as pd
import re

# Set high precision for decimal operations
getcontext().prec = 3

def is_number(string):
    """Check if a string is a valid number (integer or floating point)"""
    try:
        float(string)
        return True
    except ValueError:
        return False

def apply_operator(a: Decimal, b: Decimal, operator: str) -> Decimal:
    """Apply an operator to two operands"""
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        return a / b
    elif operator == '^':
        return a ** b
    else:
        raise ValueError(f"Unsupported operator: {operator}")

def evaluate_prefix(expression):
    stack = []
    operators = set(['+', '-', '*', '/', '^'])
    tokens = expression.split()

    # Reverse operand order
    for token in reversed(tokens):
        if token in operators:
            if len(stack) < 2:
                raise ValueError(f"Not enough operands in the stack: {expression}")
            left_operand = stack.pop()
            right_operand = stack.pop()
            stack.append(apply_operator(left_operand, right_operand, token))
        else:
            if is_number(token):
                stack.append(Decimal(token))
            else:
                raise ValueError(f"Invalid token '{token}' in prefix expression.")

    if len(stack) != 1:
        raise ValueError(f"Incorrect result: {expression}")
    return stack[0]

def evaluate_infix(expression):
    def precedence(op):
        if op == 'unary-':
            return 4  # Unary minus has the highest precedence
        elif op in ('^',):
            return 3
        elif op in ('*', '/'):
            return 2
        elif op in ('+', '-'):
            return 1
        else:
            return 0

    # Operator associativity definitions
    op_associativity = {
        'unary-': 'right',
        '^': 'right',
        '*': 'left',
        '/': 'left',
        '+': 'left',
        '-': 'left',
    }

    # Modify the regular expression to support unary minus
    tokens = re.findall(r'\d+\.\d+|\d+|[()+\-*/^]', expression)
    
    # Process unary minus
    def process_unary_operators(tokens):
        processed_tokens = []
        prev_token = None
        for token in tokens:
            if token == '-' and (prev_token is None or prev_token in '()+-*/^'):
                processed_tokens.append('unary-')
            else:
                processed_tokens.append(token)
            prev_token = token
        return processed_tokens

    tokens = process_unary_operators(tokens)

    def apply_operator_inner(a, b, op):
        return apply_operator(a, b, op)

    values = []
    operators_stack = []

    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == 'unary-':
            # Unary minus, push it as an operator to the stack
            operators_stack.append(token)
        elif is_number(token):
            values.append(Decimal(token))
            # Check if there's a unary minus to handle
            while operators_stack and operators_stack[-1] == 'unary-':
                operators_stack.pop()
                a = values.pop()
                values.append(a * Decimal('-1'))
        elif token == '(':
            operators_stack.append(token)
        elif token == ')':
            while operators_stack and operators_stack[-1] != '(':
                op = operators_stack.pop()
                if op == 'unary-':
                    if not values:
                        raise ValueError(f"Missing operand: {expression}")
                    a = values.pop()
                    values.append(a * Decimal('-1'))
                else:
                    if len(values) < 2:
                        raise ValueError(f"Missing operand: {expression}")
                    b = values.pop()
                    a = values.pop()
                    values.append(apply_operator_inner(a, b, op))
            if operators_stack and operators_stack[-1] == '(':
                operators_stack.pop()
            else:
                raise ValueError(f"Unmatched parentheses: {expression}")
            # Check if there's a unary minus to handle
            while operators_stack and operators_stack[-1] == 'unary-':
                operators_stack.pop()
                a = values.pop()
                values.append(a * Decimal('-1'))
        elif token in ('+', '-', '*', '/', '^'):
            assoc = op_associativity[token]
            while (operators_stack and operators_stack[-1] != '(' and
                   ((precedence(operators_stack[-1]) > precedence(token)) or
                    (precedence(operators_stack[-1]) == precedence(token) and
                     assoc == 'left'))):
                op = operators_stack.pop()
                if op == 'unary-':
                    if not values:
                        raise ValueError(f"Missing operand: {expression}")
                    a = values.pop()
                    values.append(a * Decimal('-1'))
                else:
                    if len(values) < 2:
                        raise ValueError(f"Missing operand: {expression}")
                    b = values.pop()
                    a = values.pop()
                    values.append(apply_operator_inner(a, b, op))
            operators_stack.append(token)
        else:
            raise ValueError(f"Unknown token: {token}")
        index += 1

    while operators_stack:
        op = operators_stack.pop()
        if op == 'unary-':
            if not values:
                raise ValueError(f"Missing operand: {expression}")
            a = values.pop()
            values.append(a * Decimal('-1'))
        else:
            if len(values) < 2:
                raise ValueError(f"Missing operand: {expression}")
            b = values.pop()
            a = values.pop()
            values.append(apply_operator_inner(a, b, op))

    if len(values) != 1:
        raise ValueError(f"Incorrect result: {expression}")
    return values[0]

def evaluate_postfix(expression):
    stack = []
    operators = set(['+', '-', '*', '/', '^'])
    tokens = expression.split()

    for token in tokens:
        if token in operators:
            if len(stack) < 2:
                raise ValueError(f"Not enough operands in the stack: {expression}")
            b = stack.pop()
            a = stack.pop()
            stack.append(apply_operator(a, b, token))
        else:
            if is_number(token):
                stack.append(Decimal(token))
            else:
                raise ValueError(f"Invalid token '{token}' in postfix expression.")

    if len(stack) != 1:
        raise ValueError(f"Incorrect result: {expression}")
    return stack[0]

def main():
    try:
        df = pd.read_csv('converted_expressions.csv')
        print(f"Successfully loaded dataset with {len(df)} records.")
    except Exception as e:
        print(f"Failed to read the dataset: {e}")
        return

    results = []

    for index, row in df.iterrows():
        source_expr = row['Source Expression']
        converted_expr = row['Converted Expression']
        target_type = row['Target Type']

        print(f"Processing record {index + 1}/{len(df)}, Source: {source_expr}, Converted: {converted_expr}")

        try:
            # Evaluate source expression
            if row['Source Type'] == 'Infix':
                source_value = evaluate_infix(source_expr)
            elif row['Source Type'] == 'Prefix':
                source_value = evaluate_prefix(source_expr)
            elif row['Source Type'] == 'Postfix':
                source_value = evaluate_postfix(source_expr)
            else:
                raise ValueError(f"Unknown source type: {row['Source Type']}")

            # Evaluate converted expression
            if target_type == 'Infix':
                converted_value = evaluate_infix(converted_expr)
            elif target_type == 'Prefix':
                converted_value = evaluate_prefix(converted_expr)
            elif target_type == 'Postfix':
                converted_value = evaluate_postfix(converted_expr)
            else:
                raise ValueError(f"Unknown target type: {target_type}")

            results.append({
                'Source Type': row['Source Type'],
                'Source Expression': source_expr,
                'Source Value': source_value,
                'Target Type': target_type,
                'Converted Expression': converted_expr,
                'Converted Value': converted_value
            })

        except Exception as e:
            print(f"Computation failed, Source: {source_expr}, Converted: {converted_expr}, Error: {e}")
            results.append({
                'Source Type': row['Source Type'],
                'Source Expression': source_expr,
                'Source Value': None,
                'Target Type': target_type,
                'Converted Expression': converted_expr,
                'Converted Value': None
            })

    results_df = pd.DataFrame(results)
    results_df.to_csv('evaluated_expressions.csv', index=False)
    print("Results saved to 'evaluated_expressions.csv'.")

if __name__ == "__main__":
    main()
