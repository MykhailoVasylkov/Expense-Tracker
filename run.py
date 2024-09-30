# Used code snippet from Love Sandwich project
import gspread
from google.oauth2.service_account import Credentials
# Imported datetime module to working with dates and times.
import datetime   

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Expense Tracker').sheet1  # Open the first sheet

"""
Function to add a new expense
I used Chat-GPT to figure out how return back to the menu
I used https://docs.python.org/3/tutorial/errors.html to handle try except block
"""

def add_expense():
    while True:
        try:
            amount = input("\nEnter the expense amount or press 'm' to return to the menu: ")
            if amount.lower() == 'm':
                return
            amount = float(amount) #Convert to floating point number
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
        
        # I used Chat-GPT to figure out how collect date data using datetime module
        
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

# Empty list for expenses
expenses = [] 

# Function to load and view expenses with filtering options
def load_and_view_expenses():
    global expenses, SHEET
  
    try:
        # Get all records from Google Sheets
        rows = SHEET.get_all_records()
        if not rows:
            print("Google Sheets is empty or missing headers.")
            return
    
# Load all expenses from Google Sheets into the local list
        for row in rows:
            expense = {
                "amount": float(row["Amount"]),
                "category": row["Category"],
                "date": row["Date"]
            }
            expenses.append(expense)

        # Use loop for the menu
        while True:  
            print("\nFilter expenses:")
            print("1. By date")
            print("2. By category")
            print("3. Show all records")
            print("m. Return to the previous menu")
            filter_choice = input("Choose a filtering option (1-3 or 'm' to return to the menu): ")
            
            # I used Chat-GPT to implement filters
            if filter_choice == "1":
                # Input start date
                start_date_input = input("Enter start date (dd-mm-yyyy) or 'm' to return to the menu: ")
                if start_date_input.lower() == 'm':
                    break  
                try:
                    start_date = datetime.datetime.strptime(start_date_input, "%d-%m-%Y").date()
                except ValueError:
                    print("Error: Incorrect date format. Make sure to use dd-mm-yyyy.")
                    continue  

                # Input end date
                end_date_input = input("Enter end date (dd-mm-yyyy) or 'm' to return to the menu: ")
                if end_date_input.lower() == 'm':
                    break  
                try:
                    end_date = datetime.datetime.strptime(end_date_input, "%d-%m-%Y").date()
                except ValueError:
                    print("Error: Incorrect date format. Make sure to use dd-mm-yyyy.")
                    continue  

                # Filter expenses by entered dates
                filtered_expenses = filter_expenses_by_date(start_date, end_date)
            
            #Filtering by category
            elif filter_choice == "2":
                categories_dict = {
                    "1": "Food",
                    "2": "Transport",
                    "3": "Utilities",
                    "4": "Clothing",
                    "5": "Entertainment/Travel",
                    "6": "Health",
                    "7": "Other"
                }
                print("\nAvailable categories for filtering:")
                for key, value in categories_dict.items():
                    print(f"{key}. {value}")
                category_input = input("Choose a category (1-7) or 'm' to return to the menu: ")
                if category_input.lower() == 'm':
                    break 
                category = categories_dict.get(category_input)

                if not category:
                    print("Error: Invalid category input.")
                    continue 
                filtered_expenses = filter_expenses_by_category(category)
            
            # Display all or filtered expenses
            # Show all expenses
            elif filter_choice == "3":
                filtered_expenses = expenses  

            elif filter_choice.lower() == 'm':
                break 
            else:
                print("Invalid choice. Please choose '1', '2', '3' or 'm'.")
                continue 

            # Display filtered or all expenses
            if filtered_expenses:
                print("\nSelected expenses:")
                for expense in filtered_expenses:
                    print(f"Amount: {expense['amount']}, Category: {expense['category']}, Date: {expense['date']}")
            else:
                print("No expenses to display according to the filter.")
            input("\nPress Enter to return to the menu.")

    except Exception as e:
        print(f"Error loading data from Google Sheets: {e}")
        return

# Function to analyze expenses with filtering options
def analyze_expenses():
    if not expenses:
        print("No expenses for analysis. You need to download expenses.")
        return
    
    filtered_expenses_for_analyze = []

    while True:
        print("\nFilter expenses:")
        print("1. By date")
        print("2. By category")
        print("3. Analyze all records")
        print("m. Return to the menu")
        filter_choice = input("Choose a filtering option (1-3 or 'm' to return to the menu): ")

        # Analyze expenses by date
        if filter_choice == "1":
            try:
                start_date = datetime.datetime.strptime(input("Enter start date (dd-mm-yyyy) or 'm' to return to the menu: "), "%d-%m-%Y").date()
                end_date = datetime.datetime.strptime(input("Enter end date (dd-mm-yyyy) or 'm' to return to the menu: "), "%d-%m-%Y").date()
                filtered_expenses_for_analyze = filter_expenses_by_date(start_date, end_date)
            except ValueError:
                print("Error: Incorrect date format. Make sure to use dd-mm-yyyy.")
                continue

# Filtering functions for date and category
# Function to filter expenses by date
def filter_expenses_by_date(start_date, end_date):
    return [
        expense for expense in expenses
        if start_date <= datetime.datetime.strptime(expense['date'], "%d-%m-%Y").date() <= end_date
    ]

# Function to filter expenses by category
def filter_expenses_by_category(category):
    return [expense for expense in expenses if expense["category"] == category]      