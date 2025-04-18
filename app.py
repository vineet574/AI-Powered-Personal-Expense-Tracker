from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from modules.nlp_processor import parse_expense
from modules.visualizer import generate_charts

app = Flask(__name__)

# Initialize database connection
DATABASE = 'database/expenses.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                (id INTEGER PRIMARY KEY, amount REAL, category TEXT, date TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM expenses')
    data = c.fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        expense_text = request.form['expense']
        parsed = parse_expense(expense_text)
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)', 
                  (parsed['amount'], parsed['category'], parsed['date']))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_expense.html')

@app.route('/summary')
def summary():
    chart_path = generate_charts()
    return render_template('summary.html', chart_path=chart_path)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
