import re


class BasicEvaluator(object):
    """String Matching Evaluation Process:
        1. Robust answer extraction from the given format, it should consider:
            - Answer in double or single quotes: The answer may be enclosed in double (`"`) or single (`'`) quotes, and we need to correctly capture this content.
            - Unquoted answers: The answer could be a simple value like `O(1)`, `12345`, or other expressions that are not enclosed in quotes.
            - Whitespace tolerance: The answer extraction should account for optional spaces around key components (e.g., around the `:` or `=` sign).
            - Handling of mixed quote types: The answer might contain quotes inside the value itself (e.g., `This is a response with quotes inside: "hello"`), and the regex should correctly capture the entire content, without prematurely stopping at the internal quotes.
            - Correct match termination: The extraction should stop at the first closing brace `}` to ensure that we capture the entire answer part. If no closing brace is provided, it should capture all remaining content up to the next brace or line break.
            - Flexible handling of key name: The key `answer` might be written in different cases (e.g., `"ANSWER"`, `"answer"`), so the matching should be case-insensitive.
            - Possible use of `=` instead of `:`: The separator between the key (`answer`) and its value can be either a colon (`:`) or an equals sign (`=`), and both should be supported.
            - Edge cases: The regex should handle cases where the format deviates slightly, such as missing closing braces, extra spaces, or mixed quote usage.


        2. Refine the extracted answer by:
            - replace multiple blank by single space blank.
            - remove the begin and ending blank and special symbols.
    """
    
    def __init__(self, key: str = 'answer', strip_symbols: str = '\'"'):
        self.key = key.lower()
        self.strip_symbols = list(strip_symbols)
        
    
    def __call__(self, task, source, target, *args, **kwargs):
        eval_func = getattr(self, task)
        ret = eval_func(source, target, *args, **kwargs)
        return ret
    
    def number_match(self, source: str, target: str) -> bool:
        source = source.lower()
        target = target.lower()
        source = self._extract_answer(source)
        source = self._refine_string(source)
        target = self._refine_string(target)
        if source is None:
            return False
        
        if target == str(source):
            return True
        else:
            return False
    
    def string_match(self, source: str, target: str, skip: str = None) -> bool:
        source = source.lower()
        target = target.lower()
        source = self._extract_answer(source)
        source = self._refine_string(source)
        target = self._refine_string(target)
        if source is None:
            return False
        if skip:
            source = re.sub(skip, '', source)
            target = re.sub(skip, '', target)
        # print(source)
        # print(target)
        if target == source or target in source:
            return True
        else:
            return False
        
    # def bool_match(self, source: str, target: str) -> bool:
    #     source = source.lower()
    #     target = target.lower()
    #     source = self._extract_answer(source)
    #     source = self._refine_string(source)
    #     target = self._refine_string(target)
    #     if source is None:
    #         return False
    #     if bool(target) == bool(source):
    #         return True
    #     else:
    #         return False
        
    def list_match(self, source: str, target: str, sep: str, remove_blank: bool = True):
        source = source.lower()
        target = target.lower()
        source = self._extract_answer(source)
        source = self._refine_string(source)
        target = self._refine_string(target)
        if source is None:
            return False
        if remove_blank:
            source = re.sub(r'\s+', '', source)
            target = re.sub(r'\s+', '', target)
        source = source.split(sep)
        target = target.split(sep)
        if not source:
            return False
        if not target:
            raise ValueError('empty target value.')
        for i, j in zip(sorted(source), sorted(target)):
            if i != j:
                return False
        return True
    
    def hierarchical_structure_match(self, source: str, target: str):
        source = source.lower()
        target = target.lower()
        source = self._extract_answer(source)
        source = self._refine_string(source)
        target = self._refine_string(target)
        if source is None:
            return False
        source = re.sub(r"\D", "", source)
        target = re.sub(r"\D", "", target)
        return source == target
    
    def hit_rate(self, source: str, target: str, sep: str, remove_blank: bool = True) -> float:
        source = source.lower()
        target = target.lower()
        source = self._extract_answer(source)
        target = self._extract_answer(target)
        if source is None:
            return 0.
        if remove_blank:
            source = re.sub(r'\s+', '', source)
            target = re.sub(r'\s+', '', target)
        source = source.split(sep)
        target = target.split(sep)
        source = [self._refine_string(s) for s in  source]
        target = [self._refine_string(s) for s in  target]
        if not source:
            return 0.
        if not target:
            raise ValueError('empty target value.')
        hit = 0.
        for i in target:
            if i in source:
                hit += 1
        return hit / len(target)
        
    def _extract_answer(self, string: str) -> str:
        string = string.lower()
        pattern = (
        r'\{\s*'  # Match the opening brace with optional spaces
        r'["\']?' + self.key + r'["\']?\s*[:=]\s*'  # Match "answer" with optional quotes, followed by ':' or '='
        r'('  # Start a capturing group for the answer content
        r'"([^"]*)"' # Match double-quoted content (answer with double quotes)
        r'|'  # OR
        r"'([^']*)"  # Match single-quoted content (answer with single quotes)
        r'|'  # OR
        r'([^}\n]*)'  # Match unquoted content (anything except '}' or newlines)
        r')'  # End of the capturing group
        r'\s*\}?'  # Ensure the match ends at the first closing brace (optional)
    )
        match = re.search(pattern, string)
        if not match:
            return None
        else:
            ret = match.group(1)
            if ret:
                return ret.strip()
            else:
                return None
    
    def _refine_string(self, string: str):
        if string is None:
            return None
        string = string.lower()
        string = string.strip()
        string = re.sub(r'\s+', ' ', string)
        string = re.sub(r'[^a-zA-Z0-9 ,]', '', string)
        for symbol in self.strip_symbols:
            string = string.strip(symbol)
        return string
    
    
if __name__ == '__main__':
    evaluator = BasicEvaluator()

    # Test Case 1: Basic string match (exact match)
    source = "{ answer : 'Hello World' }"
    target = "hello world"
    assert evaluator.string_match(source, target) == True

    # Test Case 2: String match with extra spaces and quotes
    source = "{ answer : '  Hello World  ' }"
    target = "hello world"
    assert evaluator.string_match(source, target) == True

    # Test Case 3: Case-insensitive string match (key case)
    source = "{ Answer: 'Hello World' }"
    target = "hello world"
    assert evaluator.string_match(source, target) == True

    # Test Case 4: Case-insensitive string match (value case)
    source = "{ answer : 'HELLO world' }"
    target = "hello world"
    assert evaluator.string_match(source, target) == True

    # Test Case 5: Match with boolean values
    source = "{ answer : true }"
    target = "True"
    assert evaluator.string_match(source, target) == True

    source = "{ answer : false }"
    target = "false"
    assert evaluator.string_match(source, target) == True
    
    source = "{ answer : false }"
    target = "true"
    assert evaluator.string_match(source, target) == False

    # Test Case 6: List match with unquoted values (order matters)
    source = "{ answer : 'apple, banana, cherry' }"
    target = "banana, apple, cherry"
    sep = ','
    assert evaluator.list_match(source, target, sep) == True

    # Test Case 7: List match with extra spaces (order doesn't matter)
    source = "{ answer : 'apple ,   banana, cherry ' }"
    target = " banana, apple, cherry "
    sep = ','
    assert evaluator.list_match(source, target, sep) == True

    # Test Case 8: Hierarchical structure match (matching unquoted content)
    source = "{ answer : '   1\n    |-- 0\n    `-- 2' }"
    target = "   1\n    |-- 0\n    `-- 2"
    assert evaluator.hierarchical_structure_match(source, target) == True

    # Test Case 9: Hierarchical structure match (mismatch)
    source = "{ answer :   1\n    |-- 0\n    `-- 2}"
    target = "   1\n    |-- 0\n    |   `-- 3\n    `-- 2"
    assert evaluator.hierarchical_structure_match(source, target) == False

    # Test Case 10: Handle edge case with missing closing brace
    source = "{ answer : 'unquoted content without brace"
    target = "unquoted content without brace"
    assert evaluator.string_match(source, target) == True

    # Test Case 11: Handle case with mixed quotes inside value
    source = "{ answer : 'response with \"quotes\" inside' }"
    target = "response with \"quotes\" inside"
    assert evaluator.string_match(source, target) == True

    # Test Case 12: Non-matching case
    source = "{ answer : 'apple' }"
    target = "orange"
    assert evaluator.string_match(source, target) == False

    # Test Case 13: Empty target value in list match
    source = "{ answer : 'apple, banana' }"
    target = ""
    sep = ','
    try:
        result = evaluator.list_match(source, target, sep)
    except ValueError as e:
        assert str(e) == 'empty target value.'
        
    # Test Case 14: List match with one element
    source = "{ answer : 'apple ' }"
    target = " apple "
    sep = ','
    assert evaluator.list_match(source, target, sep) == True

    # Test Case 15: Number match
    source = "{ answer : 12345 }"
    target = "12345"
    assert evaluator.number_match(source, target) == True
    

    print('all cases passed!')