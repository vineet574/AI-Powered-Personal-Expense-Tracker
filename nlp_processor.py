import re
from datetime import datetime

def parse_expense(text):
    amount = float(re.search(r'\d+', text).group())
    category = 'Other'
    if 'groceries' in text:
        category = 'Groceries'
    elif 'rent' in text:
        category = 'Rent'
    elif 'food' in text:
        category = 'Food'
    date = datetime.now().strftime('%Y-%m-%d')
    return {'amount': amount, 'category': category, 'date': date}
