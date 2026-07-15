# #!/usr/bin/env python3
# """
# Web-based Sales Dashboard with Flask
# """

# from flask import Flask, render_template, request, jsonify, redirect, url_for
# import sqlite3
# import json
# from datetime import datetime

# app = Flask(__name__)

# def init_db():
#     conn = sqlite3.connect('sales_dashboard.db')
#     cursor = conn.cursor()
    
#     cursor.execute('''CREATE TABLE IF NOT EXISTS stock (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         product_name TEXT NOT NULL,
#         quantity INTEGER NOT NULL,
#         purchase_price REAL NOT NULL,
#         selling_price REAL NOT NULL,
#         supplier TEXT,
#         date_added TEXT NOT NULL
#     )''')
    
#     cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         invoice_no TEXT NOT NULL,
#         customer_name TEXT,
#         items TEXT NOT NULL,
#         total_amount REAL NOT NULL,
#         payment_type TEXT NOT NULL,
#         sale_date TEXT NOT NULL
#     )''')
    
#     cursor.execute('''CREATE TABLE IF NOT EXISTS credits (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         type TEXT NOT NULL,
#         name TEXT NOT NULL,
#         amount REAL NOT NULL,
#         description TEXT,
#         date TEXT NOT NULL
#     )''')
    
#     cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         category TEXT NOT NULL,
#         amount REAL NOT NULL,
#         description TEXT,
#         date TEXT NOT NULL
#     )''')
    
#     conn.commit()
#     conn.close()

# @app.route('/')
# def dashboard():
#     return render_template('dashboard.html')

# @app.route('/stock')
# def stock():
#     conn = sqlite3.connect('sales_dashboard.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM stock ORDER BY id")
#     stocks = cursor.fetchall()
#     conn.close()
#     return render_template('stock.html', stocks=stocks)

# @app.route('/add_stock', methods=['POST'])
# def add_stock():
#     data = request.json
#     conn = sqlite3.connect('sales_dashboard.db')
#     cursor = conn.cursor()
    
#     cursor.execute('''INSERT INTO stock 
#                      (product_name, quantity, purchase_price, selling_price, supplier, date_added)
#                      VALUES (?, ?, ?, ?, ?, ?)''',
#                   (data['product_name'], data['quantity'], data['purchase_price'], 
#                    data['selling_price'], data['supplier'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
#     # Add supplier credit if specified
#     if data.get('add_to_credit') and data['supplier']:
#         total_cost = float(data['quantity']) * float(data['purchase_price'])
#         cursor.execute('''INSERT INTO credits (type, name, amount, description, date)
#                          VALUES (?, ?, ?, ?, ?)''',
#                       ("supplier", data['supplier'], total_cost, f"Stock purchase: {data['product_name']}", 
#                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
#     conn.commit()
#     conn.close()
#     return jsonify({'success': True})

# @app.route('/sales')
# def sales():
#     conn = sqlite3.connect('sales_dashboard.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM sales ORDER BY id DESC")
#     sales_data = cursor.fetchall()
#     conn.close()
#     return render_template('sales.html', sales=sales_data)

# @app.route('/create_invoice', methods=['POST'])
# def create_invoice():
#     data = request.json
#     invoice_no = f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
#     conn = sqlite3.connect('sales_dashboard.db')
#     cursor = conn.cursor()
    
#     total_amount = sum(item['total'] for item in data['items'])
    
#     cursor.execute('''INSERT INTO sales 
#                      (invoice_no, customer_name, items, total_amount, payment_type, sale_date)
#                      VALUES (?, ?, ?, ?, ?, ?)''',
#                   (invoice_no, data['customer_name'], json.dumps(data['items']), 
#                    total_amount, data['payment_type'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
#     # Update stock quantities
#     for item in data['items']:
#         cursor.execute("UPDATE stock SET quantity = quantity - ? WHERE product_name = ?", 
#                       (item['quantity'], item['product_name']))
    
#     # Add customer credit if payment is credit
#     if data['payment_type'] == 'credit':
#         cursor.execute('''INSERT INTO credits (type, name, amount, description, date)
#                          VALUES (?, ?, ?, ?, ?)''',
#                       ("customer", data['customer_name'], total_amount, f"Sale: {invoice_no}", 
#                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
#     conn.commit()
#     conn.close()
    
#     return jsonify({'success': True, 'invoice_no': invoice_no})

# @app.route('/analytics')
# def analytics():
#     conn = sqlite3.connect('sales_dashboard.db')
#     cursor = conn.cursor()
    
#     cursor.execute("SELECT SUM(total_amount) FROM sales")
#     total_revenue = cursor.fetchone()[0] or 0
    
#     cursor.execute("SELECT COUNT(*) FROM sales")
#     total_sales = cursor.fetchone()[0]
    
#     cursor.execute("SELECT SUM(quantity) FROM stock")
#     total_stock = cursor.fetchone()[0] or 0
    
#     cursor.execute("SELECT SUM(amount) FROM expenses")
#     total_expenses = cursor.fetchone()[0] or 0
    
#     conn.close()
    
#     analytics_data = {
#         'total_revenue': total_revenue,
#         'total_sales': total_sales,
#         'total_stock': total_stock,
#         'total_expenses': total_expenses
#     }
    
#     return render_template('analytics.html', data=analytics_data)

# @app.route('/credits')
# def credits():
#     conn = sqlite3.connect('sales_dashboard.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM credits ORDER BY date DESC")
#     credits_data = cursor.fetchall()
#     conn.close()
#     return render_template('credits.html', credits=credits_data)

# @app.route('/expenses')
# def expenses():
#     conn = sqlite3.connect('sales_dashboard.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
#     expenses_data = cursor.fetchall()
#     conn.close()
#     return render_template('expenses.html', expenses=expenses_data)

# @app.route('/add_expense', methods=['POST'])
# def add_expense():
#     data = request.json
#     conn = sqlite3.connect('sales_dashboard.db')
#     cursor = conn.cursor()
    
#     cursor.execute('''INSERT INTO expenses (category, amount, description, date)
#                      VALUES (?, ?, ?, ?)''',
#                   (data['category'], data['amount'], data['description'], 
#                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
#     conn.commit()
#     conn.close()
#     return jsonify({'success': True})

# @app.route('/ai_chat', methods=['POST'])
# def ai_chat():
#     query = request.json['query'].lower()
    
#     conn = sqlite3.connect('sales_dashboard.db')
#     cursor = conn.cursor()
    
#     if "stock" in query or "inventory" in query:
#         if "low" in query:
#             cursor.execute("SELECT product_name, quantity FROM stock WHERE quantity < 10")
#             low_stock = cursor.fetchall()
#             if low_stock:
#                 response = "Low stock items: " + ", ".join([f"{item[0]} ({item[1]} left)" for item in low_stock])
#             else:
#                 response = "All items are well stocked!"
#         else:
#             cursor.execute("SELECT COUNT(*), SUM(quantity) FROM stock")
#             result = cursor.fetchone()
#             response = f"You have {result[0]} products with {result[1]} total items in stock."
#     elif "price" in query:
#         words = query.split()
#         product_found = False
#         for word in words:
#             cursor.execute("SELECT product_name, selling_price FROM stock WHERE LOWER(product_name) LIKE ?", (f"%{word}%",))
#             result = cursor.fetchone()
#             if result:
#                 response = f"{result[0]} costs ${result[1]}"
#                 product_found = True
#                 break
#         if not product_found:
#             response = "Product not found. Please specify the product name."
#     elif "sales" in query or "revenue" in query:
#         if "today" in query:
#             cursor.execute("SELECT COUNT(*), SUM(total_amount) FROM sales WHERE DATE(sale_date) = DATE('now')")
#             result = cursor.fetchone()
#             response = f"Today's sales: {result[0]} transactions, Revenue: ${result[1] or 0}"
#         else:
#             cursor.execute("SELECT COUNT(*), SUM(total_amount) FROM sales")
#             result = cursor.fetchone()
#             response = f"Total sales: {result[0]} transactions, Revenue: ${result[1] or 0}"
#     elif "credit" in query:
#         cursor.execute("SELECT SUM(amount) FROM credits WHERE type = 'customer'")
#         customer_credit = cursor.fetchone()[0] or 0
#         cursor.execute("SELECT SUM(amount) FROM credits WHERE type = 'supplier'")
#         supplier_credit = cursor.fetchone()[0] or 0
#         response = f"Customer credits: ${customer_credit}, Supplier credits: ${supplier_credit}"
#     elif "profit" in query:
#         cursor.execute("SELECT SUM(total_amount) FROM sales")
#         revenue = cursor.fetchone()[0] or 0
#         cursor.execute("SELECT SUM(amount) FROM expenses")
#         expenses = cursor.fetchone()[0] or 0
#         profit = revenue - expenses
#         response = f"Revenue: ${revenue}, Expenses: ${expenses}, Net Profit: ${profit}"
#     else:
#         response = "I can help with stock, prices, sales, credits, and profit analysis. Try asking about specific products or business metrics."
    
#     conn.close()
#     return jsonify({'response': response})

# @app.route('/print_invoice/<invoice_no>')
# def print_invoice(invoice_no):
#     conn = sqlite3.connect('sales_dashboard.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM sales WHERE invoice_no = ?", (invoice_no,))
#     sale = cursor.fetchone()
#     conn.close()
    
#     if sale:
#         items = json.loads(sale[3])
#         return render_template('print_invoice.html', sale=sale, items=items)
#     return "Invoice not found", 404

# @app.route('/ledger')
# def ledger():
#     conn = sqlite3.connect('sales_dashboard.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM credits ORDER BY date DESC")
#     credits_data = cursor.fetchall()
#     conn.close()
#     return render_template('ledger.html', credits=credits_data)

# if __name__ == '__main__':
#     init_db()
#     app.run(debug=True, host='0.0.0.0', port=5000)



#!/usr/bin/env python3
"""
Web-based Sales Dashboard with Flask
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import json
from datetime import datetime
import webbrowser
import threading

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        purchase_price REAL NOT NULL,
        selling_price REAL NOT NULL,
        supplier TEXT,
        date_added TEXT NOT NULL
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_no TEXT NOT NULL,
        customer_name TEXT,
        customer_phone TEXT,
        items TEXT NOT NULL,
        total_amount REAL NOT NULL,
        payment_type TEXT NOT NULL,
        sale_date TEXT NOT NULL
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS credits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        name TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        date TEXT NOT NULL
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        date TEXT NOT NULL
    )''')
    
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/stock')
def stock():
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stock ORDER BY id")
    stocks = cursor.fetchall()
    conn.close()
    return render_template('stock.html', stocks=stocks)

@app.route('/add_stock', methods=['POST'])
def add_stock():
    data = request.json
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO stock 
                     (product_name, quantity, purchase_price, selling_price, supplier, date_added)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (data['product_name'], data['quantity'], data['purchase_price'], 
                   data['selling_price'], data['supplier'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    if data.get('add_to_credit') and data['supplier']:
        total_cost = float(data['quantity']) * float(data['purchase_price'])
        cursor.execute('''INSERT INTO credits (type, name, amount, description, date)
                         VALUES (?, ?, ?, ?, ?)''',
                      ("supplier", data['supplier'], total_cost, f"Stock purchase: {data['product_name']}", 
                       datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/sales')
def sales():
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales ORDER BY id DESC")
    sales_data = cursor.fetchall()
    conn.close()
    return render_template('sales.html', sales=sales_data)

def send_whatsapp_invoice(phone, invoice_no, customer_name, items, total_amount):
    try:
        message = f"INVOICE: {invoice_no}\\nCustomer: {customer_name}\\n"
        for item in items:
            message += f"{item['product_name']} x{item['quantity']} = ${item['total']}\\n"
        message += f"Total: ${total_amount}"
        
        url = "https://wa.me/{phone.replace('+', '')}?text={message.replace(' ', '%20').replace('\\n', '%0A')}"
        webbrowser.open(url)
    except Exception as e:
        print(f"WhatsApp error: {e}")

@app.route('/create_invoice', methods=['POST'])
def create_invoice():
    data = request.json
    invoice_no = f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    
    total_amount = sum(item['total'] for item in data['items'])
    
    cursor.execute('''INSERT INTO sales 
                     (invoice_no, customer_name, customer_phone, items, total_amount, payment_type, sale_date)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (invoice_no, data['customer_name'], data.get('customer_phone'), json.dumps(data['items']), 
                   total_amount, data['payment_type'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    for item in data['items']:
        cursor.execute("UPDATE stock SET quantity = quantity - ? WHERE product_name = ?", 
                      (item['quantity'], item['product_name']))
    
    if data['payment_type'] == 'credit':
        cursor.execute('''INSERT INTO credits (type, name, amount, description, date)
                         VALUES (?, ?, ?, ?, ?)''',
                      ("customer", data['customer_name'], total_amount, f"Sale: {invoice_no}", 
                       datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    conn.commit()
    conn.close()
    
    if data.get('customer_phone') and data.get('send_whatsapp'):
        threading.Thread(target=send_whatsapp_invoice, 
                        args=(data['customer_phone'], invoice_no, data['customer_name'], 
                             data['items'], total_amount), daemon=True).start()
    
    return jsonify({'success': True, 'invoice_no': invoice_no})

@app.route('/analytics')
def analytics():
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(total_amount) FROM sales")
    total_revenue = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM sales")
    total_sales = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(quantity) FROM stock")
    total_stock = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = cursor.fetchone()[0] or 0
    
    conn.close()
    
    analytics_data = {
        'total_revenue': total_revenue,
        'total_sales': total_sales,
        'total_stock': total_stock,
        'total_expenses': total_expenses
    }
    
    return render_template('analytics.html', data=analytics_data)

@app.route('/ledger')
def ledger():
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credits ORDER BY date DESC")
    credits_data = cursor.fetchall()
    conn.close()
    return render_template('ledger.html', credits=credits_data)

@app.route('/expenses')
def expenses():
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses_data = cursor.fetchall()
    conn.close()
    return render_template('expenses.html', expenses=expenses_data)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO expenses (category, amount, description, date)
                     VALUES (?, ?, ?, ?)''',
                  (data['category'], data['amount'], data['description'], 
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/ai_chat', methods=['POST'])
def ai_chat():
    query = request.json['query'].lower()
    
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    
    if "stock" in query:
        cursor.execute("SELECT COUNT(*), SUM(quantity) FROM stock")
        result = cursor.fetchone()
        response = f"You have {result[0]} products with {result[1]} total items in stock."
    elif "sales" in query or "revenue" in query:
        cursor.execute("SELECT COUNT(*), SUM(total_amount) FROM sales")
        result = cursor.fetchone()
        response = f"Total sales: {result[0]} transactions, Revenue: ${result[1] or 0}"
    elif "credit" in query:
        cursor.execute("SELECT SUM(amount) FROM credits WHERE type = 'customer'")
        customer_credit = cursor.fetchone()[0] or 0
        response = f"Customer credits: ${customer_credit}"
    else:
        response = "I can help with stock, sales, and credits. Try asking about inventory or revenue."
    
    conn.close()
    return jsonify({'response': response})

@app.route('/print_invoice/<invoice_no>')
def print_invoice(invoice_no):
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales WHERE invoice_no = ?", (invoice_no,))
    sale = cursor.fetchone()
    conn.close()
    
    if sale:
        items = json.loads(sale[4])
        return render_template('print_invoice.html', sale=sale, items=items)
    return "Invoice not found", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)