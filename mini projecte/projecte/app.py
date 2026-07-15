# from flask import Flask, request, jsonify, render_template, redirect, url_for

# app = Flask(__name__)

# # Hard-coded user for login
# USER = {
#     "username": "admin",
#     "password": "1234"
# }

# # Sample data for home page (for testing)
# HOME_DATA = {
#     "stocks": [
#         {"item": "Tea", "quantity": 50, "price": 10},
#         {"item": "Coffee", "quantity": 30, "price": 15}
#     ],
#     "credit": [
#         {"customer": "Ali", "amount": 100},
#         {"customer": "Ahmed", "amount": 200}
#     ],
#     "mycredit": [
#         {"supplier": "Tea Supplier", "amount": 150}
#     ],
#     "profit": 500,
#     "monthly_profit": {   # 👈 New section
#         "January": 200,
#         "February": 350,
#         "March": 500,
#         "April": 250,
#         "May": 400,
#         "June": 600,
#         "July": 450,
#         "August": 300,
#         "September": 550,
#         "October": 700,
#         "November": 650,
#         "December": 800
#     }
# }

# @app.route('/')
# def index():
#     return render_template('login.html')

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.form
#     username = data.get('username')
#     password = data.get('password')

#     if username == USER["username"] and password == USER["password"]:
#         return redirect(url_for('home'))
#     else:
#         return render_template('login.html', error="Invalid username or password!")

# @app.route('/home')
# def home():
#     return render_template('home.html', data=HOME_DATA)

# @app.route('/api/home_data')
# def home_data():
#     # API endpoint to send home page data as JSON
#     return jsonify(HOME_DATA)

# if __name__ == "__main__":
#     app.run(debug=True)



# from flask import Flask, request, jsonify, render_template, redirect, url_for
# import pandas as pd
# import os
# from datetime import datetime

# app = Flask(__name__, template_folder="templates")

# # =======================
# # File Paths
# # =======================
# STOCK_FILE = "stocks.xlsx"
# ORDER_FILE = "orders.xlsx"
# PROFIT_FILE = "profit.xlsx"

# # =======================
# # Initial Setup
# # =======================
# def initialize_files():
#     """Excel files agar na hon to create kar do."""
#     if not os.path.exists(STOCK_FILE):
#         stocks_df = pd.DataFrame([
#             {"item": "Tea", "quantity": 50, "price": 10},
#             {"item": "Coffee", "quantity": 30, "price": 15}
#         ])
#         stocks_df.to_excel(STOCK_FILE, index=False)

#     if not os.path.exists(ORDER_FILE):
#         pd.DataFrame(columns=["customer", "item", "quantity", "amount"]).to_excel(ORDER_FILE, index=False)

#     if not os.path.exists(PROFIT_FILE):
#         pd.DataFrame(columns=["month", "profit"]).to_excel(PROFIT_FILE, index=False)


# initialize_files()

# # =======================
# # Dummy Login
# # =======================
# USER = {"username": "admin", "password": "1234"}

# @app.route('/')
# def index():
#     return render_template('login.html')


# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form.get('username')
#     password = request.form.get('password')

#     if username == USER["username"] and password == USER["password"]:
#         return redirect(url_for('home'))
#     else:
#         return render_template('login.html', error="Invalid username or password!")


# @app.route('/home')
# def home():
#     try:
#         stocks_df = pd.read_excel(STOCK_FILE)
#         profit_df = pd.read_excel(PROFIT_FILE)
#         total_profit = profit_df["profit"].sum() if not profit_df.empty else 0

#         return render_template(
#             'home.html',
#             stocks=stocks_df.to_dict(orient="records"),
#             profit=total_profit
#         )
#     except Exception as e:
#         return f"Error: {e}"


# # =======================
# # API: Place Order
# # =======================
# @app.route('/order', methods=['POST'])
# def place_order():
#     try:
#         customer = request.form.get("customer")
#         item = request.form.get("item")
#         qty = int(request.form.get("quantity"))

#         if not customer or not item or qty <= 0:
#             return jsonify({"error": "Invalid order data!"}), 400

#         # Load data
#         stocks_df = pd.read_excel(STOCK_FILE)

#         if item not in stocks_df["item"].values:
#             return jsonify({"error": f"Item '{item}' not found in stock!"}), 400

#         row = stocks_df.loc[stocks_df["item"] == item].iloc[0]
#         if qty > row["quantity"]:
#             return jsonify({"error": "Not enough stock!"}), 400

#         # Calculate bill
#         amount = qty * row["price"]

#         # Update stock
#         stocks_df.loc[stocks_df["item"] == item, "quantity"] -= qty
#         stocks_df.to_excel(STOCK_FILE, index=False)

#         # Save order
#         order_df = pd.read_excel(ORDER_FILE)
#         new_order = pd.DataFrame([{
#             "customer": customer,
#             "item": item,
#             "quantity": qty,
#             "amount": amount
#         }])
#         order_df = pd.concat([order_df, new_order], ignore_index=True)
#         order_df.to_excel(ORDER_FILE, index=False)

#         # Save profit
#         profit_margin = 0.3  # 30%
#         month = datetime.now().strftime("%B")
#         profit_df = pd.read_excel(PROFIT_FILE)
#         new_profit = pd.DataFrame([{"month": month, "profit": amount * profit_margin}])
#         profit_df = pd.concat([profit_df, new_profit], ignore_index=True)
#         profit_df.to_excel(PROFIT_FILE, index=False)

#         return jsonify({
#             "message": "Order placed successfully!",
#             "bill": {
#                 "customer": customer,
#                 "item": item,
#                 "quantity": qty,
#                 "amount": amount
#             }
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(debug=True)
















# from flask import Flask, request, jsonify, send_file
# import sqlite3
# import json
# from datetime import datetime, date
# from fpdf import FPDF
# import os
# import threading
# import shutil

# app = Flask(__name__)
# DB = "shop.db"

# # ====================== Database Init ======================
# def init_db():
#     conn = sqlite3.connect(DB)
#     cursor = conn.cursor()
    
#     # Stock Table
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS stock(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         item_name TEXT NOT NULL,
#         quantity INTEGER NOT NULL,
#         price REAL NOT NULL,
#         date_added DATE DEFAULT (DATE('now'))
#     )
#     ''')
    
#     # Sale Table
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS sale(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         date DATE DEFAULT (DATE('now')),
#         items TEXT NOT NULL,
#         total_amount REAL NOT NULL,
#         customer_credit REAL DEFAULT 0
#     )
#     ''')
    
#     # Ledger Table
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS ledger(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         type TEXT NOT NULL,
#         amount REAL NOT NULL,
#         date DATE DEFAULT (DATE('now'))
#     )
#     ''')
    
#     # Expense Table
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS expense(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         description TEXT NOT NULL,
#         amount REAL NOT NULL,
#         date DATE DEFAULT (DATE('now'))
#     )
#     ''')
    
#     conn.commit()
#     conn.close()

# init_db()

# # ====================== Stock API ======================
# @app.route("/add_stock", methods=["POST"])
# def add_stock():
#     data = request.json
#     item_name = data.get("item_name")
#     quantity = data.get("quantity")
#     price = data.get("price")
    
#     conn = sqlite3.connect(DB)
#     cursor = conn.cursor()
#     today = date.today()
#     cursor.execute("INSERT INTO stock(item_name, quantity, price, date_added) VALUES (?,?,?,?)", 
#                    (item_name, quantity, price, today))
    
#     # Supplier credit in ledger
#     cursor.execute("INSERT INTO ledger(type, amount, date) VALUES (?,?,?)", 
#                    ("supplier", quantity*price, today))
    
#     conn.commit()
#     conn.close()
#     return jsonify({"status":"success", "message":"Stock added successfully!"})

# @app.route("/list_stock", methods=["GET"])
# def list_stock():
#     conn = sqlite3.connect(DB)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM stock ORDER BY id ASC")
#     rows = cursor.fetchall()
#     conn.close()
    
#     stock_list = [{"id":idx+1, "item_name":r[1], "quantity":r[2], "price":r[3], "date_added":r[4]} 
#                   for idx, r in enumerate(rows)]
#     return jsonify(stock_list)

# # ====================== Sale API ======================
# @app.route("/add_sale", methods=["POST"])
# def add_sale():
#     data = request.json
#     items = data.get("items")  # [{"item_id":1,"quantity":2},...]
#     customer_credit = data.get("customer_credit", 0)
    
#     total_amount = 0
#     conn = sqlite3.connect(DB)
#     cursor = conn.cursor()
    
#     for item in items:
#         cursor.execute("SELECT quantity, price FROM stock WHERE id=?", (item["item_id"],))
#         stock_item = cursor.fetchone()
#         if not stock_item:
#             return jsonify({"status":"error", "message":f"Item ID {item['item_id']} not found"})
#         if stock_item[0] < item["quantity"]:
#             return jsonify({"status":"error", "message":f"Not enough stock for item ID {item['item_id']}"})
#         total_amount += stock_item[1] * item["quantity"]
#         cursor.execute("UPDATE stock SET quantity=? WHERE id=?", (stock_item[0]-item["quantity"], item["item_id"]))
    
#     today = date.today()
#     cursor.execute("INSERT INTO sale(items, total_amount, customer_credit) VALUES (?,?,?)",
#                    (json.dumps(items), total_amount, customer_credit))
    
#     if customer_credit > 0:
#         cursor.execute("INSERT INTO ledger(type, amount, date) VALUES (?,?,?)", ("customer", customer_credit, today))
    
#     conn.commit()
#     conn.close()
    
#     # Generate PDF Invoice
#     invoice_path = generate_invoice(items, total_amount)
    
#     return jsonify({"status":"success", "message":"Sale added successfully!", "total_amount": total_amount, "invoice": invoice_path})

# # ====================== Expense API ======================
# @app.route("/add_expense", methods=["POST"])
# def add_expense():
#     data = request.json
#     description = data.get("description")
#     amount = data.get("amount")
#     today = date.today()
    
#     conn = sqlite3.connect(DB)
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO expense(description, amount, date) VALUES (?,?,?)", (description, amount, today))
#     cursor.execute("INSERT INTO ledger(type, amount, date) VALUES (?,?,?)", ("expense", amount, today))
#     conn.commit()
#     conn.close()
    
#     return jsonify({"status":"success", "message":"Expense added successfully!"})

# # ====================== Ledger API ======================
# @app.route("/ledger", methods=["GET"])
# def view_ledger():
#     conn = sqlite3.connect(DB)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM ledger ORDER BY id ASC")
#     rows = cursor.fetchall()
#     conn.close()
    
#     ledger_list = [{"id":r[0], "type":r[1], "amount":r[2], "date":r[3]} for r in rows]
#     return jsonify(ledger_list)

# # ====================== Sale Analytics ======================
# @app.route("/sale_analytics", methods=["GET"])
# def sale_analytics():
#     conn = sqlite3.connect(DB)
#     cursor = conn.cursor()
    
#     # Total sales
#     cursor.execute("SELECT SUM(total_amount) FROM sale")
#     total_sales = cursor.fetchone()[0] or 0
    
#     # Sales today
#     today = date.today()
#     cursor.execute("SELECT SUM(total_amount) FROM sale WHERE date=?", (today,))
#     sales_today = cursor.fetchone()[0] or 0
    
#     # Items sold
#     cursor.execute("SELECT items FROM sale")
#     items_sold = {}
#     for row in cursor.fetchall():
#         items = json.loads(row[0])
#         for it in items:
#             items_sold[it["item_id"]] = items_sold.get(it["item_id"], 0) + it["quantity"]
    
#     conn.close()
#     return jsonify({"total_sales": total_sales, "sales_today": sales_today, "items_sold": items_sold})

# # ====================== PDF Invoice ======================
# def generate_invoice(items, total_amount):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt=f"Invoice - {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
#     pdf.ln(5)
    
#     for item in items:
#         pdf.cell(200, 10, txt=f"Item ID: {item['item_id']} | Quantity: {item['quantity']}", ln=True)
    
#     pdf.ln(5)
#     pdf.cell(200, 10, txt=f"Total Amount: {total_amount}", ln=True)
    
#     if not os.path.exists("invoices"):
#         os.makedirs("invoices")
#     filename = f"invoices/invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
#     pdf.output(filename)
#     return filename

# # ====================== Auto Backup ======================
# def auto_backup():
#     while True:
#         today_str = datetime.now().strftime('%Y%m%d')
#         backup_folder = f"backups/{today_str}"
#         os.makedirs(backup_folder, exist_ok=True)
#         shutil.copy(DB, f"{backup_folder}/shop_backup.db")
#         # PDF invoices copy
#         if os.path.exists("invoices"):
#             shutil.copytree("invoices", f"{backup_folder}/invoices", dirs_exist_ok=True)
#         # Wait 24 hours
#         threading.Event().wait(86400)

# backup_thread = threading.Thread(target=auto_backup, daemon=True)
# backup_thread.start()

# # ====================== Run Flask App ======================
# if __name__ == "__main__":
#     app.run(debug=True)
















# # app.py
# """
# Single-file Shop Dashboard (Frontend + Backend)
# Features:
# - Stock management (add/list with auto-date)
# - Sale management (multi-item sale, invoice PDF)
# - Ledger (supplier/customer/expense)
# - Expense management
# - Sale analytics
# - Daily auto-backup (local) + optional Google Drive upload stub
# - Frontend served from same Flask app (no separate build)
# """

# import os
# import sqlite3
# import json
# import threading
# from datetime import datetime, date
# from fpdf import FPDF
# from flask import Flask, request, jsonify, send_from_directory, render_template_string, abort

# # Optional Google Drive libs (only required if you enable upload_to_gdrive)
# try:
#     from google.oauth2 import service_account
#     from googleapiclient.discovery import build
#     DRIVE_LIBS_AVAILABLE = True
# except Exception:
#     DRIVE_LIBS_AVAILABLE = False

# # Setup
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DB_PATH = os.path.join(BASE_DIR, "shop.db")
# INVOICES_DIR = os.path.join(BASE_DIR, "invoices")
# BACKUPS_DIR = os.path.join(BASE_DIR, "backups")
# os.makedirs(INVOICES_DIR, exist_ok=True)
# os.makedirs(BACKUPS_DIR, exist_ok=True)

# app = Flask(__name__, static_folder=None)

# # -----------------------
# # Database init & helpers
# # -----------------------
# def get_conn():
#     return sqlite3.connect(DB_PATH)

# def init_db():
#     conn = get_conn()
#     c = conn.cursor()
#     # Stock table
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS stock(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             item_name TEXT NOT NULL,
#             quantity INTEGER NOT NULL,
#             price REAL NOT NULL,
#             date_added TEXT NOT NULL
#         )
#     """)
#     # Sale table (items saved as JSON)
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS sale(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             date TEXT NOT NULL,
#             items TEXT NOT NULL,
#             total_amount REAL NOT NULL,
#             customer_credit REAL DEFAULT 0
#         )
#     """)
#     # Ledger table
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS ledger(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             type TEXT NOT NULL,
#             amount REAL NOT NULL,
#             date TEXT NOT NULL
#         )
#     """)
#     # Expense table
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS expense(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             description TEXT NOT NULL,
#             amount REAL NOT NULL,
#             date TEXT NOT NULL
#         )
#     """)
#     conn.commit()
#     conn.close()

# init_db()

# # -----------------------
# # Utility functions
# # -----------------------
# def to_date_str(d=None):
#     if d is None:
#         d = datetime.now()
#     return d.strftime("%Y-%m-%d")

# def generate_invoice_pdf(items, total_amount, sale_id=None):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(0, 10, f"Invoice #{sale_id or ''} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
#     pdf.ln(4)
#     pdf.set_font("Arial", size=11)
#     pdf.cell(40, 8, "Item", border=1)
#     pdf.cell(30, 8, "Qty", border=1)
#     pdf.cell(30, 8, "Rate", border=1)
#     pdf.cell(40, 8, "Subtotal", border=1)
#     pdf.ln()
#     for it in items:
#         name = it.get("item_name") or f"ID:{it.get('item_id')}"
#         qty = it.get("quantity", 0)
#         rate = it.get("rate", 0)
#         subtotal = qty * rate
#         pdf.cell(40, 8, str(name), border=1)
#         pdf.cell(30, 8, str(qty), border=1)
#         pdf.cell(30, 8, f"{rate}", border=1)
#         pdf.cell(40, 8, f"{subtotal}", border=1)
#         pdf.ln()
#     pdf.ln(4)
#     pdf.cell(0, 8, f"Total: {total_amount}", ln=True)
#     # Save
#     filename = f"invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
#     path = os.path.join(INVOICES_DIR, filename)
#     pdf.output(path)
#     return filename, path

# # -----------------------
# # Google Drive upload stub
# # -----------------------
# def upload_to_gdrive(filepath, credentials_json_path=None, folder_id=None):
#     """
#     Optional: upload a file to Google Drive.
#     - credentials_json_path: path to Service Account JSON (recommended)
#     - folder_id: Drive folder id where to upload
#     NOTE: google-api-python-client and google-auth libraries must be installed.
#     """
#     if not DRIVE_LIBS_AVAILABLE:
#         print("Google Drive libraries not installed. Skipping upload.")
#         return False
#     if not credentials_json_path or not os.path.exists(credentials_json_path):
#         print("No valid service account JSON provided. Skipping upload.")
#         return False
#     SCOPES = ["https://www.googleapis.com/auth/drive.file"]
#     creds = service_account.Credentials.from_service_account_file(credentials_json_path, scopes=SCOPES)
#     service = build("drive", "v3", credentials=creds)
#     metadata = {"name": os.path.basename(filepath)}
#     if folder_id:
#         metadata["parents"] = [folder_id]
#     media_body = None
#     from googleapiclient.http import MediaFileUpload
#     media = MediaFileUpload(filepath, resumable=True)
#     file = service.files().create(body=metadata, media_body=media, fields="id").execute()
#     print("Uploaded to Drive, file id:", file.get("id"))
#     return True

# # -----------------------
# # API endpoints
# # -----------------------

# # Add stock (date auto set and supplier credit ledger)
# @app.route("/add_stock", methods=["POST"])
# def add_stock():
#     data = request.json
#     item_name = data.get("item_name")
#     quantity = int(data.get("quantity", 0))
#     price = float(data.get("price", 0))
#     date_added = to_date_str()
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("INSERT INTO stock (item_name, quantity, price, date_added) VALUES (?, ?, ?, ?)",
#               (item_name, quantity, price, date_added))
#     # ledger supplier credit
#     supplier_amount = quantity * price
#     c.execute("INSERT INTO ledger (type, amount, date) VALUES (?, ?, ?)",
#               ("supplier", supplier_amount, date_added))
#     conn.commit()
#     conn.close()
#     return jsonify({"status":"success", "message":"Stock added"})

# # List stock (return sequential id in frontend)
# @app.route("/list_stock", methods=["GET"])
# def list_stock():
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("SELECT id, item_name, quantity, price, date_added FROM stock ORDER BY id ASC")
#     rows = c.fetchall()
#     conn.close()
#     # Return rows as list of dicts; frontend will show seq id (1..n)
#     out = []
#     for r in rows:
#         out.append({"id": r[0], "item_name": r[1], "quantity": r[2], "price": r[3], "date_added": r[4]})
#     return jsonify(out)

# # Add Sale (multiple items support, update stock, add ledger entry if customer credit)
# @app.route("/add_sale", methods=["POST"])
# def add_sale():
#     data = request.json
#     items = data.get("items", [])  # each: {"item_id":.., "quantity":..}
#     customer_credit = float(data.get("customer_credit", 0) or 0)
#     conn = get_conn()
#     c = conn.cursor()
#     total_amount = 0.0
#     # enrich items with item_name and rate
#     enriched = []
#     for it in items:
#         item_id = int(it.get("item_id"))
#         qty = int(it.get("quantity", 0))
#         c.execute("SELECT item_name, quantity, price FROM stock WHERE id=?", (item_id,))
#         row = c.fetchone()
#         if not row:
#             conn.close()
#             return jsonify({"status":"error", "message":f"Item id {item_id} not found"}), 400
#         name, stock_qty, price = row
#         if stock_qty < qty:
#             conn.close()
#             return jsonify({"status":"error", "message":f"Not enough stock for {name} (id {item_id})"}), 400
#         # update stock
#         new_qty = stock_qty - qty
#         c.execute("UPDATE stock SET quantity=? WHERE id=?", (new_qty, item_id))
#         subtotal = qty * price
#         total_amount += subtotal
#         enriched.append({"item_id": item_id, "item_name": name, "quantity": qty, "rate": price, "subtotal": subtotal})
#     date_now = to_date_str()
#     c.execute("INSERT INTO sale (date, items, total_amount, customer_credit) VALUES (?, ?, ?, ?)",
#               (date_now, json.dumps(enriched), total_amount, customer_credit))
#     sale_id = c.lastrowid
#     # if customer credit > 0 add to ledger
#     if customer_credit > 0:
#         c.execute("INSERT INTO ledger (type, amount, date) VALUES (?, ?, ?)",
#                   ("customer", customer_credit, date_now))
#     conn.commit()
#     conn.close()
#     # generate invoice
#     filename, path = generate_invoice_pdf(enriched, total_amount, sale_id)
#     return jsonify({"status":"success", "message":"Sale recorded", "total_amount": total_amount, "invoice": f"/invoices/{filename}", "sale_id": sale_id})

# # Serve invoice files
# @app.route("/invoices/<path:filename>")
# def serve_invoice(filename):
#     fullpath = os.path.join(INVOICES_DIR, filename)
#     if not os.path.exists(fullpath):
#         abort(404)
#     return send_from_directory(INVOICES_DIR, filename)

# # Add expense
# @app.route("/add_expense", methods=["POST"])
# def add_expense():
#     data = request.json
#     desc = data.get("description")
#     amount = float(data.get("amount", 0))
#     date_now = to_date_str()
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("INSERT INTO expense (description, amount, date) VALUES (?, ?, ?)",
#               (desc, amount, date_now))
#     # Also add to ledger as expense
#     c.execute("INSERT INTO ledger (type, amount, date) VALUES (?, ?, ?)",
#               ("expense", amount, date_now))
#     conn.commit()
#     conn.close()
#     return jsonify({"status":"success", "message":"Expense recorded"})

# # Ledger view
# @app.route("/ledger", methods=["GET"])
# def ledger_view():
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("SELECT id, type, amount, date FROM ledger ORDER BY id ASC")
#     rows = c.fetchall()
#     conn.close()
#     out = [{"id": r[0], "type": r[1], "amount": r[2], "date": r[3]} for r in rows]
#     return jsonify(out)

# # Sale analytics
# @app.route("/sale_analytics", methods=["GET"])
# def sale_analytics():
#     conn = get_conn()
#     c = conn.cursor()
#     # total sales
#     c.execute("SELECT SUM(total_amount) FROM sale")
#     total_sales = c.fetchone()[0] or 0
#     # sales today
#     today = to_date_str()
#     c.execute("SELECT SUM(total_amount) FROM sale WHERE date=?", (today,))
#     sales_today = c.fetchone()[0] or 0
#     # items sold counts
#     c.execute("SELECT items FROM sale")
#     rows = c.fetchall()
#     items_sold = {}
#     for r in rows:
#         items = json.loads(r[0])
#         for it in items:
#             iid = str(it["item_id"])
#             items_sold[iid] = items_sold.get(iid, 0) + int(it["quantity"])
#     conn.close()
#     return jsonify({"total_sales": total_sales, "sales_today": sales_today, "items_sold": items_sold})

# # Export quick backup (manual trigger)
# @app.route("/create_backup", methods=["POST"])
# def create_backup_route():
#     success, folder = create_daily_backup(upload=False)  # default: no upload
#     if success:
#         return jsonify({"status":"success", "backup_folder": folder})
#     return jsonify({"status":"error"}), 500

# # -----------------------
# # Backup generation
# # -----------------------
# def create_pdf_summary(path):
#     # create a PDF summary of stock, sales, ledger
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(0, 8, f"Backup Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
#     pdf.ln(4)
#     conn = get_conn()
#     c = conn.cursor()
#     # stock
#     pdf.set_font("Arial", size=11)
#     pdf.cell(0, 8, "STOCK:", ln=True)
#     c.execute("SELECT id, item_name, quantity, price, date_added FROM stock")
#     for r in c.fetchall():
#         pdf.cell(0, 6, f"ID:{r[0]} {r[1]} | qty:{r[2]} | price:{r[3]} | added:{r[4]}", ln=True)
#     pdf.ln(4)
#     # sales
#     pdf.cell(0, 8, "SALES:", ln=True)
#     c.execute("SELECT id, date, items, total_amount, customer_credit FROM sale")
#     for r in c.fetchall():
#         pdf.cell(0, 6, f"SaleID:{r[0]} Date:{r[1]} Total:{r[3]} Credit:{r[4]}", ln=True)
#     pdf.ln(4)
#     # ledger
#     pdf.cell(0, 8, "LEDGER:", ln=True)
#     c.execute("SELECT id, type, amount, date FROM ledger")
#     for r in c.fetchall():
#         pdf.cell(0, 6, f"ID:{r[0]} {r[1]} | {r[2]} | {r[3]}", ln=True)
#     conn.close()
#     pdf.output(path)

# def create_daily_backup(upload=False, credentials_json_path=None, drive_folder_id=None):
#     today_str = datetime.now().strftime("%Y%m%d")
#     folder = os.path.join(BACKUPS_DIR, today_str)
#     os.makedirs(folder, exist_ok=True)
#     # copy invoices
#     invoices_dest = os.path.join(folder, "invoices")
#     os.makedirs(invoices_dest, exist_ok=True)
#     for fname in os.listdir(INVOICES_DIR):
#         src = os.path.join(INVOICES_DIR, fname)
#         dst = os.path.join(invoices_dest, fname)
#         try:
#             if os.path.isfile(src):
#                 with open(src, "rb") as fin, open(dst, "wb") as fout:
#                     fout.write(fin.read())
#         except Exception as e:
#             print("copy invoice err:", e)
#     # DB copy
#     try:
#         db_copy = os.path.join(folder, "shop_backup.db")
#         with open(DB_PATH, "rb") as fin, open(db_copy, "wb") as fout:
#             fout.write(fin.read())
#     except Exception as e:
#         print("db copy err:", e)
#     # PDF summary
#     pdf_path = os.path.join(folder, f"summary_{today_str}.pdf")
#     try:
#         create_pdf_summary(pdf_path)
#     except Exception as e:
#         print("pdf summary err:", e)
#     # optional upload to Google Drive
#     uploaded = False
#     if upload:
#         uploaded = upload_to_gdrive(pdf_path, credentials_json_path, drive_folder_id)
#     return True, folder

# # Auto backup thread (every 24h)
# def backup_worker():
#     while True:
#         try:
#             create_daily_backup(upload=False)
#         except Exception as e:
#             print("backup_worker error:", e)
#         # sleep 24 hours
#         threading.Event().wait(86400)

# backup_thread = threading.Thread(target=backup_worker, daemon=True)
# backup_thread.start()

# # -----------------------
# # Frontend page (single-page app) - embedded HTML + minimal CSS to look modern
# # -----------------------
# INDEX_HTML = r"""
# <!doctype html>
# <html>
# <head>
#   <meta charset="utf-8">
#   <title>Shop Dashboard</title>
#   <meta name="viewport" content="width=device-width, initial-scale=1">
#   <style>
#     /* Minimal modern styling (Tailwind-like feel without building Tailwind) */
#     :root{--bg:#f3f4f6;--card:#fff;--muted:#6b7280;--accent:#2563eb;}
#     body{font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; background:var(--bg); margin:0; padding:20px;}
#     .container{max-width:1100px;margin:0 auto;}
#     .card{background:var(--card);border-radius:12px;padding:16px;box-shadow:0 6px 18px rgba(15,23,42,0.06);margin-bottom:16px;}
#     h1{font-size:22px;margin:0 0 12px 0;}
#     label{font-size:13px;color:var(--muted);display:block;margin-bottom:6px;}
#     input, select{width:100%;padding:8px;border:1px solid #e6e9ee;border-radius:8px;margin-bottom:8px;box-sizing:border-box;}
#     .grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;}
#     .btn{display:inline-block;padding:8px 12px;border-radius:8px;background:var(--accent);color:white;text-decoration:none;border:none;cursor:pointer;}
#     .btn-ghost{background:#efefef;color:#111}
#     table{width:100%;border-collapse:collapse;}
#     th,td{padding:8px;text-align:left;border-bottom:1px solid #f1f5f9;font-size:13px;}
#     .small{font-size:12px;color:var(--muted);}
#     @media(max-width:900px){ .grid{grid-template-columns:1fr;} }
#     .flex{display:flex;gap:8px;align-items:center;}
#     .right{display:flex;gap:8px;justify-content:flex-end;}
#     .muted{color:var(--muted)}
#     .seq{width:36px;text-align:center}
#     .danger{background:#ef4444}
#   </style>
# </head>
# <body>
#   <div class="container">
#     <h1>🛒 Shop Dashboard</h1>

#     <div class="grid">
#       <div class="card">
#         <h3>Add Stock</h3>
#         <div class="small muted">Date auto-set on server</div>
#         <label>Item name</label>
#         <input id="stock_item" placeholder="e.g. Rice 5kg">
#         <label>Quantity</label>
#         <input id="stock_qty" type="number" min="1" value="1">
#         <label>Price (per unit)</label>
#         <input id="stock_price" type="number" step="0.01" value="0">
#         <div class="flex">
#           <button class="btn" onclick="addStock()">Add Stock</button>
#           <button class="btn btn-ghost" onclick="refreshStocks()">Refresh</button>
#         </div>
#       </div>

#       <div class="card">
#         <h3>Create Sale / Invoice</h3>
#         <div id="saleRows"></div>
#         <div style="margin-top:8px;">
#           <button class="btn btn-ghost" onclick="addSaleRow()">+ Add Item Row</button>
#         </div>
#         <label>Customer Credit (if any)</label>
#         <input id="customer_credit" type="number" step="0.01" value="0">
#         <div class="flex" style="margin-top:8px;">
#           <button class="btn" onclick="submitSale()">Submit Sale & Print</button>
#           <button class="btn btn-ghost" onclick="refreshAll()">Refresh All</button>
#         </div>
#         <div id="sale_msg" class="small muted"></div>
#       </div>
#     </div>

#     <div class="grid">
#       <div class="card">
#         <h3>Stock List</h3>
#         <div class="small muted">IDs shown sequentially (visual)</div>
#         <div style="max-height:260px; overflow:auto;">
#           <table id="stockTable"><thead><tr><th class="seq">#</th><th>Item</th><th>Qty</th><th>Price</th><th>Date</th></tr></thead><tbody></tbody></table>
#         </div>
#       </div>

#       <div class="card">
#         <h3>Quick Actions & Backups</h3>
#         <div class="small muted">Auto backup runs daily. You can also trigger manual backup.</div>
#         <div style="margin-top:8px;" class="flex">
#           <button class="btn" onclick="manualBackup()">Create Backup Now</button>
#           <button class="btn btn-ghost" onclick="openBackups()">Open Backups Folder</button>
#         </div>

#         <hr style="margin:12px 0;">

#         <h4>Sales Analytics</h4>
#         <div id="analytics"></div>

#       </div>
#     </div>

#     <div class="grid">
#       <div class="card">
#         <h3>Add Expense</h3>
#         <label>Description</label><input id="expense_desc" placeholder="salary / bills">
#         <label>Amount</label><input id="expense_amount" type="number" step="0.01" value="0">
#         <div class="flex"><button class="btn" onclick="addExpense()">Add Expense</button></div>
#       </div>

#       <div class="card">
#         <h3>Ledger</h3>
#         <div style="max-height:320px; overflow:auto;">
#           <table id="ledgerTable"><thead><tr><th class="seq">#</th><th>Type</th><th>Amount</th><th>Date</th></tr></thead><tbody></tbody></table>
#         </div>
#       </div>
#     </div>

#     <div class="card">
#       <h3>Invoices (recent)</h3>
#       <div id="invoicesList" class="small muted"></div>
#     </div>

#   </div>

# <script>
# async function api(path, method='GET', body=null){
#   const opts = {method, headers:{}};
#   if(body!==null){ opts.headers['Content-Type']='application/json'; opts.body = JSON.stringify(body); }
#   const res = await fetch(path, opts);
#   return res.json();
# }

# async function refreshStocks(){
#   const stocks = await api('/list_stock');
#   const tbody = document.querySelector('#stockTable tbody');
#   tbody.innerHTML = '';
#   // show sequential visual ids
#   stocks.forEach((s, idx) => {
#     const tr = document.createElement('tr');
#     tr.innerHTML = `<td class="seq">${idx+1}</td><td>${s.item_name}</td><td>${s.quantity}</td><td>${s.price}</td><td>${s.date_added}</td>`;
#     tbody.appendChild(tr);
#   });
#   // also refresh sale rows stock options
#   refreshSaleRowsOptions(stocks);
# }

# async function refreshLedger(){
#   const ledger = await api('/ledger');
#   const tbody = document.querySelector('#ledgerTable tbody');
#   tbody.innerHTML = '';
#   ledger.forEach((l, idx)=> {
#     const tr = document.createElement('tr');
#     tr.innerHTML = `<td class="seq">${l.id}</td><td>${l.type}</td><td>${l.amount}</td><td>${l.date}</td>`;
#     tbody.appendChild(tr);
#   });
# }

# async function refreshInvoices(){
#   // list invoice files from server: we'll try reading /invoices/ dir via a simple fetch (not listed by default)
#   // The backend does not expose a direct listing for security; we will instead show recent invoice filenames by scanning invoices endpoint via /invoices-list
#   try {
#     const data = await api('/invoices_list');
#     const cont = document.getElementById('invoicesList');
#     cont.innerHTML = '';
#     data.forEach(f => {
#       const a = document.createElement('a');
#       a.href = '/invoices/'+f;
#       a.target = '_blank';
#       a.textContent = f;
#       a.style.display = 'inline-block';
#       a.style.marginRight = '8px';
#       cont.appendChild(a);
#     });
#   } catch(e){}
# }

# async function refreshAnalytics(){
#   const a = await api('/sale_analytics');
#   const container = document.getElementById('analytics');
#   container.innerHTML = `<div>Total sales: <strong>${a.total_sales}</strong></div>
#     <div>Sales today: <strong>${a.sales_today}</strong></div>
#     <div>Items sold:</div>`;
#   const ul = document.createElement('ul'); ul.className='small';
#   for(const k in a.items_sold){
#     const li = document.createElement('li'); li.textContent = `Item ID ${k}: ${a.items_sold[k]} pcs`; ul.appendChild(li);
#   }
#   container.appendChild(ul);
# }

# async function refreshAll(){
#   await refreshStocks();
#   await refreshLedger();
#   await refreshInvoices();
#   await refreshAnalytics();
# }

# async function addStock(){
#   const item = document.getElementById('stock_item').value.trim();
#   const qty = Number(document.getElementById('stock_qty').value||0);
#   const price = Number(document.getElementById('stock_price').value||0);
#   if(!item||qty<=0){ alert('Provide item and qty'); return; }
#   const res = await api('/add_stock','POST',{item_name:item, quantity:qty, price:price});
#   alert(res.message || (res.status=='success'?'Added':'Error'));
#   document.getElementById('stock_item').value='';
#   document.getElementById('stock_qty').value=1;
#   document.getElementById('stock_price').value=0;
#   await refreshAll();
# }

# let saleRowCount = 0;
# function addSaleRow(){
#   saleRowCount++;
#   const wrapper = document.getElementById('saleRows');
#   const row = document.createElement('div');
#   row.id = 'saleRow_'+saleRowCount;
#   row.style.marginBottom='8px';
#   row.innerHTML = `
#     <select id="sale_item_${saleRowCount}"></select>
#     <input id="sale_qty_${saleRowCount}" type="number" min="1" value="1" style="width:100px;display:inline-block;margin-left:8px;">
#     <button onclick="removeSaleRow(${saleRowCount})" class="btn btn-ghost" style="margin-left:8px">Del</button>
#   `;
#   wrapper.appendChild(row);
#   refreshSaleRowsOptionsCache();
# }
# function removeSaleRow(id){
#   const el = document.getElementById('saleRow_'+id);
#   if(el) el.remove();
# }
# let lastStocksCache = [];
# async function refreshSaleRowsOptions(stocks){
#   lastStocksCache = stocks || lastStocksCache;
#   // update all selects
#   for(let i=1;i<=saleRowCount;i++){
#     const sel = document.getElementById('sale_item_'+i);
#     if(!sel) continue;
#     sel.innerHTML = '<option value="">Select item</option>';
#     lastStocksCache.forEach(s => {
#       const opt = document.createElement('option');
#       opt.value = s.id;
#       opt.text = `${s.item_name} (id:${s.id}) - ${s.quantity}pcs`;
#       sel.appendChild(opt);
#     });
#   }
# }
# async function refreshSaleRowsOptionsCache(){
#   const stocks = await api('/list_stock');
#   await refreshSaleRowsOptions(stocks);
# }

# async function submitSale(){
#   // gather rows
#   const items=[];
#   for(let i=1;i<=saleRowCount;i++){
#     const sel = document.getElementById('sale_item_'+i);
#     const qty = document.getElementById('sale_qty_'+i);
#     if(!sel) continue;
#     if(sel.value){
#       items.push({item_id: Number(sel.value), quantity: Number(qty.value)});
#     }
#   }
#   if(items.length===0){ alert('Add at least one item'); return; }
#   const customer_credit = Number(document.getElementById('customer_credit').value || 0);
#   const res = await api('/add_sale','POST', {items, customer_credit});
#   if(res.status === 'success'){
#     // open invoice
#     if(res.invoice){
#       window.open(res.invoice, '_blank');
#     }
#     alert('Sale recorded. Total: '+res.total_amount);
#     // reset sale
#     document.getElementById('saleRows').innerHTML='';
#     saleRowCount = 0;
#     addSaleRow(); // one row by default
#     document.getElementById('customer_credit').value=0;
#     await refreshAll();
#   } else {
#     alert(res.message || 'Sale failed');
#   }
# }

# async function addExpense(){
#   const desc = document.getElementById('expense_desc').value.trim();
#   const amt = Number(document.getElementById('expense_amount').value || 0);
#   if(!desc||amt<=0){ alert('Provide desc and amount'); return; }
#   const res = await api('/add_expense','POST',{description:desc, amount:amt});
#   alert(res.message || 'Expense added');
#   document.getElementById('expense_desc').value='';
#   document.getElementById('expense_amount').value=0;
#   await refreshAll();
# }

# async function manualBackup(){
#   const res = await api('/create_backup','POST', {});
#   if(res.status === 'success') alert('Backup created: '+res.backup_folder);
#   else alert('Backup failed');
# }

# function openBackups(){
#   // This will open the local folder only if server exposes it — not exposed by default.
#   alert('Backups folder on server: ' + '/backups/');
# }

# async function init(){
#   // ensure at least one sale row exists
#   addSaleRow();
#   await refreshAll();
# }
# init();
# </script>
# </body>
# </html>
# """

# @app.route("/")
# def index():
#     return render_template_string(INDEX_HTML)

# # Provide a listing of invoices (used by frontend)
# @app.route("/invoices_list")
# def invoices_list():
#     try:
#         files = sorted([f for f in os.listdir(INVOICES_DIR) if f.lower().endswith('.pdf')], reverse=True)
#         return jsonify(files[:50])
#     except Exception:
#         return jsonify([])

# # -----------------------
# # Run
# # -----------------------
# if __name__ == "__main__":
#     print("Starting Shop Dashboard app...")
#     print("Open http://127.0.0.1:5000 in your browser")
#     app.run(debug=True)



















# # app.py
# """
# Single-file Shop Dashboard (Frontend + Backend)
# Implements features requested:
# - Stock add/list (date auto)
# - Sales with multi-items & invoice PDF + customer credit ledger entry
# - Supplier credit entry on add_stock
# - Expense management + ledger
# - Sale analytics (Chart.js frontend)
# - Daily auto backup (local) + optional Google Drive upload
# - Single-file Flask app serving backend APIs and frontend UI
# """

# import os
# import sqlite3
# import json
# import threading
# from datetime import datetime
# from fpdf import FPDF
# from flask import Flask, request, jsonify, send_from_directory, render_template_string, abort

# # Optional Google Drive libs - install only if you want uploads:
# try:
#     from google.oauth2 import service_account
#     from googleapiclient.discovery import build
#     from googleapiclient.http import MediaFileUpload
#     DRIVE_LIBS_AVAILABLE = True
# except Exception:
#     DRIVE_LIBS_AVAILABLE = False

# # ---------- CONFIG ----------
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DB_PATH = os.path.join(BASE_DIR, "shop.db")
# INVOICES_DIR = os.path.join(BASE_DIR, "invoices")
# BACKUPS_DIR = os.path.join(BASE_DIR, "backups")
# os.makedirs(INVOICES_DIR, exist_ok=True)
# os.makedirs(BACKUPS_DIR, exist_ok=True)

# # If you want Google Drive uploads, set these variables:
# # Example: GDRIVE_CRED_PATH = r"C:\Users\pc\Downloads\shopdashboard-eb21fdfcdcf8.json"
# GDRIVE_CRED_PATH = None
# GDRIVE_FOLDER_ID = None

# app = Flask(__name__, static_folder=None)

# # ---------- Database helpers ----------
# def get_conn():
#     return sqlite3.connect(DB_PATH)

# def init_db():
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS stock(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             item_name TEXT NOT NULL,
#             quantity INTEGER NOT NULL,
#             price REAL NOT NULL,
#             date_added TEXT NOT NULL
#         )
#     """)
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS sale(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             date TEXT NOT NULL,
#             items TEXT NOT NULL,
#             total_amount REAL NOT NULL,
#             customer_credit REAL DEFAULT 0
#         )
#     """)
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS ledger(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             type TEXT NOT NULL,
#             amount REAL NOT NULL,
#             date TEXT NOT NULL
#         )
#     """)
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS expense(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             description TEXT NOT NULL,
#             amount REAL NOT NULL,
#             date TEXT NOT NULL
#         )
#     """)
#     conn.commit()
#     conn.close()

# init_db()

# # ---------- Utilities ----------
# def to_date_str(d=None):
#     if d is None:
#         d = datetime.now()
#     return d.strftime("%Y-%m-%d")

# def generate_invoice_pdf(items, total_amount, sale_id=None):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(0, 10, f"Invoice #{sale_id or ''} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
#     pdf.ln(4)
#     pdf.set_font("Arial", size=11)
#     pdf.cell(70, 8, "Item", border=1)
#     pdf.cell(25, 8, "Qty", border=1)
#     pdf.cell(30, 8, "Rate", border=1)
#     pdf.cell(40, 8, "Subtotal", border=1)
#     pdf.ln()
#     for it in items:
#         name = it.get("item_name") or f"ID:{it.get('item_id')}"
#         qty = it.get("quantity", 0)
#         rate = it.get("rate", 0)
#         subtotal = qty * rate
#         pdf.cell(70, 8, str(name)[:35], border=1)
#         pdf.cell(25, 8, str(qty), border=1)
#         pdf.cell(30, 8, f"{rate}", border=1)
#         pdf.cell(40, 8, f"{subtotal}", border=1)
#         pdf.ln()
#     pdf.ln(4)
#     pdf.cell(0, 8, f"Total: {total_amount}", ln=True)
#     filename = f"invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
#     path = os.path.join(INVOICES_DIR, filename)
#     pdf.output(path)
#     return filename, path

# # ---------- Google Drive upload ----------
# def upload_to_gdrive(filepath, credentials_json_path=None, folder_id=None):
#     if not DRIVE_LIBS_AVAILABLE:
#         print("Google Drive libs not installed; skipping upload.")
#         return False
#     if not credentials_json_path or not os.path.exists(credentials_json_path):
#         print("No valid service account JSON provided; skipping upload.")
#         return False
#     SCOPES = ["https://www.googleapis.com/auth/drive.file"]
#     creds = service_account.Credentials.from_service_account_file(credentials_json_path, scopes=SCOPES)
#     service = build("drive", "v3", credentials=creds)
#     metadata = {"name": os.path.basename(filepath)}
#     if folder_id:
#         metadata["parents"] = [folder_id]
#     media = MediaFileUpload(filepath, resumable=True)
#     file = service.files().create(body=metadata, media_body=media, fields="id").execute()
#     print("Uploaded to Drive, file id:", file.get("id"))
#     return True

# # ---------- API endpoints ----------

# # Add stock: auto date and supplier credit in ledger
# @app.route("/add_stock", methods=["POST"])
# def add_stock():
#     data = request.json
#     item_name = data.get("item_name")
#     quantity = int(data.get("quantity", 0))
#     price = float(data.get("price", 0))
#     date_added = to_date_str()
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("INSERT INTO stock (item_name, quantity, price, date_added) VALUES (?, ?, ?, ?)",
#               (item_name, quantity, price, date_added))
#     supplier_amount = quantity * price
#     c.execute("INSERT INTO ledger (type, amount, date) VALUES (?, ?, ?)",
#               ("supplier", supplier_amount, date_added))
#     conn.commit()
#     conn.close()
#     return jsonify({"status":"success", "message":"Stock added"})

# # List stock (frontend will display sequential numbers)
# @app.route("/list_stock", methods=["GET"])
# def list_stock():
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("SELECT id, item_name, quantity, price, date_added FROM stock ORDER BY id ASC")
#     rows = c.fetchall()
#     conn.close()
#     out = [{"id": r[0], "item_name": r[1], "quantity": r[2], "price": r[3], "date_added": r[4]} for r in rows]
#     return jsonify(out)

# # Add sale: multi-items support, update stock, ledger for customer credit, generate invoice pdf
# @app.route("/add_sale", methods=["POST"])
# def add_sale():
#     data = request.json
#     items = data.get("items", [])
#     customer_credit = float(data.get("customer_credit", 0) or 0)
#     if not items or len(items) == 0:
#         return jsonify({"status":"error", "message":"No items provided"}), 400
#     conn = get_conn()
#     c = conn.cursor()
#     total_amount = 0.0
#     enriched = []
#     try:
#         for it in items:
#             item_id = int(it.get("item_id"))
#             qty = int(it.get("quantity", 0))
#             c.execute("SELECT item_name, quantity, price FROM stock WHERE id=?", (item_id,))
#             row = c.fetchone()
#             if not row:
#                 return jsonify({"status":"error", "message":f"Item id {item_id} not found"}), 400
#             name, stock_qty, price = row
#             if stock_qty < qty:
#                 return jsonify({"status":"error", "message":f"Not enough stock for {name} (id {item_id})"}), 400
#             new_qty = stock_qty - qty
#             c.execute("UPDATE stock SET quantity=? WHERE id=?", (new_qty, item_id))
#             subtotal = qty * price
#             total_amount += subtotal
#             enriched.append({"item_id": item_id, "item_name": name, "quantity": qty, "rate": price, "subtotal": subtotal})
#         date_now = to_date_str()
#         c.execute("INSERT INTO sale (date, items, total_amount, customer_credit) VALUES (?, ?, ?, ?)",
#                   (date_now, json.dumps(enriched), total_amount, customer_credit))
#         sale_id = c.lastrowid
#         if customer_credit > 0:
#             c.execute("INSERT INTO ledger (type, amount, date) VALUES (?, ?, ?)",
#                       ("customer", customer_credit, date_now))
#         conn.commit()
#     finally:
#         conn.close()
#     filename, path = generate_invoice_pdf(enriched, total_amount, sale_id)
#     return jsonify({"status":"success", "message":"Sale recorded", "total_amount": total_amount, "invoice": f"/invoices/{filename}", "sale_id": sale_id})

# # Serve invoice PDF files
# @app.route("/invoices/<path:filename>")
# def serve_invoice(filename):
#     fullpath = os.path.join(INVOICES_DIR, filename)
#     if not os.path.exists(fullpath):
#         abort(404)
#     return send_from_directory(INVOICES_DIR, filename)

# # Add expense
# @app.route("/add_expense", methods=["POST"])
# def add_expense():
#     data = request.json
#     desc = data.get("description")
#     amount = float(data.get("amount", 0))
#     date_now = to_date_str()
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("INSERT INTO expense (description, amount, date) VALUES (?, ?, ?)", (desc, amount, date_now))
#     c.execute("INSERT INTO ledger (type, amount, date) VALUES (?, ?, ?)", ("expense", amount, date_now))
#     conn.commit()
#     conn.close()
#     return jsonify({"status":"success", "message":"Expense recorded"})

# # Ledger view
# @app.route("/ledger", methods=["GET"])
# def ledger_view():
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("SELECT id, type, amount, date FROM ledger ORDER BY id ASC")
#     rows = c.fetchall()
#     conn.close()
#     out = [{"id": r[0], "type": r[1], "amount": r[2], "date": r[3]} for r in rows]
#     return jsonify(out)

# # Sale analytics: total sales, sales today, items_sold, expenses total
# @app.route("/sale_analytics", methods=["GET"])
# def sale_analytics():
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("SELECT SUM(total_amount) FROM sale")
#     total_sales = c.fetchone()[0] or 0
#     today = to_date_str()
#     c.execute("SELECT SUM(total_amount) FROM sale WHERE date=?", (today,))
#     sales_today = c.fetchone()[0] or 0
#     c.execute("SELECT items FROM sale")
#     rows = c.fetchall()
#     items_sold = {}
#     for r in rows:
#         if not r[0]:
#             continue
#         items = json.loads(r[0])
#         for it in items:
#             iid = str(it["item_id"])
#             items_sold[iid] = items_sold.get(iid, 0) + int(it["quantity"])
#     c.execute("SELECT SUM(amount) FROM expense")
#     total_expenses = c.fetchone()[0] or 0
#     conn.close()
#     return jsonify({
#         "total_sales": total_sales,
#         "sales_today": sales_today,
#         "items_sold": items_sold,
#         "total_expenses": total_expenses
#     })

# # Create manual backup
# @app.route("/create_backup", methods=["POST"])
# def create_backup_route():
#     success, folder = create_daily_backup(upload=bool(GDRIVE_CRED_PATH and GDRIVE_FOLDER_ID),
#                                          credentials_json_path=GDRIVE_CRED_PATH,
#                                          drive_folder_id=GDRIVE_FOLDER_ID)
#     if success:
#         return jsonify({"status":"success", "backup_folder": folder})
#     return jsonify({"status":"error"}), 500

# # List invoices
# @app.route("/invoices_list")
# def invoices_list():
#     try:
#         files = sorted([f for f in os.listdir(INVOICES_DIR) if f.lower().endswith('.pdf')], reverse=True)
#         return jsonify(files[:50])
#     except Exception:
#         return jsonify([])

# # ---------- Backup generation ----------
# def create_pdf_summary(path):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(0, 8, f"Backup Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
#     pdf.ln(4)
#     conn = get_conn()
#     c = conn.cursor()
#     pdf.set_font("Arial", size=11)
#     pdf.cell(0, 8, "STOCK:", ln=True)
#     c.execute("SELECT id, item_name, quantity, price, date_added FROM stock")
#     for r in c.fetchall():
#         pdf.cell(0, 6, f"ID:{r[0]} {r[1]} | qty:{r[2]} | price:{r[3]} | added:{r[4]}", ln=True)
#     pdf.ln(4)
#     pdf.cell(0, 8, "SALES:", ln=True)
#     c.execute("SELECT id, date, items, total_amount, customer_credit FROM sale")
#     for r in c.fetchall():
#         pdf.cell(0, 6, f"SaleID:{r[0]} Date:{r[1]} Total:{r[3]} Credit:{r[4]}", ln=True)
#     pdf.ln(4)
#     pdf.cell(0, 8, "LEDGER:", ln=True)
#     c.execute("SELECT id, type, amount, date FROM ledger")
#     for r in c.fetchall():
#         pdf.cell(0, 6, f"ID:{r[0]} {r[1]} | {r[2]} | {r[3]}", ln=True)
#     c.close()
#     conn.close()
#     pdf.output(path)

# def create_daily_backup(upload=False, credentials_json_path=None, drive_folder_id=None):
#     today_str = datetime.now().strftime("%Y%m%d")
#     folder = os.path.join(BACKUPS_DIR, today_str)
#     os.makedirs(folder, exist_ok=True)
#     invoices_dest = os.path.join(folder, "invoices")
#     os.makedirs(invoices_dest, exist_ok=True)
#     # copy invoices
#     for fname in os.listdir(INVOICES_DIR):
#         src = os.path.join(INVOICES_DIR, fname)
#         dst = os.path.join(invoices_dest, fname)
#         try:
#             if os.path.isfile(src):
#                 with open(src, "rb") as fin, open(dst, "wb") as fout:
#                     fout.write(fin.read())
#         except Exception as e:
#             print("copy invoice err:", e)
#     # DB copy
#     try:
#         db_copy = os.path.join(folder, "shop_backup.db")
#         with open(DB_PATH, "rb") as fin, open(db_copy, "wb") as fout:
#             fout.write(fin.read())
#     except Exception as e:
#         print("db copy err:", e)
#     # PDF summary
#     pdf_path = os.path.join(folder, f"summary_{today_str}.pdf")
#     try:
#         create_pdf_summary(pdf_path)
#     except Exception as e:
#         print("pdf summary err:", e)
#     # optionally upload to Google Drive
#     if upload and credentials_json_path:
#         try:
#             upload_to_gdrive(pdf_path, credentials_json_path, drive_folder_id)
#         except Exception as e:
#             print("gdrive upload err:", e)
#     return True, folder

# # Auto backup worker: runs every 24 hours
# def backup_worker():
#     while True:
#         try:
#             create_daily_backup(upload=bool(GDRIVE_CRED_PATH and GDRIVE_FOLDER_ID),
#                                 credentials_json_path=GDRIVE_CRED_PATH,
#                                 drive_folder_id=GDRIVE_FOLDER_ID)
#         except Exception as e:
#             print("backup_worker error:", e)
#         # sleep 24 hours
#         threading.Event().wait(86400)

# backup_thread = threading.Thread(target=backup_worker, daemon=True)
# backup_thread.start()

# # ---------- Frontend HTML (embedded; uses Chart.js CDN for analytics) ----------
# INDEX_HTML = r"""
# <!doctype html>
# <html>
# <head>
#   <meta charset="utf-8">
#   <title>Shop Dashboard</title>
#   <meta name="viewport" content="width=device-width, initial-scale=1">
#   <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
#   <style>
#     :root{--bg:#f3f4f6;--card:#fff;--muted:#6b7280;--accent:#2563eb;}
#     body{font-family:Inter,system-ui, -apple-system, 'Segoe UI', Roboto, Arial; background:var(--bg); margin:0; padding:18px;}
#     .container{max-width:1100px;margin:0 auto;}
#     .card{background:var(--card);border-radius:10px;padding:14px;box-shadow:0 6px 18px rgba(15,23,42,0.06);margin-bottom:14px;}
#     h1{font-size:20px;margin:0 0 10px 0;}
#     label{font-size:13px;color:var(--muted);display:block;margin-bottom:6px;}
#     input, select{width:100%;padding:8px;border:1px solid #e6e9ee;border-radius:8px;margin-bottom:8px;box-sizing:border-box;}
#     .grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;}
#     .btn{display:inline-block;padding:8px 12px;border-radius:8px;background:var(--accent);color:white;border:none;cursor:pointer;}
#     .btn-ghost{background:#efefef;color:#111}
#     table{width:100%;border-collapse:collapse;}
#     th,td{padding:8px;text-align:left;border-bottom:1px solid #f1f5f9;font-size:13px;}
#     .small{font-size:12px;color:var(--muted);}
#     @media(max-width:900px){ .grid{grid-template-columns:1fr;} }
#     .flex{display:flex;gap:8px;align-items:center;}
#     .seq{width:36px;text-align:center}
#   </style>
# </head>
# <body>
#   <div class="container">
#     <h1>🛒 Shop Dashboard</h1>

#     <div class="grid">
#       <div class="card">
#         <h3>Add Stock</h3>
#         <div class="small muted">Date auto-set by server</div>
#         <label>Item name</label><input id="stock_item" placeholder="e.g. Rice 5kg">
#         <label>Quantity</label><input id="stock_qty" type="number" min="1" value="1">
#         <label>Price (per unit)</label><input id="stock_price" type="number" step="0.01" value="0">
#         <div class="flex">
#           <button class="btn" onclick="addStock()">Add Stock</button>
#           <button class="btn btn-ghost" onclick="refreshStocks()">Refresh</button>
#         </div>
#         <div id="stock_msg" class="small"></div>
#       </div>

#       <div class="card">
#         <h3>Create Sale / Invoice</h3>
#         <div id="saleRows"></div>
#         <div style="margin-top:8px;"><button class="btn btn-ghost" onclick="addSaleRow()">+ Add Item Row</button></div>
#         <label>Customer Credit (if any)</label><input id="customer_credit" type="number" step="0.01" value="0">
#         <div class="flex" style="margin-top:8px;">
#           <button class="btn" onclick="submitSale()">Submit Sale & Print</button>
#           <button class="btn btn-ghost" onclick="refreshAll()">Refresh All</button>
#         </div>
#         <div id="sale_msg" class="small muted"></div>
#       </div>
#     </div>

#     <div class="grid">
#       <div class="card">
#         <h3>Stock List</h3>
#         <div class="small muted">IDs shown sequentially for display</div>
#         <div style="max-height:260px; overflow:auto;">
#           <table id="stockTable"><thead><tr><th class="seq">#</th><th>Item</th><th>Qty</th><th>Price</th><th>Date</th></tr></thead><tbody></tbody></table>
#         </div>
#       </div>

#       <div class="card">
#         <h3>Quick Actions & Backups</h3>
#         <div class="small muted">Auto backup runs daily. You can also trigger manual backup.</div>
#         <div style="margin-top:8px;" class="flex">
#           <button class="btn" onclick="manualBackup()">Create Backup Now</button>
#           <button class="btn btn-ghost" onclick="openBackups()">Open Backups Folder</button>
#         </div>
#         <hr style="margin:12px 0;">
#         <h4>Sales Analytics</h4>
#         <canvas id="salesChart" style="max-height:240px"></canvas>
#         <div id="analyticsText" class="small"></div>
#       </div>
#     </div>

#     <div class="grid">
#       <div class="card">
#         <h3>Add Expense</h3>
#         <label>Description</label><input id="expense_desc" placeholder="salary / bills">
#         <label>Amount</label><input id="expense_amount" type="number" step="0.01" value="0">
#         <div class="flex"><button class="btn" onclick="addExpense()">Add Expense</button></div>
#       </div>

#       <div class="card">
#         <h3>Ledger</h3>
#         <div style="max-height:320px; overflow:auto;">
#           <table id="ledgerTable"><thead><tr><th class="seq">#</th><th>Type</th><th>Amount</th><th>Date</th></tr></thead><tbody></tbody></table>
#         </div>
#       </div>
#     </div>

#     <div class="card">
#       <h3>Invoices (recent)</h3>
#       <div id="invoicesList" class="small muted"></div>
#     </div>

#   </div>

# <script>
# // ---- API helper
# async function api(path, method='GET', body=null){
#   const opts = {method, headers:{}};
#   if(body !== null){ opts.headers['Content-Type']='application/json'; opts.body = JSON.stringify(body); }
#   const res = await fetch(path, opts);
#   return res.json();
# }

# // ---- Stocks
# async function refreshStocks(){
#   const stocks = await api('/list_stock');
#   const tbody = document.querySelector('#stockTable tbody');
#   tbody.innerHTML = '';
#   stocks.forEach((s, idx) => {
#     const tr = document.createElement('tr');
#     tr.innerHTML = `<td class="seq">${idx+1}</td><td>${s.item_name}</td><td>${s.quantity}</td><td>${s.price}</td><td>${s.date_added}</td>`;
#     tbody.appendChild(tr);
#   });
#   refreshSaleRowsOptions(stocks);
# }

# async function addStock(){
#   const item = document.getElementById('stock_item').value.trim();
#   const qty = Number(document.getElementById('stock_qty').value||0);
#   const price = Number(document.getElementById('stock_price').value||0);
#   if(!item || qty <= 0){ alert('Provide item and qty'); return; }
#   const res = await api('/add_stock','POST',{item_name:item, quantity:qty, price:price});
#   alert(res.message || 'Added');
#   document.getElementById('stock_item').value='';
#   document.getElementById('stock_qty').value=1;
#   document.getElementById('stock_price').value=0;
#   await refreshAll();
# }

# // ---- Sale form (multiple rows)
# let saleRowCount = 0;
# function addSaleRow(){
#   saleRowCount++;
#   const wrapper = document.getElementById('saleRows');
#   const row = document.createElement('div');
#   row.id = 'saleRow_'+saleRowCount;
#   row.style.marginBottom='8px';
#   row.innerHTML = `
#     <select id="sale_item_${saleRowCount}"></select>
#     <input id="sale_qty_${saleRowCount}" type="number" min="1" value="1" style="width:100px;display:inline-block;margin-left:8px;">
#     <button onclick="removeSaleRow(${saleRowCount})" class="btn btn-ghost" style="margin-left:8px">Del</button>
#   `;
#   wrapper.appendChild(row);
#   refreshSaleRowsOptionsCache();
# }
# function removeSaleRow(id){
#   const el = document.getElementById('saleRow_'+id);
#   if(el) el.remove();
# }
# let lastStocksCache = [];
# async function refreshSaleRowsOptions(stocks){
#   lastStocksCache = stocks || lastStocksCache;
#   for(let i=1;i<=saleRowCount;i++){
#     const sel = document.getElementById('sale_item_'+i);
#     if(!sel) continue;
#     sel.innerHTML = '<option value="">Select item</option>';
#     lastStocksCache.forEach(s => {
#       const opt = document.createElement('option');
#       opt.value = s.id;
#       opt.text = `${s.item_name} (id:${s.id}) - ${s.quantity}pcs`;
#       sel.appendChild(opt);
#     });
#   }
# }
# async function refreshSaleRowsOptionsCache(){
#   const stocks = await api('/list_stock');
#   await refreshSaleRowsOptions(stocks);
# }

# async function submitSale(){
#   const items=[];
#   for(let i=1;i<=saleRowCount;i++){
#     const sel = document.getElementById('sale_item_'+i);
#     const qty = document.getElementById('sale_qty_'+i);
#     if(!sel) continue;
#     if(sel.value){
#       items.push({item_id: Number(sel.value), quantity: Number(qty.value)});
#     }
#   }
#   if(items.length===0){ alert('Add at least one item'); return; }
#   const customer_credit = Number(document.getElementById('customer_credit').value || 0);
#   const res = await api('/add_sale','POST', {items, customer_credit});
#   if(res.status === 'success'){
#     if(res.invoice){
#       window.open(res.invoice, '_blank');
#     }
#     alert('Sale recorded. Total: '+res.total_amount);
#     document.getElementById('saleRows').innerHTML='';
#     saleRowCount = 0;
#     addSaleRow();
#     document.getElementById('customer_credit').value=0;
#     await refreshAll();
#   } else {
#     alert(res.message || 'Sale failed');
#   }
# }

# // ---- Expenses
# async function addExpense(){
#   const desc = document.getElementById('expense_desc').value.trim();
#   const amt = Number(document.getElementById('expense_amount').value || 0);
#   if(!desc || amt <= 0){ alert('Provide desc and amount'); return; }
#   const res = await api('/add_expense','POST',{description:desc, amount:amt});
#   alert(res.message || 'Expense added');
#   document.getElementById('expense_desc').value='';
#   document.getElementById('expense_amount').value=0;
#   await refreshAll();
# }

# // ---- Ledger
# async function refreshLedger(){
#   const ledger = await api('/ledger');
#   const tbody = document.querySelector('#ledgerTable tbody');
#   tbody.innerHTML = '';
#   ledger.forEach((l, idx)=> {
#     const tr = document.createElement('tr');
#     tr.innerHTML = `<td class="seq">${l.id}</td><td>${l.type}</td><td>${l.amount}</td><td>${l.date}</td>`;
#     tbody.appendChild(tr);
#   });
# }

# // ---- Invoices list
# async function refreshInvoices(){
#   try {
#     const data = await api('/invoices_list');
#     const cont = document.getElementById('invoicesList');
#     cont.innerHTML = '';
#     data.forEach(f => {
#       const a = document.createElement('a');
#       a.href = '/invoices/'+f;
#       a.target = '_blank';
#       a.textContent = f;
#       a.style.display = 'inline-block';
#       a.style.marginRight = '8px';
#       cont.appendChild(a);
#     });
#   } catch(e){}
# }

# // ---- Analytics (Chart.js)
# let salesChart = null;
# async function refreshAnalytics(){
#   const a = await api('/sale_analytics');
#   const container = document.getElementById('analyticsText');
#   container.innerHTML = `<div>Total sales: <strong>${a.total_sales}</strong></div><div>Sales today: <strong>${a.sales_today}</strong></div><div>Total expenses: <strong>${a.total_expenses || a.total_expenses === 0 ? a.total_expenses : a.total_expenses}</strong></div>`;
#   // Build simple items sold chart
#   const labels = Object.keys(a.items_sold || {});
#   const data = labels.map(k => a.items_sold[k]);
#   const ctx = document.getElementById('salesChart').getContext('2d');
#   if(salesChart) salesChart.destroy();
#   salesChart = new Chart(ctx, {
#     type: 'bar',
#     data: { labels, datasets: [{ label: 'Items sold (qty)', data }] },
#     options: { responsive:true, maintainAspectRatio:false }
#   });
# }

# // ---- Backup
# async function manualBackup(){
#   const res = await api('/create_backup','POST', {});
#   if(res.status === 'success') alert('Backup created: '+res.backup_folder);
#   else alert('Backup failed');
# }
# function openBackups(){
#   alert('Backups folder on server: ' + '/backups/');
# }

# // ---- Refresh all
# async function refreshAll(){
#   await refreshStocks();
#   await refreshLedger();
#   await refreshInvoices();
#   await refreshAnalytics();
# }

# // ---- Init
# async function init(){
#   addSaleRow();
#   await refreshAll();
# }
# init();

# </script>
# </body>
# </html>
# """

# @app.route("/")
# def index():
#     return render_template_string(INDEX_HTML)

# # ---------- Run ----------
# if __name__ == "__main__":
#     print("Starting Shop Dashboard app...")
#     print("Open http://127.0.0.1:5000 in your browser")
#     app.run(debug=True)
















# # app.py
# """
# Single-file Shop Dashboard (Frontend + Backend)
# Implements features requested:
# - Stock add/list (date auto)
# - Sales with multi-items & invoice PDF + customer credit ledger entry
# - Supplier credit entry on add_stock
# - Expense management + ledger
# - Sale analytics (Chart.js frontend)
# - Daily auto backup (local) + optional Google Drive upload
# - Single-file Flask app serving backend APIs and frontend UI
# - Added Rasa Webchat for WhatsApp and menu data handling
# """

# import os
# import sqlite3
# import json
# import threading
# from datetime import datetime
# from fpdf import FPDF
# from flask import Flask, request, jsonify, send_from_directory, render_template_string, abort

# # Optional Google Drive libs - install only if you want uploads:
# try:
#     from google.oauth2 import service_account
#     from googleapiclient.discovery import build
#     from googleapiclient.http import MediaFileUpload
#     DRIVE_LIBS_AVAILABLE = True
# except Exception:
#     DRIVE_LIBS_AVAILABLE = False

# # ---------- CONFIG ----------
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DB_PATH = os.path.join(BASE_DIR, "shop.db")
# INVOICES_DIR = os.path.join(BASE_DIR, "invoices")
# BACKUPS_DIR = os.path.join(BASE_DIR, "backups")
# os.makedirs(INVOICES_DIR, exist_ok=True)
# os.makedirs(BACKUPS_DIR, exist_ok=True)

# # If you want Google Drive uploads, set these variables:
# # Example: GDRIVE_CRED_PATH = r"C:\Users\pc\Downloads\shopdashboard-eb21fdfcdcf8.json"
# GDRIVE_CRED_PATH = None
# GDRIVE_FOLDER_ID = None

# app = Flask(__name__, static_folder=None)

# # ---------- Database helpers ----------
# def get_conn():
#     return sqlite3.connect(DB_PATH)

# def init_db():
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS stock(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             item_name TEXT NOT NULL,
#             quantity INTEGER NOT NULL,
#             price REAL NOT NULL,
#             date_added TEXT NOT NULL
#         )
#     """)
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS sale(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             date TEXT NOT NULL,
#             items TEXT NOT NULL,
#             total_amount REAL NOT NULL,
#             customer_credit REAL DEFAULT 0
#         )
#     """)
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS ledger(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             type TEXT NOT NULL,
#             amount REAL NOT NULL,
#             date TEXT NOT NULL
#         )
#     """)
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS expense(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             description TEXT NOT NULL,
#             amount REAL NOT NULL,
#             date TEXT NOT NULL
#         )
#     """)
#     conn.commit()
#     conn.close()

# init_db()

# # ---------- Utilities ----------
# def to_date_str(d=None):
#     if d is None:
#         d = datetime.now()
#     return d.strftime("%Y-%m-%d")

# def generate_invoice_pdf(items, total_amount, sale_id=None):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(0, 10, f"Invoice #{sale_id or ''} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
#     pdf.ln(4)
#     pdf.set_font("Arial", size=11)
#     pdf.cell(70, 8, "Item", border=1)
#     pdf.cell(25, 8, "Qty", border=1)
#     pdf.cell(30, 8, "Rate", border=1)
#     pdf.cell(40, 8, "Subtotal", border=1)
#     pdf.ln()
#     for it in items:
#         name = it.get("item_name") or f"ID:{it.get('item_id')}"
#         qty = it.get("quantity", 0)
#         rate = it.get("rate", 0)
#         subtotal = qty * rate
#         pdf.cell(70, 8, str(name)[:35], border=1)
#         pdf.cell(25, 8, str(qty), border=1)
#         pdf.cell(30, 8, f"{rate}", border=1)
#         pdf.cell(40, 8, f"{subtotal}", border=1)
#         pdf.ln()
#     pdf.ln(4)
#     pdf.cell(0, 8, f"Total: {total_amount}", ln=True)
#     filename = f"invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
#     path = os.path.join(INVOICES_DIR, filename)
#     pdf.output(path)
#     return filename, path

# # ---------- Google Drive upload ----------
# def upload_to_gdrive(filepath, credentials_json_path=None, folder_id=None):
#     if not DRIVE_LIBS_AVAILABLE:
#         print("Google Drive libs not installed; skipping upload.")
#         return False
#     if not credentials_json_path or not os.path.exists(credentials_json_path):
#         print("No valid service account JSON provided; skipping upload.")
#         return False
#     SCOPES = ["https://www.googleapis.com/auth/drive.file"]
#     creds = service_account.Credentials.from_service_account_file(credentials_json_path, scopes=SCOPES)
#     service = build("drive", "v3", credentials=creds)
#     metadata = {"name": os.path.basename(filepath)}
#     if folder_id:
#         metadata["parents"] = [folder_id]
#     media = MediaFileUpload(filepath, resumable=True)
#     file = service.files().create(body=metadata, media_body=media, fields="id").execute()
#     print("Uploaded to Drive, file id:", file.get("id"))
#     return True

# # ---------- API endpoints ----------

# # Add stock: auto date and supplier credit in ledger
# @app.route("/add_stock", methods=["POST"])
# def add_stock():
#     data = request.json
#     item_name = data.get("item_name")
#     quantity = int(data.get("quantity", 0))
#     price = float(data.get("price", 0))
#     date_added = to_date_str()
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("INSERT INTO stock (item_name, quantity, price, date_added) VALUES (?, ?, ?, ?)",
#               (item_name, quantity, price, date_added))
#     supplier_amount = quantity * price
#     c.execute("INSERT INTO ledger (type, amount, date) VALUES (?, ?, ?)",
#               ("supplier", supplier_amount, date_added))
#     conn.commit()
#     conn.close()
#     return jsonify({"status":"success", "message":"Stock added"})

# # List stock (frontend will display sequential numbers)
# @app.route("/list_stock", methods=["GET"])
# def list_stock():
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("SELECT id, item_name, quantity, price, date_added FROM stock ORDER BY id ASC")
#     rows = c.fetchall()
#     conn.close()
#     out = [{"id": r[0], "item_name": r[1], "quantity": r[2], "price": r[3], "date_added": r[4]} for r in rows]
#     return jsonify(out)

# # Add sale: multi-items support, update stock, ledger for customer credit, generate invoice pdf
# @app.route("/add_sale", methods=["POST"])
# def add_sale():
#     data = request.json
#     items = data.get("items", [])
#     customer_credit = float(data.get("customer_credit", 0) or 0)
#     if not items or len(items) == 0:
#         return jsonify({"status":"error", "message":"No items provided"}), 400
#     conn = get_conn()
#     c = conn.cursor()
#     total_amount = 0.0
#     enriched = []
#     try:
#         for it in items:
#             item_id = int(it.get("item_id"))
#             qty = int(it.get("quantity", 0))
#             c.execute("SELECT item_name, quantity, price FROM stock WHERE id=?", (item_id,))
#             row = c.fetchone()
#             if not row:
#                 return jsonify({"status":"error", "message":f"Item id {item_id} not found"}), 400
#             name, stock_qty, price = row
#             if stock_qty < qty:
#                 return jsonify({"status":"error", "message":f"Not enough stock for {name} (id {item_id})"}), 400
#             new_qty = stock_qty - qty
#             c.execute("UPDATE stock SET quantity=? WHERE id=?", (new_qty, item_id))
#             subtotal = qty * price
#             total_amount += subtotal
#             enriched.append({"item_id": item_id, "item_name": name, "quantity": qty, "rate": price, "subtotal": subtotal})
#         date_now = to_date_str()
#         c.execute("INSERT INTO sale (date, items, total_amount, customer_credit) VALUES (?, ?, ?, ?)",
#                   (date_now, json.dumps(enriched), total_amount, customer_credit))
#         sale_id = c.lastrowid
#         if customer_credit > 0:
#             c.execute("INSERT INTO ledger (type, amount, date) VALUES (?, ?, ?)",
#                       ("customer", customer_credit, date_now))
#         conn.commit()
#     finally:
#         conn.close()
#     filename, path = generate_invoice_pdf(enriched, total_amount, sale_id)
#     return jsonify({"status":"success", "message":"Sale recorded", "total_amount": total_amount, "invoice": f"/invoices/{filename}", "sale_id": sale_id})

# # Serve invoice PDF files
# @app.route("/invoices/<path:filename>")
# def serve_invoice(filename):
#     fullpath = os.path.join(INVOICES_DIR, filename)
#     if not os.path.exists(fullpath):
#         abort(404)
#     return send_from_directory(INVOICES_DIR, filename)

# # Add expense
# @app.route("/add_expense", methods=["POST"])
# def add_expense():
#     data = request.json
#     desc = data.get("description")
#     amount = float(data.get("amount", 0))
#     date_now = to_date_str()
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("INSERT INTO expense (description, amount, date) VALUES (?, ?, ?)", (desc, amount, date_now))
#     c.execute("INSERT INTO ledger (type, amount, date) VALUES (?, ?, ?)", ("expense", amount, date_now))
#     conn.commit()
#     conn.close()
#     return jsonify({"status":"success", "message":"Expense recorded"})

# # Ledger view
# @app.route("/ledger", methods=["GET"])
# def ledger_view():
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("SELECT id, type, amount, date FROM ledger ORDER BY id ASC")
#     rows = c.fetchall()
#     conn.close()
#     out = [{"id": r[0], "type": r[1], "amount": r[2], "date": r[3]} for r in rows]
#     return jsonify(out)

# # Sale analytics: total sales, sales today, items_sold, expenses total
# @app.route("/sale_analytics", methods=["GET"])
# def sale_analytics():
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("SELECT SUM(total_amount) FROM sale")
#     total_sales = c.fetchone()[0] or 0
#     today = to_date_str()
#     c.execute("SELECT SUM(total_amount) FROM sale WHERE date=?", (today,))
#     sales_today = c.fetchone()[0] or 0
#     c.execute("SELECT items FROM sale")
#     rows = c.fetchall()
#     items_sold = {}
#     for r in rows:
#         if not r[0]:
#             continue
#         items = json.loads(r[0])
#         for it in items:
#             iid = str(it["item_id"])
#             items_sold[iid] = items_sold.get(iid, 0) + int(it["quantity"])
#     c.execute("SELECT SUM(amount) FROM expense")
#     total_expenses = c.fetchone()[0] or 0
#     conn.close()
#     return jsonify({
#         "total_sales": total_sales,
#         "sales_today": sales_today,
#         "items_sold": items_sold,
#         "total_expenses": total_expenses
#     })

# # Create manual backup
# @app.route("/create_backup", methods=["POST"])
# def create_backup_route():
#     success, folder = create_daily_backup(upload=bool(GDRIVE_CRED_PATH and GDRIVE_FOLDER_ID),
#                                          credentials_json_path=GDRIVE_CRED_PATH,
#                                          drive_folder_id=GDRIVE_FOLDER_ID)
#     if success:
#         return jsonify({"status":"success", "backup_folder": folder})
#     return jsonify({"status":"error"}), 500

# # List invoices
# @app.route("/invoices_list")
# def invoices_list():
#     try:
#         files = sorted([f for f in os.listdir(INVOICES_DIR) if f.lower().endswith('.pdf')], reverse=True)
#         return jsonify(files[:50])
#     except Exception:
#         return jsonify([])

# # ---------- Backup generation ----------
# def create_pdf_summary(path):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(0, 8, f"Backup Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
#     pdf.ln(4)
#     conn = get_conn()
#     c = conn.cursor()
#     pdf.set_font("Arial", size=11)
#     pdf.cell(0, 8, "STOCK:", ln=True)
#     c.execute("SELECT id, item_name, quantity, price, date_added FROM stock")
#     for r in c.fetchall():
#         pdf.cell(0, 6, f"ID:{r[0]} {r[1]} | qty:{r[2]} | price:{r[3]} | added:{r[4]}", ln=True)
#     pdf.ln(4)
#     pdf.cell(0, 8, "SALES:", ln=True)
#     c.execute("SELECT id, date, items, total_amount, customer_credit FROM sale")
#     for r in c.fetchall():
#         pdf.cell(0, 6, f"SaleID:{r[0]} Date:{r[1]} Total:{r[3]} Credit:{r[4]}", ln=True)
#     pdf.ln(4)
#     pdf.cell(0, 8, "LEDGER:", ln=True)
#     c.execute("SELECT id, type, amount, date FROM ledger")
#     for r in c.fetchall():
#         pdf.cell(0, 6, f"ID:{r[0]} {r[1]} | {r[2]} | {r[3]}", ln=True)
#     c.close()
#     conn.close()
#     pdf.output(path)

# def create_daily_backup(upload=False, credentials_json_path=None, drive_folder_id=None):
#     today_str = datetime.now().strftime("%Y%m%d")
#     folder = os.path.join(BACKUPS_DIR, today_str)
#     os.makedirs(folder, exist_ok=True)
#     invoices_dest = os.path.join(folder, "invoices")
#     os.makedirs(invoices_dest, exist_ok=True)
#     # copy invoices
#     for fname in os.listdir(INVOICES_DIR):
#         src = os.path.join(INVOICES_DIR, fname)
#         dst = os.path.join(invoices_dest, fname)
#         try:
#             if os.path.isfile(src):
#                 with open(src, "rb") as fin, open(dst, "wb") as fout:
#                     fout.write(fin.read())
#         except Exception as e:
#             print("copy invoice err:", e)
#     # DB copy
#     try:
#         db_copy = os.path.join(folder, "shop_backup.db")
#         with open(DB_PATH, "rb") as fin, open(db_copy, "wb") as fout:
#             fout.write(fin.read())
#     except Exception as e:
#         print("db copy err:", e)
#     # PDF summary
#     pdf_path = os.path.join(folder, f"summary_{today_str}.pdf")
#     try:
#         create_pdf_summary(pdf_path)
#     except Exception as e:
#         print("pdf summary err:", e)
#     # optionally upload to Google Drive
#     if upload and credentials_json_path:
#         try:
#             upload_to_gdrive(pdf_path, credentials_json_path, drive_folder_id)
#         except Exception as e:
#             print("gdrive upload err:", e)
#     return True, folder

# # Auto backup worker: runs every 24 hours
# def backup_worker():
#     while True:
#         try:
#             create_daily_backup(upload=bool(GDRIVE_CRED_PATH and GDRIVE_FOLDER_ID),
#                                 credentials_json_path=GDRIVE_CRED_PATH,
#                                 drive_folder_id=GDRIVE_FOLDER_ID)
#         except Exception as e:
#             print("backup_worker error:", e)
#         # sleep 24 hours
#         threading.Event().wait(86400)

# backup_thread = threading.Thread(target=backup_worker, daemon=True)
# backup_thread.start()

# # ---------- Frontend HTML (embedded; uses Chart.js CDN for analytics) ----------
# INDEX_HTML = r"""
# <!doctype html>
# <html>
# <head>
#   <meta charset="utf-8">
#   <title>Shop Dashboard</title>
#   <meta name="viewport" content="width=device-width, initial-scale=1">
#   <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
#   <!-- Add Rasa Webchat -->
#   <script src="https://cdn.jsdelivr.net/npm/rasa-webchat@1.x.x/lib/index.js"></script>
#   <style>
#     :root{--bg:#f3f4f6;--card:#fff;--muted:#6b7280;--accent:#2563eb;}
#     body{font-family:Inter,system-ui, -apple-system, 'Segoe UI', Roboto, Arial; background:var(--bg); margin:0; padding:18px;}
#     .container{max-width:1100px;margin:0 auto;}
#     .card{background:var(--card);border-radius:10px;padding:14px;box-shadow:0 6px 18px rgba(15,23,42,0.06);margin-bottom:14px;}
#     h1{font-size:20px;margin:0 0 10px 0;}
#     label{font-size:13px;color:var(--muted);display:block;margin-bottom:6px;}
#     input, select{width:100%;padding:8px;border:1px solid #e6e9ee;border-radius:8px;margin-bottom:8px;box-sizing:border-box;}
#     .grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;}
#     .btn{display:inline-block;padding:8px 12px;border-radius:8px;background:var(--accent);color:white;border:none;cursor:pointer;}
#     .btn-ghost{background:#efefef;color:#111}
#     table{width:100%;border-collapse:collapse;}
#     th,td{padding:8px;text-align:left;border-bottom:1px solid #f1f5f9;font-size:13px;}
#     .small{font-size:12px;color:var(--muted);}
#     @media(max-width:900px){ .grid{grid-template-columns:1fr;} }
#     .flex{display:flex;gap:8px;align-items:center;}
#     .seq{width:36px;text-align:center}
#     #rasa-chat-widget { position: fixed; bottom: 20px; right: 20px; }
#   </style>
# </head>
# <body>
#   <div class="container">
#     <h1>🛒 Shop Dashboard</h1>

#     <div class="grid">
#       <div class="card">
#         <h3>Add Stock</h3>
#         <div class="small muted">Date auto-set by server</div>
#         <label>Item name</label><input id="stock_item" placeholder="e.g. Rice 5kg">
#         <label>Quantity</label><input id="stock_qty" type="number" min="1" value="1">
#         <label>Price (per unit)</label><input id="stock_price" type="number" step="0.01" value="0">
#         <div class="flex">
#           <button class="btn" onclick="addStock()">Add Stock</button>
#           <button class="btn btn-ghost" onclick="refreshStocks()">Refresh</button>
#         </div>
#         <div id="stock_msg" class="small"></div>
#       </div>

#       <div class="card">
#         <h3>Create Sale / Invoice</h3>
#         <div id="saleRows"></div>
#         <div style="margin-top:8px;"><button class="btn btn-ghost" onclick="addSaleRow()">+ Add Item Row</button></div>
#         <label>Customer Credit (if any)</label><input id="customer_credit" type="number" step="0.01" value="0">
#         <div class="flex" style="margin-top:8px;">
#           <button class="btn" onclick="submitSale()">Submit Sale & Print</button>
#           <button class="btn btn-ghost" onclick="refreshAll()">Refresh All</button>
#         </div>
#         <div id="sale_msg" class="small muted"></div>
#       </div>
#     </div>

#     <div class="grid">
#       <div class="card">
#         <h3>Stock List</h3>
#         <div class="small muted">IDs shown sequentially for display</div>
#         <div style="max-height:260px; overflow:auto;">
#           <table id="stockTable"><thead><tr><th class="seq">#</th><th>Item</th><th>Qty</th><th>Price</th><th>Date</th></tr></thead><tbody></tbody></table>
#         </div>
#       </div>

#       <div class="card">
#         <h3>Quick Actions & Backups</h3>
#         <div class="small muted">Auto backup runs daily. You can also trigger manual backup.</div>
#         <div style="margin-top:8px;" class="flex">
#           <button class="btn" onclick="manualBackup()">Create Backup Now</button>
#           <button class="btn btn-ghost" onclick="openBackups()">Open Backups Folder</button>
#         </div>
#         <hr style="margin:12px 0;">
#         <h4>Sales Analytics</h4>
#         <canvas id="salesChart" style="max-height:240px"></canvas>
#         <div id="analyticsText" class="small"></div>
#       </div>
#     </div>

#     <div class="grid">
#       <div class="card">
#         <h3>Add Expense</h3>
#         <label>Description</label><input id="expense_desc" placeholder="salary / bills">
#         <label>Amount</label><input id="expense_amount" type="number" step="0.01" value="0">
#         <div class="flex"><button class="btn" onclick="addExpense()">Add Expense</button></div>
#       </div>

#       <div class="card">
#         <h3>Ledger</h3>
#         <div style="max-height:320px; overflow:auto;">
#           <table id="ledgerTable"><thead><tr><th class="seq">#</th><th>Type</th><th>Amount</th><th>Date</th></tr></thead><tbody></tbody></table>
#         </div>
#       </div>
#     </div>

#     <div class="card">
#       <h3>Invoices (recent)</h3>
#       <div id="invoicesList" class="small muted"></div>
#     </div>

#     <!-- Rasa Chat Widget -->
#     <div id="rasa-chat-widget"></div>
#   </div>

# <script>
# // ---- API helper
# async function api(path, method='GET', body=null){
#   const opts = {method, headers:{}};
#   if(body !== null){ opts.headers['Content-Type']='application/json'; opts.body = JSON.stringify(body); }
#   const res = await fetch(path, opts);
#   return res.json();
# }

# // ---- Stocks
# async function refreshStocks(){
#   const stocks = await api('/list_stock');
#   const tbody = document.querySelector('#stockTable tbody');
#   tbody.innerHTML = '';
#   stocks.forEach((s, idx) => {
#     const tr = document.createElement('tr');
#     tr.innerHTML = `<td class="seq">${idx+1}</td><td>${s.item_name}</td><td>${s.quantity}</td><td>${s.price}</td><td>${s.date_added}</td>`;
#     tbody.appendChild(tr);
#   });
#   refreshSaleRowsOptions(stocks);
# }

# async function addStock(){
#   const item = document.getElementById('stock_item').value.trim();
#   const qty = Number(document.getElementById('stock_qty').value||0);
#   const price = Number(document.getElementById('stock_price').value||0);
#   if(!item || qty <= 0){ alert('Provide item and qty'); return; }
#   const res = await api('/add_stock','POST',{item_name:item, quantity:qty, price:price});
#   alert(res.message || 'Added');
#   document.getElementById('stock_item').value='';
#   document.getElementById('stock_qty').value=1;
#   document.getElementById('stock_price').value=0;
#   await refreshAll();
# }

# // ---- Sale form (multiple rows)
# let saleRowCount = 0;
# function addSaleRow(){
#   saleRowCount++;
#   const wrapper = document.getElementById('saleRows');
#   const row = document.createElement('div');
#   row.id = 'saleRow_'+saleRowCount;
#   row.style.marginBottom='8px';
#   row.innerHTML = `
#     <select id="sale_item_${saleRowCount}"></select>
#     <input id="sale_qty_${saleRowCount}" type="number" min="1" value="1" style="width:100px;display:inline-block;margin-left:8px;">
#     <button onclick="removeSaleRow(${saleRowCount})" class="btn btn-ghost" style="margin-left:8px">Del</button>
#   `;
#   wrapper.appendChild(row);
#   refreshSaleRowsOptionsCache();
# }
# function removeSaleRow(id){
#   const el = document.getElementById('saleRow_'+id);
#   if(el) el.remove();
# }
# let lastStocksCache = [];
# async function refreshSaleRowsOptions(stocks){
#   lastStocksCache = stocks || lastStocksCache;
#   for(let i=1;i<=saleRowCount;i++){
#     const sel = document.getElementById('sale_item_'+i);
#     if(!sel) continue;
#     sel.innerHTML = '<option value="">Select item</option>';
#     lastStocksCache.forEach(s => {
#       const opt = document.createElement('option');
#       opt.value = s.id;
#       opt.text = `${s.item_name} (id:${s.id}) - ${s.quantity}pcs`;
#       sel.appendChild(opt);
#     });
#   }
# }
# async function refreshSaleRowsOptionsCache(){
#   const stocks = await api('/list_stock');
#   await refreshSaleRowsOptions(stocks);
# }

# async function submitSale(){
#   const items=[];
#   for(let i=1;i<=saleRowCount;i++){
#     const sel = document.getElementById('sale_item_'+i);
#     const qty = document.getElementById('sale_qty_'+i);
#     if(!sel) continue;
#     if(sel.value){
#       items.push({item_id: Number(sel.value), quantity: Number(qty.value)});
#     }
#   }
#   if(items.length===0){ alert('Add at least one item'); return; }
#   const customer_credit = Number(document.getElementById('customer_credit').value || 0);
#   const res = await api('/add_sale','POST', {items, customer_credit});
#   if(res.status === 'success'){
#     if(res.invoice){
#       window.open(res.invoice, '_blank');
#     }
#     alert('Sale recorded. Total: '+res.total_amount);
#     document.getElementById('saleRows').innerHTML='';
#     saleRowCount = 0;
#     addSaleRow();
#     document.getElementById('customer_credit').value=0;
#     await refreshAll();
#   } else {
#     alert(res.message || 'Sale failed');
#   }
# }

# // ---- Expenses
# async function addExpense(){
#   const desc = document.getElementById('expense_desc').value.trim();
#   const amt = Number(document.getElementById('expense_amount').value || 0);
#   if(!desc || amt <= 0){ alert('Provide desc and amount'); return; }
#   const res = await api('/add_expense','POST',{description:desc, amount:amt});
#   alert(res.message || 'Expense added');
#   document.getElementById('expense_desc').value='';
#   document.getElementById('expense_amount').value=0;
#   await refreshAll();
# }

# // ---- Ledger
# async function refreshLedger(){
#   const ledger = await api('/ledger');
#   const tbody = document.querySelector('#ledgerTable tbody');
#   tbody.innerHTML = '';
#   ledger.forEach((l, idx)=> {
#     const tr = document.createElement('tr');
#     tr.innerHTML = `<td class="seq">${l.id}</td><td>${l.type}</td><td>${l.amount}</td><td>${l.date}</td>`;
#     tbody.appendChild(tr);
#   });
# }

# // ---- Invoices list
# async function refreshInvoices(){
#   try {
#     const data = await api('/invoices_list');
#     const cont = document.getElementById('invoicesList');
#     cont.innerHTML = '';
#     data.forEach(f => {
#       const a = document.createElement('a');
#       a.href = '/invoices/'+f;
#       a.target = '_blank';
#       a.textContent = f;
#       a.style.display = 'inline-block';
#       a.style.marginRight = '8px';
#       cont.appendChild(a);
#     });
#   } catch(e){}
# }

# // ---- Analytics (Chart.js)
# let salesChart = null;
# async function refreshAnalytics(){
#   const a = await api('/sale_analytics');
#   const container = document.getElementById('analyticsText');
#   container.innerHTML = `<div>Total sales: <strong>${a.total_sales}</strong></div><div>Sales today: <strong>${a.sales_today}</strong></div><div>Total expenses: <strong>${a.total_expenses || a.total_expenses === 0 ? a.total_expenses : a.total_expenses}</strong></div>`;
#   const labels = Object.keys(a.items_sold || {});
#   const data = labels.map(k => a.items_sold[k]);
#   const ctx = document.getElementById('salesChart').getContext('2d');
#   if(salesChart) salesChart.destroy();
#   salesChart = new Chart(ctx, {
#     type: 'bar',
#     data: { 
#       labels, 
#       datasets: [{ 
#         label: 'Items sold (qty)', 
#         data,
#         backgroundColor: ['#4CAF50', '#2196F3', '#FFC107'],
#         borderColor: ['#388E3C', '#1976D2', '#FFA000'],
#         borderWidth: 1
#       }]
#     },
#     options: { 
#       responsive: true, 
#       maintainAspectRatio: false,
#       scales: { y: { beginAtZero: true } }
#     }
#   });
# }

# // ---- Backup
# async function manualBackup(){
#   const res = await api('/create_backup','POST', {});
#   if(res.status === 'success') alert('Backup created: '+res.backup_folder);
#   else alert('Backup failed');
# }
# function openBackups(){
#   alert('Backups folder on server: ' + '/backups/');
# }

# // ---- Rasa Chat Widget
# window.WebChat.default({
#   customData: { language: "ur" },
#   socketUrl: "http://localhost:5005",
#   title: "Urdu Sales Bot"
# }, null);

# // ---- Refresh all
# async function refreshAll(){
#   await refreshStocks();
#   await refreshLedger();
#   await refreshInvoices();
#   await refreshAnalytics();
# }

# // ---- Init
# async function init(){
#   addSaleRow();
#   await refreshAll();
# }
# init();

# </script>
# </body>
# </html>
# """

# @app.route("/")
# def index():
#     return render_template_string(INDEX_HTML)

# # ---------- Run ----------
# if __name__ == "__main__":
#     print("Starting Shop Dashboard app...")
#     print("Open http://127.0.0.1:5000 in your browser")
#     app.run(debug=True)







from flask import Flask, request, jsonify, render_template, redirect, url_for
import csv
import os
from collections import defaultdict
import datetime
import json

app = Flask(__name__)

# Hard-coded user for login
USER = {
    "username": "admin",
    "password": "1234"
}

# File paths
STOCK_FILE = "stocks.csv"
LEDGER_FILE = "ledger.csv"

# Ensure CSV files exist with headers
if not os.path.exists(STOCK_FILE):
    with open(STOCK_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["item", "quantity", "price"])

if not os.path.exists(LEDGER_FILE):
    with open(LEDGER_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "type", "name", "amount"])  
        # type = "supplier" / "customer"


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == USER["username"] and password == USER["password"]:
        return redirect(url_for('home'))
    else:
        return render_template('login.html', error="Invalid username or password!")


@app.route('/home')
def home():
    # Load stocks
    stocks = []
    with open(STOCK_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("item"):
                stocks.append(row)

    # Load ledger
    ledger = []
    with open(LEDGER_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("date"):
                ledger.append(row)

    # Calculate monthly profit from ledger
    monthly_profit = calculate_monthly_profit()

    return render_template(
        'home.html',
        stocks=stocks,
        ledger=ledger,
        monthly_profit=monthly_profit
    )


# -------- STOCK MANAGEMENT --------
@app.route('/add_stock', methods=['POST'])
def add_stock():
    item = request.form.get("item")
    quantity = request.form.get("quantity")
    price = request.form.get("price")

    if not item or not quantity or not price:
        return redirect(url_for("home"))

    with open(STOCK_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([item, quantity, price])

    return redirect(url_for("home"))


# -------- LEDGER MANAGEMENT --------
@app.route('/add_ledger', methods=['POST'])
def add_ledger():
    entry_type = request.form.get("type")  # supplier / customer
    name = request.form.get("name")
    amount = request.form.get("amount")
    today = datetime.date.today().strftime("%Y-%m-%d")

    if not entry_type or not name or not amount:
        return redirect(url_for("home"))

    with open(LEDGER_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([today, entry_type, name, amount])

    return redirect(url_for("home"))


# -------- PROFIT/LOSS GRAPH --------
@app.route('/profit_graph')
def profit_graph():
    monthly_profit = calculate_monthly_profit()
    monthly_profit_json = json.dumps(monthly_profit)  # safe JSON string
    return render_template("profit_graph.html", monthly_profit_json=monthly_profit_json)


# -------- Helper Function --------
def calculate_monthly_profit():
    monthly_profit = defaultdict(lambda: 0)

    with open(LEDGER_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("date") or row["date"] == "date":
                continue

            try:
                date = datetime.datetime.strptime(row["date"], "%Y-%m-%d")
                month = date.strftime("%B")
                amount = float(row["amount"])
            except Exception as e:
                print("Skipping invalid row:", row, e)
                continue

            if row["type"] == "customer":
                monthly_profit[month] += amount
            elif row["type"] == "supplier":
                monthly_profit[month] -= amount

    # Jan → Dec order
    months_order = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]
    return {m: monthly_profit[m] for m in months_order if m in monthly_profit}


if __name__ == "__main__":
    app.run(debug=True)
