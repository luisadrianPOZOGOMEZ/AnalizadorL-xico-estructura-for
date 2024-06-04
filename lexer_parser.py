import re


def analyze_code(code):
    lexical_analysis = perform_lexical_analysis(code)
    syntactic_analysis = perform_syntactic_analysis(code)
    return lexical_analysis, syntactic_analysis


def perform_lexical_analysis(code):
    tokens = []
    token_specification = [
        ('INT', r'int'),
        ('ID', r'[A-Za-z_][A-Za-z0-9_]*'),
        ('NUMBER', r'\d+'),
        ('OP', r'[+\-*/=<>]'),
        ('PAREN', r'[()]'),
        ('BRACE', r'[{}]'),
        ('SEMICOLON', r';'),
        ('WHITESPACE', r'\s+'),
        ('STRING', r'".*?"'),
        ('DOT', r'\.'),
        ('UNKNOWN', r'.')
    ]
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind != 'WHITESPACE':
            tokens.append((kind, value))
    return tokens


def perform_syntactic_analysis(code):
    # Verificar estructura básica del for
    for_pattern = re.compile(
        r'for\s*\(\s*int\s+[A-Za-z_][A-Za-z0-9_]*\s*=\s*\d+\s*;\s*[A-Za-z_][A-Za-z0-9_]*\s*[<>=!]+\s*\d+\s*;\s*[A-Za-z_][A-Za-z0-9_]*\s*\+\+\s*\)\s*\{\s*System\.out\.println\(".*"\s*\+\s*[A-Za-z_][A-Za-z0-9_]*\s*\);\s*\}',
        re.DOTALL
    )

    if not for_pattern.search(code):
        return "Error sintáctico: Estructura básica del FOR incorrecta"

    # Extraer el cuerpo del bucle for
    for_body_pattern = re.compile(r'\{([^}]*)\}', re.DOTALL)
    body_match = for_body_pattern.search(code)
    if body_match:
        body = body_match.group(1).strip()
        # Verificar que cada sentencia termine con ';'
        statements = body.split('\n')
        for statement in statements:
            if statement.strip() and not statement.strip().endswith(';'):
                return f"Error sintáctico: falta ';' en la sentencia: {statement.strip()}"

    return "Estructura FOR correcta"
