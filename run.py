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
    
    categories_dict = {
        "1": "Food",
        "2": "Transport",
        "3": "Utilities",
        "4": "Clothing",
        "5": "Entertainment/Travel",
        "6": "Health",
        "7": "Other"
    }

    while True:
        print("\nEnter the expense category or press 'm' to return to the menu:")
        for key, value in categories_dict.items():
            print(f"{key}. {value}")
        category_input = input("Choose a category (1-7): ")
        
        if category_input.lower() == 'm':
            return
        if category_input in categories_dict:
            category = categories_dict[category_input]
            break
        else:
            print("Error: Invalid category input. Enter a number from 1 to 7.")
        """
        I used Chat-GPT to figure out how collect date data using datetime module
        """
    while True:
        date_input = input("\nEnter the date (dd-mm-yyyy) or press Enter for today's date or 'm' to return to the menu: ")
        if date_input.lower() == 'm':
            return
        if date_input:
            try:
                date = datetime.datetime.strptime(date_input, "%d-%m-%Y").date()
                break
            except ValueError:
                print("Error: Incorrect date format. Use dd-mm-yyyy.")
        else:
            date = datetime.date.today().strftime("%d-%m-%Y")
            break

    SHEET.append_row([amount, category, str(date)])  # Add data to Google Sheets
    print("\nExpense added successfully!")

expenses = [] # Empty list for expenses

# Function to load and view expenses with filtering options
def load_and_view_expenses():
    global SHEET
  
    try:
        # Get all records from Google Sheets
        rows = SHEET.get_all_records() 
        if not rows:
            print("Google Sheets is empty or missing headers.")
            return
    except Exception as e:
        print(f"Error loading data from Google Sheets: {e}")
        return

# Load all expenses from Google Sheets into the local list
        for row in rows:
            expense = {
                "amount": float(row["Amount"]),
                "category": row["Category"],
                "date": row["Date"]
            }
            expenses.append(expense)   
