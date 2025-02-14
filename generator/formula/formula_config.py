from decimal import Decimal

formula_config = {
    "symbol complexity":{
        "easy": ["+", "-", "*", "/"],
        "medium": ["+", "-", "*", "/", "(", ")"],
        "hard": ["+", "-", "*", "/", "^", "(", ")"],
        "logic": ["and", "or", "not", "xor", "=>", "<=>", "(", ")"],
    },
    "value complexity":{
        "easy": range(1, 10),
        "easy_float": [round(x * 0.01, 2) for x in range(1, 11)],
        "medium": range(-50, 50),
        "medium_float": [round(x * 0.01, 2) for x in range(-50, 51)],
        "hard": range(-100, 100),
        "hard_float": [round(x * 0.01, 2) for x in range(-100, 101)],
        },
    "length": {
        "easy": 3,
        "medium": 6,
        "hard": 9,
    },
    "dataset_size": 2,
}

