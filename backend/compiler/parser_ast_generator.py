# -----------------------
# STAGE 2: Parser
# -----------------------
import re

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def _parse_block(self, code):
        stmts = [line.strip() for line in code.split(';') if line.strip()]
        block_ast = []
        for line in stmts:
            return_match = re.match(r'^return\s+(.+)$', line)
            decl_match = re.match(r'^(let|const|var)\s+(\w+)\s*=\s*(.+)$', line)
            log_match = re.match(r'^console\.log\((.*)\)$', line)
            inc_dec_match = re.match(r'^(\w+)\s*(\+\+|--)$', line)
            comp_assign_match = re.match(r'^(\w+)\s*([\+\-])=\s*(\d+)$', line)

            if return_match:
                block_ast.append({'type': 'ReturnStatement', 'value': return_match.group(1).strip()})
            elif decl_match:
                block_ast.append({
                    'type': 'VariableDeclaration',
                    'kind': decl_match.group(1),
                    'identifier': decl_match.group(2),
                    'value': decl_match.group(3).strip()
                })
            elif log_match:
                block_ast.append({'type': 'ConsoleLog', 'value': log_match.group(1).strip()})
            elif inc_dec_match:
                var, op = inc_dec_match.groups()
                block_ast.append({
                    'type': 'UpdateExpression',
                    'operator': op,
                    'argument': var
                })
            elif comp_assign_match:
                var, op, val = comp_assign_match.groups()
                block_ast.append({
                    'type': 'CompoundAssignment',
                    'operator': op,
                    'variable': var,
                    'value': val
                })
            else:
                block_ast.append({'type': 'Unknown', 'code': line})
        return block_ast

    def parse(self):
        ast = []
        for token in self.tokens:
            if token['type'] == 'declaration':
                ast.append({
                    'type': 'VariableDeclaration',
                    'kind': token['kind'],
                    'identifier': token['name'],
                    'value': token['value']
                })
            elif token['type'] == 'console_log':
                ast.append({
                    'type': 'ConsoleLog',
                    'value': token['value']
                })
            elif token['type'] in ['function_declaration', 'arrow_function']:
                body_str = token['body'].strip()
                if body_str == '':
                    body_lines = []
                else:
                    body_lines = [line.strip() for line in body_str.split(';') if line.strip()]
                body_ast = []
                for line in body_lines:
                    return_match = re.match(r'^return\s+(.+)$', line)
                    decl_match = re.match(r'^(let|const|var)\s+(\w+)\s*=\s*(.+)$', line)
                    log_match = re.match(r'^console\.log\((.*)\)$', line)
                    inc_dec_match = re.match(r'^(\w+)\s*(\+\+|--)$', line)
                    comp_assign_match = re.match(r'^(\w+)\s*([\+\-])=\s*(\d+)$', line)

                    if return_match:
                        body_ast.append({'type': 'ReturnStatement', 'value': return_match.group(1).strip()})
                    elif decl_match:
                        body_ast.append({
                            'type': 'VariableDeclaration',
                            'kind': decl_match.group(1),
                            'identifier': decl_match.group(2),
                            'value': decl_match.group(3).strip()
                        })
                    elif log_match:
                        body_ast.append({
                            'type': 'ConsoleLog',
                            'value': log_match.group(1).strip()
                        })
                    elif inc_dec_match:
                        var, op = inc_dec_match.groups()
                        body_ast.append({
                            'type': 'UpdateExpression',
                            'operator': op,
                            'argument': var
                        })
                    elif comp_assign_match:
                        var, op, val = comp_assign_match.groups()
                        body_ast.append({
                            'type': 'CompoundAssignment',
                            'operator': op,
                            'variable': var,
                            'value': val
                        })
                    else:
                        body_ast.append({'type': 'Unknown', 'code': line})
                ast.append({
                    'type': 'FunctionDeclaration',
                    'name': token['name'],
                    'params': token['params'],
                    'body': body_ast
                })
            elif token['type'] == 'if_statement_chain':
                def parse_block(code):
                    stmts = [line.strip() for line in code.split(';') if line.strip()]
                    block_ast = []
                    for line in stmts:
                        return_match = re.match(r'^return\s+(.+)$', line)
                        decl_match = re.match(r'^(let|const|var)\s+(\w+)\s*=\s*(.+)$', line)
                        log_match = re.match(r'^console\.log\((.*)\)$', line)
                        inc_dec_match = re.match(r'^(\w+)\s*(\+\+|--)$', line)
                        comp_assign_match = re.match(r'^(\w+)\s*([\+\-])=\s*(\d+)$', line)

                        if return_match:
                            block_ast.append({'type': 'ReturnStatement', 'value': return_match.group(1).strip()})
                        elif decl_match:
                            block_ast.append({
                                'type': 'VariableDeclaration',
                                'kind': decl_match.group(1),
                                'identifier': decl_match.group(2),
                                'value': decl_match.group(3).strip()
                            })
                        elif log_match:
                            block_ast.append({'type': 'ConsoleLog', 'value': log_match.group(1).strip()})
                        elif inc_dec_match:
                            var, op = inc_dec_match.groups()
                            block_ast.append({
                                'type': 'UpdateExpression',
                                'operator': op,
                                'argument': var
                            })
                        elif comp_assign_match:
                            var, op, val = comp_assign_match.groups()
                            block_ast.append({
                                'type': 'CompoundAssignment',
                                'operator': op,
                                'variable': var,
                                'value': val
                            })
                        else:
                            block_ast.append({'type': 'Unknown', 'code': line})
                    return block_ast

                if_body = parse_block(token['if']['body'])
                elif_blocks = [{'condition': e['condition'], 'body': parse_block(e['body'])}
                            for e in token.get('elif', [])]
                else_body = parse_block(token['else']) if token.get('else') else None

                ast.append({
                    'type': 'IfStatementChain',
                    'if': {'condition': token['if']['condition'], 'body': if_body},
                    'elif': elif_blocks,
                    'else': else_body
                })
            elif token['type'] == 'while_loop':
                body = self._parse_block(token['body'])
                ast.append({
                    'type': 'WhileLoop',
                    'condition': token['condition'],
                    'body': body
                })
            elif token['type'] == 'do_while_loop':
                body = self._parse_block(token['body'])
                ast.append({
                    'type': 'DoWhileLoop',
                    'condition': token['condition'],
                    'body': body
                })
            elif token['type'] == 'for_loop':
                body = self._parse_block(token['body'])
                ast.append({
                    'type': 'ForLoop',
                    'init': token['init'],
                    'condition': token['condition'],
                    'increment': token['increment'],
                    'body': body
                })
            elif token['type'] == 'inc_dec_operation':
                ast.append({
                    'type': 'UpdateExpression',
                    'operator': token['operator'],
                    'argument': token['variable']
                })
            elif token['type'] == 'compound_assignment':
                ast.append({
                    'type': 'CompoundAssignment',
                    'operator': token['operator'],
                    'variable': token['variable'],
                    'value': token['value']
                })

        return ast
