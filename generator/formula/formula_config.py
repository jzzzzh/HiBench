from decimal import Decimal

formula_config = {
    "symbol complexity":{
        "easy": ["+", "-", "*", "/"],
        "medium": ["+", "-", "*", "/", "(", ")"],
        "hard": ["+", "-", "*", "/", "^", "(", ")"],
        "logic": ["and", "or", "not", "xor", "=>", "<=>", "(", ")"],
    },
    "value complexity":{
        "easy": range(1, 100),
        "easy_float": [round(x * 0.01, 2) for x in range(1, 1001)],
        "medium": range(-100, 100),
        "medium_float": [round(x * 0.01, 2) for x in range(-10000, 10001)],
        "hard": range(-1000, 1000),
        "hard_float": [round(x * 0.01, 2) for x in range(-100000, 100001)],
        },
    "length": {
        "easy": 5,
        "medium": 10,
        "hard": 15,
    },
}

