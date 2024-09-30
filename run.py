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
Function to add a new expense.
I used Chat-GPT to figure out how return back to the menu.
I used https://docs.python.org/3/tutorial/errors.html to handle try except
block.
"""


def add_expense():
    while True:
        try:
            amount = input(
                f"Enter the expense amount"
                f" or press 'm' to return to the menu:\n"
            )
            if amount.lower() == 'm':
                return
            amount = float(amount)  # Convert to floating point number
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
        print(
            "\nEnter the expense category or press 'm' to return to the menu:"
            )
        for key, value in categories_dict.items():
            print(f"{key}. {value}")
        category_input = input("Choose a category (1-7):\n")

        if category_input.lower() == 'm':
            return
        if category_input in categories_dict:
            category = categories_dict[category_input]
            break
        else:
            print("Error: Invalid category input. Enter a number from 1 to 7.")

        """
        I used Chat-GPT to figure out how collect date data using
        datetime module
        """

    while True:
        date_input = input(
            f"Enter the date (dd-mm-yyyy) or press Enter for today's"
            f" date or 'm' to return to the menu:\n")
        if date_input.lower() == 'm':
            return
        if date_input:
            try:
                date = datetime.datetime.strptime(date_input, "%d-%m-%Y")
                date = date.date()
                break
            except ValueError:
                print("Error: Incorrect date format. Use dd-mm-yyyy.")
        else:
            date = datetime.date.today().strftime("%d-%m-%Y")
            break

    # Add data to Google Sheets
    SHEET.append_row([amount, category, str(date)])
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
            filter_choice = input(
                f"Choose a filtering option"
                f"(1-3 or 'm' to return to the menu):"
                )

            # I used Chat-GPT to implement filters
            if filter_choice == "1":
                # Input start date
                start_date_input = input(
                    f"Enter start date (dd-mm-yyyy)"
                    f" or 'm' to return to the menu:\n"
                    )
                if start_date_input.lower() == 'm':
                    break
                try:
                    s_date = datetime.datetime.strptime(
                        start_date_input, "%d-%m-%Y"
                        )
                    s_date = s_date.date()
                except ValueError:
                    print(
                        f"Error: Incorrect date format."
                        f" Make sure to use dd-mm-yyyy."
                        )
                    continue

                # Input end date
                end_date_input = input(
                    f"Enter end date (dd-mm-yyyy)"
                    f" or 'm' to return to the menu:\n")
                if end_date_input.lower() == 'm':
                    break
                try:
                    end_date = datetime.datetime.strptime(
                               end_date_input, "%d-%m-%Y"
                               ).date()
                except ValueError:
                    print(
                        f"Error: Incorrect date format."
                        f" Make sure to use dd-mm-yyyy."
                        )
                    continue

                # Filter expenses by entered dates
                filtered_expenses = filter_expenses_by_date(s_date, end_date)

            # Filtering by category
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
                category_input = input(
                    f"Choose a category (1-7)"
                    f" or 'm' to return to the menu:\n"
                    )
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
                    print(
                         f"Amount: {expense['amount']}, "
                         f"Category: {expense['category']}, "
                         f"Date: {expense['date']}"
                         )

            else:
                print("No expenses to display according to the filter.")
            input("\nPress Enter to return to the menu.\n")

    except Exception as e:
        print(f"Error loading data from Google Sheets: {e}")
        return


# Function to analyze expenses with filtering options
def analyze_expenses():
    if not expenses:
        print("No expenses for analysis. You need to download expenses.")
        return

    filtered_expenses_analyze = []

    while True:
        print("\nFilter expenses:")
        print("1. By date")
        print("2. By category")
        print("3. Analyze all records")
        print("m. Return to the menu")
        filter_choice = input(
                        f"Choose a filtering option"
                        f" (1-3 or 'm' to return to the menu):\n"
                        )

        # Analyze expenses by date
        if filter_choice == "1":
            try:
                start_date = datetime.datetime.strptime(input(
                    f"Enter start date (dd-mm-yyyy)"
                    f" or 'm' to return to the menu:\n"), "%d-%m-%Y").date()
                end_date = datetime.datetime.strptime(input(
                    f"Enter end date (dd-mm-yyyy)"
                    f" or 'm' to return to the menu:\n"), "%d-%m-%Y").date()
                filtered_expenses_analyze = filter_expenses_by_date(
                    start_date, end_date
                )
            except ValueError:
                print(
                    f"Error: Incorrect date format."
                    f" Make sure to use dd-mm-yyyy."
                    )
                continue

        # Analyze expenses by category
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
            category_input = input(
                f"Choose a category (1-7)"
                f" or 'm' to return to the menu:\n"
                )
            if category_input.lower() == 'm':
                return
            category = categories_dict.get(category_input)

            if not category:
                print("Error: Invalid category input.")
                continue
            filtered_expenses_analyze = filter_expenses_by_category(category)

        # Analyze all expenses
        elif filter_choice == "3":
            filtered_expenses_analyze = expenses

        elif filter_choice.lower() == 'm':
            return
        else:
            print("Invalid choice. Please choose '1', '2', '3' or 'm'.")
            continue

        # Analyzing filtered or all expenses
        if filtered_expenses_analyze:
            total = sum(
                [expense['amount'] for expense in filtered_expenses_analyze]
                )
            print(f"\nTotal expenses: {total}")

            # Analyze expenses by category
            categories = {}
            for expense in filtered_expenses_analyze:
                categories[expense["category"]] = categories.get(
                    expense["category"], 0
                    ) + expense["amount"]

            print("\nAnalysis by category:")
            for category, amount in categories.items():
                print(f"{category}: {amount}")
        else:
            print("No expenses to analyze according to the filter.")
        input("\nPress Enter to return to the menu.\n")


# Filtering functions for date and category
# Function to filter expenses by date
def filter_expenses_by_date(start_date, end_date):
    return [
        expense for expense in expenses
        if start_date <= datetime.datetime.strptime(
            expense['date'], "%d-%m-%Y"
            ).date() <= end_date
    ]


# Function to filter expenses by category
def filter_expenses_by_category(category):
    return [expense for expense in expenses if expense["category"] == category]


# Main menu function
def main_menu():
    while True:
        print("\n----- Expense Tracker Menu -----")
        print("1. Add Expense")
        print("2. Load and View Expenses")
        print("3. Analyze Expenses")
        print("m. Exit")
        choice = input("Choose an action (1-3 or 'm' to exit): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            load_and_view_expenses()
        elif choice == "3":
            analyze_expenses()
        elif choice.lower() == 'm':
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please try again.")


# Run the application
main_menu()
