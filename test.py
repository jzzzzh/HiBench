dict1 = {'a': 1, 'b': 2}
result = '_'.join([f"{key}_{value}" for key, value in dict1.items()])
print(result)