# Expense Tracker

**Expense Tracker** is a Python terminal application that helps users manage and analyze their expenses by integrating with Google Sheets. It allows users to add expenses, filter them by category or date, and analyze their spending.

[Here is the live version of my project](https://expense-tracker-project-2d005a9072a1.herokuapp.com/)
![ ](assets/photos/am_i_responsive.jpg)
## How to Use

The Expense Tracker is designed to simplify expense tracking by offering easy-to-use options for adding, viewing, and analyzing expenses.

### Main Features:
- **Add Expenses**: Users can add new expenses by entering the amount, category, and date.
- **View Expenses**: Users can load expenses from Google Sheets and filter them by date or category.
- **Analyze Expenses**: The program offers an analysis of total expenses and expenses by category.
- **Google Sheets Integration**: All data is stored in a Google Sheets document for easy access and persistent storage.

## Features

### Existing Features
- **Add Expense**: Input the amount, category, and date of the expense. Input validation ensures correct data format.
- **View Expenses**: Load all expenses from Google Sheets and filter them by date or category.
- **Analyze Expenses**: Get total expenses and break down expenses by category.
- **Google Sheets Integration**: Expenses are stored in a Google Sheet, and the app uses the `gspread` library for interaction.
- **Error Handling**: The app uses try-except blocks to manage errors like incorrect date formats or invalid inputs.

### Future Features
- Allow users to edit or delete expenses.
- Add more robust filtering and analysis options (e.g., filtering by price range, a mix of filters).

## Data Model

This project uses Google Sheets as the primary data store. Each expense consists of:
- **Amount**: The cost of the expense.
- **Category**: The type of expense (e.g., Food, Transport, Utilities).
- **Date**: The date the expense was incurred.

The app interacts with Google Sheets using the `gspread` library. Data is read from and written to a Google Sheet, where each row contains an individual expense record.

## Testing

This project was manually tested by:
- Passed the code trought a PEP8 linter without problems.
- Adding, viewing, and analyzing expenses in both local and Heroku terminals.
- Using valid and invalid inputs to test the input validation.
- Testing the Google Sheets integration with both empty and populated sheets.

### Solved Bugs
- During manual testing, it was found that when selecting an expense category, an error occurred due to incorrect indentation of the categories_dict dictionary. I fixed the indentation.
- In the analyze_expenses function, I did not initialize an empty list to store the filtered expenses, which caused an UnboundLocalError. I fixed this by initializing the filtered_expenses_analyze list.

### Remaining Bugs
- No known bugs remain at this time.

## Validator Testing
- **PEP8**: The project code has been checked using PEP8 linter, with no issues reported.

## Deployment

This project was deployed using Code Institute's mock terminal for Heroku, following these steps:
1. Create a new Heroku app.
2. Add config vars
3. Set the buildbacks to `Python` and `Node.js` in this order.
4. Link the Heroku app to the GitHub repository.
5. Click "Deploy".

## Credits
- **gspread**: Library used for Google Sheets integration.
- **Google Developers**: For OAuth2 credentials and Google Sheets API.
- **PEP8**: For code validation and linting.
- **https://docs.python.org/3/tutorial/errors.html**: To handle try and except statements
- **Chat-GPT**: I used it for all the questions I needed to solve.