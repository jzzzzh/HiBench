import re

pattern = (
    r'\{\s*'  # Match the opening brace with optional spaces
    r'["\']?' + 'answer' + r'["\']?\s*[:=]\s*'  # Match "answer" with optional quotes, followed by ':' or '='
    r'('  # Start a capturing group for the answer content
    r'"([^"]*)"' # Match double-quoted content (answer with double quotes)
    r'|'  # OR
    r"'([^']*)"  # Match single-quoted content (answer with single quotes)
    r'|'  # OR
    r'([^}\n]*)'  # Match unquoted content (anything except '}' or newlines)
    r')'  # End of the capturing group
    r'\s*\}?'  # Ensure the match ends at the first closing brace (optional)
)

test_cases = [
    "{ answer : 'Hello World' }",
    '{"answer":  O(1)}',
    "{'answer':  O(1)}",
    '{answer:  O(1)}',
    '{"answer": "O(1)"}',
    "{'answer': 'O(1)'}",
    '{ "answer" : O(1) }',
    '{ "answer" = "Complex response with: special characters #@!$%" }',
    '{ "answer": "Multiline \n response test" }',
    '{ "answer" = 12345 }',
    '{ "answer" = \'Single quoted answer\' }',
    '{ "ANSWER" = "Complex value with = inside" }',
    '{ "answer": Unquoted response without closing brace',
    '{ "answer": Another response that just goes on and on',
    '{ "answer": "This is a response with quotes inside: "hello""}',
]

for test in test_cases:
    test = test.lower()  # Convert the input to lowercase for case-insensitive matching
    match = re.search(pattern, test)
    if match:
        extracted_value = match.group(1)
        print(f"Matched: {extracted_value}")
    else:
        print("No match")
