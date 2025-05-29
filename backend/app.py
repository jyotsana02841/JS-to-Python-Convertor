from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from compiler.tokenizer import lexer
from compiler.parser_ast_generator import Parser
from compiler.ir_generator import generate_ir
from compiler.python_converter import generate_python

# -----------------------
# FLASK ROUTE
# -----------------------
@app.route('/convert', methods=['POST'])
def convert_code():
    data = request.get_json()
    js_code = data.get('code', '')
    if not js_code:
        return jsonify({'message': 'No code provided'}), 400
    try:
        tokens = lexer(js_code)
        ast = Parser(tokens).parse()
        ir = generate_ir(ast)
        py = generate_python(ir)
        return jsonify({
            'tokens': tokens,
            'ast': ast,
            'ir': ir,
            'python': py
        })
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
