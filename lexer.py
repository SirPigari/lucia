import re

OPERATORS = [
    "->",
    ">=",
    "<=",
    "==",
    "!=",
    "+=",
    "-=",
    "*=",
    "/=",
    "=",
    "+",
    "-",
    "^",
    "*",
    "/",
    ">",
    "<",
    "!",
    "%",
    "||",
    "&&",
    "|",
    "#",
    "~",
]

# Token specifications
TOKEN_SPECIFICATION = [
    ('NUMBER', r'-?\b\d+(\.\d+)?\b'),                                               # Integer or decimal number
    ('STRING', r'".*?"|\'.*?\''),                                                   # Double or single quoted string
    ('BOOLEAN', r'\b(true|false|null)\b'),                                          # Boolean literals
    ('COMMENT_INLINE', r'<#.*?#>'),                                                 # In-line comment
    ('COMMENT_SINGLE', r'//.*'),                                                    # Single-line comment
    ('COMMENT_MULTI', r'/\*[\s\S]*?\*/'),                                           # Multi-line comment (replaces DOTALL flag)
    ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),                                            # Identifiers (variable/function names)
    ('OPERATOR', r'|'.join(re.escape(op) for op in OPERATORS)),                     # Operators
    ('SEPARATOR', r'\.\.\.|[(){}\[\];:.,]'),                                        # Separators
    ('WHITESPACE', r'\s+'),                                                         # Whitespace
    ('INVALID', r'.')                                                               # Any other characters
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)


def lexer(code, include_comments=False):
    tokens = []
    for match in re.finditer(TOKEN_REGEX, code):
        token_type = match.lastgroup
        value = match.group(token_type)
        if token_type in ('COMMENT_SINGLE', 'COMMENT_MULTI', 'COMMENT_INLINE'):
            if not include_comments:
                continue
            else:
                value = re.sub(r' {4}|	| {3}| {2}', '\\t', value)
        if token_type != 'WHITESPACE':
            tokens.append((token_type, value))
    return tokens


if __name__ == "__main__":
    code = '''
    public static final fun main() -> void:
        print("hello world")
    end
    
    main()
    '''

    tokens = lexer(code, include_comments=True)
    for token in tokens:
        print(token)
