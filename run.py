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

# Function to add a new expense
# I used Chat-GPT to figure out how return back to the menu
# I used https://docs.python.org/3/tutorial/errors.html to handle try except block

def add_expense():
    while True:
        try:
            amount = input("\nEnter the expense amount or press 'm' to return to the menu: ")
            if amount.lower() == 'm':
                return
            amount = float(amount) #Conver to floating point number
            if amount <= 0:
                print("Error: Amount must be a positive number.")
                continue
            break
        except ValueError:
            print("Error: Please enter a numeric value for the amount.")

    SHEET.append_row([amount])  # Add data to Google Sheets
    print("\nExpense added successfully!")

add_expense()
