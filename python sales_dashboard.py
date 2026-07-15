# #!/usr/bin/env python3
"""
Web-based Sales Dashboard with Flask
"""


from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import json
from datetime import datetime

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
        supplier_email TEXT,
        date_added TEXT NOT NULL
    )''')
    
    # Add supplier_email column if it doesn't exist
    try:
        cursor.execute('ALTER TABLE stock ADD COLUMN supplier_email TEXT')
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_no TEXT NOT NULL,
        customer_name TEXT,
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
    
    dashboard_data = {
        'total_revenue': total_revenue,
        'total_sales': total_sales,
        'total_stock': total_stock,
        'total_expenses': total_expenses
    }
    
    return render_template('dashboard.html', data=dashboard_data)

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
                     (product_name, quantity, purchase_price, selling_price, supplier, supplier_email, date_added)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (data['product_name'], data['quantity'], data['purchase_price'], 
                   data['selling_price'], data['supplier'], data.get('supplier_email', ''), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    # Add supplier credit if specified
    if data.get('add_to_credit') and data['supplier']:
        total_cost = float(data['quantity']) * float(data['purchase_price'])
        cursor.execute('''INSERT INTO credits (type, name, amount, description, date)
                         VALUES (?, ?, ?, ?, ?)''',
                      ("supplier", data['supplier'], total_cost, f"Stock purchase: {data['product_name']}", 
                       datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/get_product_price/<product_name>')
def get_product_price(product_name):
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT selling_price FROM stock WHERE product_name = ?", (product_name,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return jsonify({'price': result[0]})
    return jsonify({'price': 0})

@app.route('/sales')
def sales():
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales ORDER BY id DESC")
    sales_data = cursor.fetchall()
    conn.close()
    return render_template('sales.html', sales=sales_data)

@app.route('/create_invoice', methods=['POST'])
def create_invoice():
    data = request.json
    invoice_no = f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    
    total_amount = sum(item['total'] for item in data['items'])
    
    cursor.execute('''INSERT INTO sales 
                     (invoice_no, customer_name, items, total_amount, payment_type, sale_date)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (invoice_no, data['customer_name'], json.dumps(data['items']), 
                   total_amount, data['payment_type'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    # Update stock quantities
    for item in data['items']:
        cursor.execute("UPDATE stock SET quantity = quantity - ? WHERE product_name = ?", 
                      (item['quantity'], item['product_name']))
    
    # Add customer credit if payment is credit
    if data['payment_type'] == 'credit':
        cursor.execute('''INSERT INTO credits (type, name, amount, description, date)
                         VALUES (?, ?, ?, ?, ?)''',
                      ("customer", data['customer_name'], total_amount, f"Sale: {invoice_no}", 
                       datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    conn.commit()
    conn.close()
    
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

@app.route('/credits')
def credits():
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credits ORDER BY date DESC")
    credits_data = cursor.fetchall()
    conn.close()
    return render_template('credits.html', credits=credits_data)

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

@app.route('/print_invoice/<invoice_no>')
def print_invoice(invoice_no):
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales WHERE invoice_no = ?", (invoice_no,))
    sale = cursor.fetchone()
    conn.close()
    
    if sale:
        items = json.loads(sale[3])
        return render_template('print_invoice.html', sale=sale, items=items)
    return "Invoice not found", 404

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    report_type = data.get('report_type')
    period = data.get('period', 'monthly')
    
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    
    if period == 'monthly':
        date_filter = "strftime('%Y-%m', sale_date) = strftime('%Y-%m', 'now')"
    elif period == 'yearly':
        date_filter = "strftime('%Y', sale_date) = strftime('%Y', 'now')"
    else:
        date_filter = "DATE(sale_date) = DATE('now')"
    
    if report_type == 'sales':
        cursor.execute(f"SELECT * FROM sales WHERE {date_filter} ORDER BY sale_date DESC")
        report_data = cursor.fetchall()
    elif report_type == 'stock':
        cursor.execute("SELECT * FROM stock ORDER BY product_name")
        report_data = cursor.fetchall()
    elif report_type == 'expenses':
        cursor.execute(f"SELECT * FROM expenses WHERE {date_filter} ORDER BY date DESC")
        report_data = cursor.fetchall()
    else:
        report_data = []
    
    conn.close()
    return jsonify({'data': report_data, 'type': report_type, 'period': period})

@app.route('/ledger')
def ledger():
    conn = sqlite3.connect('sales_dashboard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credits ORDER BY date DESC")
    credits_data = cursor.fetchall()
    conn.close()
    return render_template('ledger.html', credits=credits_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)