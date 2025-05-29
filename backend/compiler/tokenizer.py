import re
# -----------------------
# STAGE 1: Lexer
# -----------------------
def lexer(js_code):
    tokens = []
    js_code = js_code.strip()

    # 1. Function declarations
    func_pattern = re.compile(r'function\s+(\w+)\s*\((.*?)\)\s*\{(.*?)\}', re.DOTALL)
    # Use finditer but accumulate matches to remove later safely
    matches = list(func_pattern.finditer(js_code))
    for match in matches:
        tokens.append({
            'type': 'function_declaration',
            'name': match.group(1),
            'params': [p.strip() for p in match.group(2).split(',')] if match.group(2).strip() else [],
            'body': match.group(3).strip()
        })
    # Remove matched function declarations
    for match in reversed(matches):
        js_code = js_code[:match.start()] + js_code[match.end():]

    # 2. Arrow function with braces: const add = (a, b) => { return a + b; }
    arrow_block = re.compile(r'(?:const|let|var)\s+(\w+)\s*=\s*\((.*?)\)\s*=>\s*\{(.*?)\}', re.DOTALL)
    matches = list(arrow_block.finditer(js_code))
    for match in matches:
        tokens.append({
            'type': 'arrow_function',
            'name': match.group(1),
            'params': [p.strip() for p in match.group(2).split(',')] if match.group(2).strip() else [],
            'body': match.group(3).strip() 
        })
    for match in reversed(matches):
        js_code = js_code[:match.start()] + js_code[match.end():]

    # 3. Arrow function with one param, no braces: const square = x => x * x
    arrow_inline_single = re.compile(r'(?:const|let|var)\s+(\w+)\s*=\s*(\w+)\s*=>\s*([^;]+)')
    matches = list(arrow_inline_single.finditer(js_code))
    for match in matches:
        tokens.append({
            'type': 'arrow_function',
            'name': match.group(1),
            'params': [match.group(2)],
            'body': f"return {match.group(3).strip()}"
        })
    for match in reversed(matches):
        js_code = js_code[:match.start()] + js_code[match.end():]

    # 4. Arrow function with no param, no braces: const hello = () => "Hi"
    arrow_inline_noparam = re.compile(r'(?:const|let|var)\s+(\w+)\s*=\s*\(\s*\)\s*=>\s*([^;]+);?')
    matches = list(arrow_inline_noparam.finditer(js_code))
    for match in matches:
        tokens.append({
            'type': 'arrow_function',
            'name': match.group(1),
            'params': [],
            'body': f"return {match.group(2).strip()}"
        })
    for match in reversed(matches):
        js_code = js_code[:match.start()] + js_code[match.end():]

    # --- if-else ---
    if_else_chain_pattern = re.compile(
        r'if\s*\((.*?)\)\s*\{(.*?)\}'              # Match initial if
        r'((?:\s*else\s+if\s*\(.*?\)\s*\{.*?\})*)'  # Match zero or more else if
        r'(?:\s*else\s*\{(.*?)\})?',               # Optional final else
        re.DOTALL
    )

    def extract_elseif_blocks(chain_str):
        elseif_pattern = re.compile(r'else\s+if\s*\((.*?)\)\s*\{(.*?)\}', re.DOTALL)
        return [{'condition': m.group(1).strip(), 'body': m.group(2).strip()}
                for m in elseif_pattern.finditer(chain_str)]

    matches = list(if_else_chain_pattern.finditer(js_code))
    for match in matches:
        condition = match.group(1).strip()
        body = match.group(2).strip()
        elseif_chain = extract_elseif_blocks(match.group(3))
        else_body = match.group(4).strip() if match.group(4) else None

        tokens.append({
            'type': 'if_statement_chain',
            'if': {'condition': condition, 'body': body},
            'elif': elseif_chain,
            'else': else_body
        })

    for match in reversed(matches):
        js_code = js_code[:match.start()] + js_code[match.end():]

    # 7. While loop
    while_pattern = re.compile(r'while\s*\((.*?)\)\s*\{(.*?)\}', re.DOTALL)
    matches = list(while_pattern.finditer(js_code))
    for match in matches:
        tokens.append({
            'type': 'while_loop',
            'condition': match.group(1).strip(),
            'body': match.group(2).strip()
        })
    for match in reversed(matches):
        js_code = js_code[:match.start()] + js_code[match.end():]

    # 8. Do-While loop
    do_while_pattern = re.compile(r'do\s*\{(.*?)\}\s*while\s*\((.*?)\)\s*;', re.DOTALL)
    matches = list(do_while_pattern.finditer(js_code))
    for match in matches:
        tokens.append({
            'type': 'do_while_loop',
            'condition': match.group(2).strip(),
            'body': match.group(1).strip()
        })
    for match in reversed(matches):
        js_code = js_code[:match.start()] + js_code[match.end():]

    # 9. For loop
    for_pattern = re.compile(r'for\s*\((.*?);(.*?);(.*?)\)\s*\{(.*?)\}', re.DOTALL)
    matches = list(for_pattern.finditer(js_code))
    for match in matches:
        tokens.append({
            'type': 'for_loop',
            'init': match.group(1).strip(),
            'condition': match.group(2).strip(),
            'increment': match.group(3).strip(),
            'body': match.group(4).strip()
        })
    for match in reversed(matches):
        js_code = js_code[:match.start()] + js_code[match.end():]

    # 6. Declarations and console.log
    lines = [line.strip() for line in js_code.split(';') if line.strip()]
    for line in lines:
        decl_match = re.match(r'^(let|const|var)\s+(\w+)\s*=\s*(.+)$', line)
        log_match = re.match(r'^console\.log\((.*)\)$', line)
        inc_match = re.match(r'^(\w+)\s*(\+\+|--)$', line)
        comp_assign_match = re.match(r'^(\w+)\s*([\+\-])=\s*(\d+)$', line)
        if decl_match:
            tokens.append({
                'type': 'declaration',
                'kind': decl_match.group(1),
                'name': decl_match.group(2),
                'value': decl_match.group(3).strip()
            })
        elif log_match:
            tokens.append({
                'type': 'console_log',
                'value': log_match.group(1).strip()
            })
        elif inc_match:
            var_name, op = inc_match.groups()
            tokens.append({
                'type': 'inc_dec_operation',
                'operator': op,
                'variable': var_name
            })
        elif comp_assign_match:
            var_name, operator, value = comp_assign_match.groups()
            tokens.append({
                'type': 'compound_assignment',
                'operator': operator,
                'variable': var_name,
                'value': value
            })
        else:
            tokens.append({'type': 'unknown', 'code': line})
    return tokens
