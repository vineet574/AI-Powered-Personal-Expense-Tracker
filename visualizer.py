import matplotlib.pyplot as plt
import sqlite3

DATABASE = 'database/expenses.db'

def generate_charts():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    data = c.fetchall()
    conn.close()

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Summary')
    chart_path = 'static/expense_chart.png'
    plt.savefig(chart_path)
    plt.close()
    return chart_path
