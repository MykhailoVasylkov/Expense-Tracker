# Used code snippet from Love Sandwich project
import gspread
from google.oauth2.service_account import Credentials
import datetime # Imported datetime module to working with dates and times.  

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Expense Tracker').sheet1  # Open the first sheet

data = SHEET.get_all_values()
print(data)