
# JavaScript to Python Compiler

This project provides a compiler that translates JavaScript code into Python. It is designed to facilitate migration of JavaScript-based applications or scripts into Python while preserving functionality.

# 🚀Features
- Parses JavaScript syntax and converts it into equivalent Python code
- Supports variable declaration, functions, loops, and conditionals
- Handles common JavaScript built-in methods and transforms them into Python equivalents
- Offers command-line usage for easy integration into workflows

# 🛠️ Tech Stack

   **Frontend**
   - HTML5, CSS
   - JavaScript
   **Backend**
   - Python(Flask)
   **Other Tools**
   - Tokenization and Parsing Libraries (custom implementation)

# 📂 Project Structure
```bash
   JsToPythonCompiler/
├── static/               # Frontend static files (CSS, JS)
├── templates/            # HTML templates for the UI
├── app.py                # Main Flask application
├── converter/            # Core compiler logic
│   ├── tokenizer.py      # Tokenization logic
│   ├── parser.py         # Parsing and syntax tree processing
│   ├── translator.py     # Core translation logic
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
   ```

# Setup Instructions
To run this project locally, please follow these steps:

**1. Clone the repository:**

   ```bash
   git clone https://github.com/example/js-to-python-compiler.git
cd js-to-python-compiler
   ```

**2. Setup the backend:**


   ```bash
   cd backend

   ```
   * **Set up the Virtual Environment:**
      
```bash
   
   python -m venv venv
   source venv/bin/activate
   venv\Scripts\activate  

```
* **Ensure you have Python installed, then install dependencies:**
```bash
   
   pip install -r requirements.txt


```
**3. Run the application**
```bash
   python app.py 
```
* This will start the development server for the frontend, usually at http://localhost:5000

# 🖥️ Demo
**Example Input(JavaScript):**
```bash
function add(a, b) {
    return a + b;
}
```

**Example Output (Python):**
```bash
def add(a, b):
    return a + b
```