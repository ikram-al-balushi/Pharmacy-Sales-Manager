# create_sample_data.py

# import sqlite3

# # DB connect (agar file nahi hai to nayi ban jayegi)
# conn = sqlite3.connect("shop.db")
# cursor = conn.cursor()

# # Stock Table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS stock (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT,
#     quantity INTEGER,
#     price REAL,
#     date_added TEXT
# )
# """)

# # Sale Table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS sales (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     item TEXT,
#     quantity INTEGER,
#     total_price REAL,
#     date TEXT
# )
# """)

# # Ledger Table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS ledger (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     person TEXT,
#     amount REAL,
#     type TEXT,
#     date TEXT
# )
# """)

# # Expense Table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS expenses (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     category TEXT,
#     amount REAL,
#     date TEXT
# )
# """)

# # Sample Stock Insert
# cursor.execute("INSERT INTO stock (name, quantity, price, date_added) VALUES ('Item A', 10, 50, '2025-09-01')")
# cursor.execute("INSERT INTO stock (name, quantity, price, date_added) VALUES ('Item B', 20, 30, '2025-09-01')")

# # Sample Sale Insert
# cursor.execute("INSERT INTO sales (item, quantity, total_price, date) VALUES ('Item A', 2, 100, '2025-09-01')")

# # Sample Ledger Insert
# cursor.execute("INSERT INTO ledger (person, amount, type, date) VALUES ('Supplier X', 500, 'credit', '2025-09-01')")

# # Sample Expense Insert
# cursor.execute("INSERT INTO expenses (category, amount, date) VALUES ('Electricity', 200, '2025-09-01')")

# conn.commit()
# conn.close()

# print("✅ shop.db created with sample data!")




# import os
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload


# def upload_to_gdrive(filepath, credentials_json_path, folder_id=None):
#     """
#     Google Drive par file upload karne ka function.
#     :param filepath: Upload karni wali file ka path
#     :param credentials_json_path: Service account JSON file ka path
#     :param folder_id: Google Drive folder ki ID (optional)
#     :return: True agar upload success ho gaya, warna False
#     """
#     # ✅ Check file exists
#     if not os.path.exists(filepath):
#         print(f"❌ File nahi mili: {filepath}")
#         return False

#     # ✅ Check credentials JSON exists
#     if not credentials_json_path or not os.path.exists(credentials_json_path):
#         print(f"❌ Service Account JSON nahi mila: {credentials_json_path}")
#         return False

#     try:
#         # ✅ Required Google Drive API scope
#         SCOPES = ["https://www.googleapis.com/auth/drive.file"]

#         # ✅ Load service account credentials
#         creds = service_account.Credentials.from_service_account_file(
#             credentials_json_path, scopes=SCOPES
#         )

#         # ✅ Build Google Drive service
#         service = build("drive", "v3", credentials=creds)

#         # ✅ File metadata (naam & folder)
#         metadata = {"name": os.path.basename(filepath)}
#         if folder_id:
#             metadata["parents"] = [folder_id]  # Upload in given folder

#         # ✅ Prepare file for upload
#         media = MediaFileUpload(filepath, resumable=True)

#         # ✅ Upload request
#         uploaded_file = service.files().create(
#             body=metadata, media_body=media, fields="id"
#         ).execute()

#         print(f"✅ Upload ho gaya! File ID: {uploaded_file.get('id')}")
#         return True

#     except Exception as e:
#         print(f"⚠️ Error: {e}")
#         return False


# # ========================
# # 👇 Example usage
# # ========================
# if __name__ == "__main__":
#     # 🔑 Tumhara service account JSON file ka naam
#     credentials_path = "service_account.json"

#     # 📄 Upload karne wali file
#     file_to_upload = "test.pdf"

#     # 📂 Tumhare folder ka ID (yahan apna folder ID daalo)
#     folder_id = "1Jiv661-J8Pp3HqjiVLfqnSrlNNFNMVLg"

#     upload_to_gdrive(file_to_upload, credentials_path, folder_id)





# # Install PyDrive first:
# # pip install pydrive

# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive

# # 🔑 Authenticate
# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()  # Login link open karega

# drive = GoogleDrive(gauth)

# # 📄 File upload
# file_path = "test.pdf"
# gfile = drive.CreateFile({'title': 'test.pdf'})
# gfile.SetContentFile(file_path)
# gfile.Upload()

# print("✅ File uploaded successfully!")













# import pywhatkit as kit
# import datetime

# # Number international format me likhein
# phone_number = "+923368552677"
# message = "Hello! This is a test message from PyWhatKit."

# # Send time (current time + 1 min)
# now = datetime.datetime.now()
# hour = now.hour
# minute = now.minute + 1

# # Send WhatsApp message
# kit.sendwhatmsg(phone_number, message, hour, minute)



# import pywhatkit as kit

# # ✅ WhatsApp number with country code
# phone_number = "+923323133978"  # Apna number yahan likhein

# # ✅ Message text
# message = "Hello zeba how are you , your oddr was submit"

# # ✅ Send message instantly
# try:
#     kit.sendwhatmsg_instantly(phone_number, message)
#     print("✅ Message sent successfully!")
# except Exception as e:
#     print(f"❌ Error: {e}")


