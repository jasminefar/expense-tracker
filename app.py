import os
import json
from datetime import datetime

EXPENSES_FILE = 'expenses.json'

class ExpenseManager:
    def __init__(self):
        """Initialize the ExpenseManager and load expenses from file."""
        self.expenses = []
        self.load_expenses()

    def load_expenses(self):
        """Load expenses from a JSON file if it exists."""
        if os.path.exists(EXPENSES_FILE):
            with open(EXPENSES_FILE, 'r') as file:
                self.expenses = json.load(file)
        else:
            print("No expenses file found. Starting with an empty expenses list.")

    def save_expenses(self):
        """Save the current expenses to a JSON file."""
        with open(EXPENSES_FILE, 'w') as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self, description, amount, category, date):
        """Add a new expense with a description, amount, category, and date."""
        try:
            expense = {
                'id': len(self.expenses) + 1,
                'description': description,
                'amount': amount,
                'category': category,
                'date': date,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.expenses.append(expense)
            self.save_expenses()
            print(f"Expense added: '{description}' of amount {amount} in category '{category}' on '{date}'.")
        except Exception as e:
            print(f"Failed to add expense: {e}")

    def list_expenses(self):
        """List all expenses with their details."""
        if not self.expenses:
            print("No expenses found. Your expenses list is empty.")
            return
        for expense in self.expenses:
            print(f"Expense ID: {expense['id']}\n"
                  f"Description: {expense['description']}\n"
                  f"Amount: {expense['amount']}\n"
                  f"Category: {expense['category']}\n"
                  f"Date: {expense['date']}\n"
                  f"Created At: {expense['created_at']}\n")

    def edit_expense(self, expense_id, description=None, amount=None, category=None, date=None):
        """Edit an existing expense by its ID."""
        try:
            for expense in self.expenses:
                if expense['id'] == expense_id:
                    if description:
                        expense['description'] = description
                    if amount:
                        expense['amount'] = amount
                    if category:
                        expense['category'] = category
                    if date:
                        expense['date'] = date
                    self.save_expenses()
                    print(f"Expense ID {expense_id} updated.")
                    return
            print(f"Expense ID {expense_id} not found.")
        except Exception as e:
            print(f"Failed to edit expense: {e}")

    def delete_expense(self, expense_id):
        """Delete an expense by its ID."""
        try:
            self.expenses = [expense for expense in self.expenses if expense['id'] != expense_id]
            self.save_expenses()
            print(f"Expense ID {expense_id} deleted.")
        except Exception as e:
            print(f"Failed to delete expense: {e}")

    def monthly_report(self, month, year):
        """Generate a report of expenses for a specific month and year."""
        try:
            month_str = f"{year}-{month:02d}"
            monthly_expenses = [expense for expense in self.expenses if expense['date'].startswith(month_str)]
            if not monthly_expenses:
                print(f"No expenses found for {month_str}.")
                return
            total_amount = sum(expense['amount'] for expense in monthly_expenses)
            print(f"Monthly Report for {month_str}:\nTotal Amount Spent: {total_amount}")
            for expense in monthly_expenses:
                print(f"Description: {expense['description']}, Amount: {expense['amount']}, Date: {expense['date']}")
        except Exception as e:
            print(f"Failed to generate monthly report: {e}")

    def category_report(self, category):
        """Generate a report of expenses for a specific category."""
        try:
            category_expenses = [expense for expense in self.expenses if expense['category'].lower() == category.lower()]
            if not category_expenses:
                print(f"No expenses found in category '{category}'.")
                return
            total_amount = sum(expense['amount'] for expense in category_expenses)
            print(f"Category Report for '{category}':\nTotal Amount Spent: {total_amount}")
            for expense in category_expenses:
                print(f"Description: {expense['description']}, Amount: {expense['amount']}, Date: {expense['date']}")
        except Exception as e:
            print(f"Failed to generate category report: {e}")

def main():
    expense_manager = ExpenseManager()

    while True:
        print("\nExpense Tracker\n")
        print("1. Add Expense")
        print("2. List All Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. View Monthly Report")
        print("6. View Category Report")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            description = input("Enter expense description: ")
            amount = float(input("Enter expense amount: "))
            category = input("Enter expense category: ")
            date = input("Enter expense date (YYYY-MM-DD): ")
            expense_manager.add_expense(description, amount, category, date)
        elif choice == '2':
            expense_manager.list_expenses()
        elif choice == '3':
            expense_id = int(input("Enter expense ID to edit: "))
            description = input("Enter new description (leave blank to keep current): ")
            amount = input("Enter new amount (leave blank to keep current): ")
            category = input("Enter new category (leave blank to keep current): ")
            date = input("Enter new date (leave blank to keep current): ")
            expense_manager.edit_expense(
                expense_id,
                description if description else None,
                float(amount) if amount else None,
                category if category else None,
                date if date else None
            )
        elif choice == '4':
            expense_id = int(input("Enter expense ID to delete: "))
            expense_manager.delete_expense(expense_id)
        elif choice == '5':
            month = int(input("Enter month (1-12): "))
            year = int(input("Enter year (e.g., 2024): "))
            expense_manager.monthly_report(month, year)
        elif choice == '6':
            category = input("Enter category: ")
            expense_manager.category_report(category)
        elif choice == '7':
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
