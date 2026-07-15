from flask import Flask, request, jsonify, render_template, redirect, url_for
import csv
import os
from collections import defaultdict
import datetime
import json

 app = Flask(__name__)


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
