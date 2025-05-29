# -----------------------
# STAGE 3: Intermediate Representation (IR)
# -----------------------
import re
def generate_ir(ast):
    ir = []
    for node in ast:
        if node['type'] == 'VariableDeclaration':
            ir.append({
                'op': 'assign',
                'target': node['identifier'],
                'value': node['value']
            })
        elif node['type'] == 'ConsoleLog':
            ir.append({
                'op': 'print',
                'value': node['value']
            })
        elif node['type'] == 'FunctionDeclaration':
            body_ir = generate_ir(node['body'])
            ir.append({
                'op': 'function_def',
                'name': node['name'],
                'params': node['params'],
                'body': body_ir
            })
        elif node['type'] == 'IfStatementChain':
            branches = [{'type': 'if', 'condition': node['if']['condition'], 'body': generate_ir(node['if']['body'])}]
            for elif_block in node.get('elif', []):
                branches.append({'type': 'elif', 'condition': elif_block['condition'], 'body': generate_ir(elif_block['body'])})
            if node.get('else'):
                branches.append({'type': 'else', 'body': generate_ir(node['else'])})
            ir.append({'op': 'if_chain', 'branches': branches})
        elif node['type'] == 'WhileLoop':
            ir.append({
                'op': 'while',
                'condition': node['condition'],
                'body': generate_ir(node['body'])
            })
        elif node['type'] == 'DoWhileLoop':
            ir.append({
                'op': 'do_while',
                'condition': node['condition'],
                'body': generate_ir(node['body'])
            })
        elif node['type'] == 'ForLoop':
            ir.append({
                'op': 'for_loop',
                'init': node['init'],
                'condition': node['condition'],
                'increment': node['increment'],
                'body': generate_ir(node['body'])
            })
        elif node['type'] == 'ReturnStatement':
            ir.append({
                'op': 'return',
                'value': node['value']
            })
        elif node['type'] == 'UpdateExpression':
            ir.append({
                'op': 'update',
                'operator': node['operator'],  # '++' or '--'
                'target': node['argument'],
                'prefix': node.get('prefix', False)  # optional
            })

    return ir
