# Pharmacy Sales Manager

A complete web-based pharmacy management system built with **Flask**
and **SQLite**. Designed for small to medium-sized medical stores to handle daily operations including sales, 
inventory, invoicing, credit tracking, expense management, and business analytics — all from a single dashboard.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Author](#author)
- [License](#license)

---

## Features

### Dashboard
- Real-time overview of total revenue, sales count, stock items, and expenses
- Quick action buttons for fast navigation
- Auto-updating timestamp for last activity

### Stock Management
- Add new medicines/products with purchase and selling prices
- Track supplier (party) name and email
- Option to auto-add supplier credit when adding stock
- View complete inventory with all product details

### Sales & Invoicing
- Create new sales with multiple line items
- Auto-fetch product selling price from inventory
- Auto-calculate item totals and grand total
- Support for multiple payment types: **Cash**, **Credit**, **Card**
- Auto-generate unique invoice numbers (format: `INV + timestamp`)
- Auto-deduct sold quantities from stock
- Auto-add credit entry for credit-based sales
- Print-ready invoice with store branding

### Credit Management
- Track both **customer credits** (receivable) and **supplier credits** (payable)
- Auto-created from credit sales and stock purchases
- Summary cards showing total outstanding amounts
- Badge-based type indicators (Customer / Supplier)

### Ledger
- Split view: customer credits vs supplier credits
- Net credit position calculator (receivable - payable)
- Color-coded profit/loss indicator

### Expense Tracking
- Record expenses with predefined categories:
  - Office Supplies, Utilities, Rent, Marketing, Transportation, Equipment, Other
- Description field for detailed notes
- Running total of all expenses

### Analytics
- Revenue, sales count, stock levels, and expense totals
- Profit analysis with progress bar visualization
- Key metrics: average sale value, profit margin percentage
- Business insights with actionable recommendations

### Reports
- Generate filtered reports by type: **Sales**, **Stock**, **Expenses**
- Filter by period: **Daily**, **Monthly**, **Yearly**
- Dynamic table rendering based on report type
- Clean tabular output for easy reading

### Invoice Printing
- Professional print-ready invoice layout
- Store name and tagline header
- Customer details, itemized list, and grand total
- Print button with auto-hide (hidden during printing)
- Footer with store contact information

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3** | Backend programming language |
| **Flask** | Lightweight web framework |
| **SQLite** | Embedded relational database |
| **Jinja2** | Server-side HTML templating |
| **Bootstrap 5** | Responsive UI framework |
| **Font Awesome 6** | Icon library |
| **JavaScript (Vanilla)** | Frontend interactivity & AJAX calls |

---

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ikram-al-balushi/Pharmacy-Sales-Manager.git
   cd Pharmacy-Sales-Manager
   ```

2. **Install Flask**
   ```bash
   pip install flask
   ```

3. **Run the application**
   ```bash
   python "python sales_dashboard.py"
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

The database (`sales_dashboard.db`) will be automatically created on first run with all required tables.

---

## Usage Guide

### Adding Stock
1. Go to **Stock** page
2. Click **"Add Stock"** button
3. Fill in product name, quantity, purchase price, selling price
4. Optionally add supplier (party) name, email
5. Check **"Add to party credit"** if stock is purchased on credit
6. Click **Add Stock**

### Creating a Sale
1. Go to **Sales** page
2. Click **"New Sale"** button
3. Enter customer name (optional for walk-in customers)
4. Select payment type (Cash / Credit / Card)
5. Enter product name — selling price auto-fills from stock
6. Enter quantity — total auto-calculates
7. Click **"+"** to add more items
8. Click **"Create Sale"** to finalize

### Printing an Invoice
1. Go to **Sales** page
2. Click **"Print"** button next to any sale
3. Invoice opens in a new tab with print-ready layout
4. Click **"Print Invoice"** or use `Ctrl + P`

### Generating Reports
1. Go to **Reports** page
2. Select report type: Sales, Stock, or Expenses
3. Select period: Daily, Monthly, or Yearly
4. Click **"Generate Report"**
5. Results appear in a formatted table

---

## Project Structure

```
Pharmacy-Sales-Manager/
│
├── python sales_dashboard.py    # Main Flask application (routes, DB logic)
├── create_sample_data.py        # Sample data generator (commented out)
├── .gitignore                   # Git ignore rules
├── README.md                    # Project documentation
│
├── templates/                   # Jinja2 HTML templates
│   ├── base.html                # Base layout (navbar, Bootstrap, Font Awesome)
│   ├── dashboard.html           # Main dashboard with summary cards
│   ├── stock.html               # Stock management + Add Stock modal
│   ├── sales.html               # Sales list + New Sale modal
│   ├── analytics.html           # Business analytics & profit analysis
│   ├── reports.html             # Report generator (daily/monthly/yearly)
│   ├── credits.html             # Customer & supplier credit tracking
│   ├── expenses.html            # Expense management + Add Expense modal
│   ├── ledger.html              # Financial ledger with net position
│   └── print_invoice.html       # Print-ready invoice template
│
├── static/                      # Static assets
│   ├── style.css                # Custom CSS styles
│   └── logo.png                 # Store logo
│
├── ledger.csv                   # Ledger data export
├── stocks.csv                   # Stock data export
│
├── mini projecte/               # Earlier version of the project
└── projecte/                    # Alternate project version
```

---

## Database Schema

The application uses SQLite with 4 tables:

### `stock`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Auto-increment ID |
| product_name | TEXT | Medicine/product name |
| quantity | INTEGER | Available quantity |
| purchase_price | REAL | Cost price |
| selling_price | REAL | Retail price |
| supplier | TEXT | Supplier/party name |
| supplier_email | TEXT | Supplier email address |
| date_added | TEXT | Timestamp of entry |

### `sales`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Auto-increment ID |
| invoice_no | TEXT | Unique invoice number (INV + timestamp) |
| customer_name | TEXT | Customer name (nullable for walk-ins) |
| items | TEXT | JSON string of sold items |
| total_amount | REAL | Grand total of the sale |
| payment_type | TEXT | cash / credit / card |
| sale_date | TEXT | Timestamp of sale |

### `credits`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Auto-increment ID |
| type | TEXT | "customer" or "supplier" |
| name | TEXT | Person/company name |
| amount | REAL | Credit amount |
| description | TEXT | Details of the credit |
| date | TEXT | Timestamp of entry |

### `expenses`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Auto-increment ID |
| category | TEXT | Expense category |
| amount | REAL | Expense amount |
| description | TEXT | Details of the expense |
| date | TEXT | Timestamp of entry |

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Dashboard with summary cards |
| GET | `/stock` | View all stock items |
| POST | `/add_stock` | Add new stock item (JSON) |
| GET | `/get_product_price/<name>` | Get selling price of a product |
| GET | `/sales` | View all sales |
| POST | `/create_invoice` | Create new sale with invoice (JSON) |
| GET | `/print_invoice/<invoice_no>` | Print-ready invoice page |
| GET | `/analytics` | Business analytics page |
| GET | `/credits` | View all credits |
| GET | `/expenses` | View all expenses |
| POST | `/add_expense` | Add new expense (JSON) |
| GET | `/reports` | Reports page |
| POST | `/generate_report` | Generate filtered report (JSON) |
| GET | `/ledger` | Financial ledger page |

---

## Screenshots

> Screenshots will be added here

---

## Author

**Ikram Al Balushi**

- GitHub: [@ikram-al-balushi](https://github.com/ikram-al-balushi)

---

## License

This project is open source and available for personal and educational use.
