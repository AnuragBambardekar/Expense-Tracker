import sqlite3
import datetime
import csv
import pandas as pd

conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

def enter_new_expense():
    date = input("Enter the date of the expense (YYYY-MM-DD): ")
    description = input("Enter the description of the expense: ")

    cur.execute("SELECT DISTINCT category FROM expenses")
    categories = cur.fetchall()

    print("Select a category by number: ")
    for idx, category in enumerate(categories):
        print(f"{idx + 1}. {category[0]}")
    print(f"{len(categories) + 1}. Create a new category")

    category_choice = int(input())
    if category_choice == len(categories) + 1:
        category = input("Enter the new category name: ")
    else:
        category = categories[category_choice - 1][0]

    price = input("Enter the price of the expense: ")

    cur.execute("INSERT INTO expenses (Date, description, category, price) VALUES (?, ?, ?, ?)", (date, description, category, price))
    conn.commit()

def view_all_expenses():
    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()
    for expense in expenses:
        print(expense)

def view_monthly_expenses():
    month = input("Enter the month (MM): ")
    year = input("Enter the year (YYYY): ")

    cur.execute("SELECT category, SUM(price) FROM expenses WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ? GROUP BY category", (month, year))

    expenses = cur.fetchall()
    for expense in expenses:
        print(f"Category: {expense[0]}, Total: {expense[1]}")

def modify_expense():
    expense_id = input("Enter the ID of the expense you want to modify: ")

    cur.execute("SELECT * FROM expenses WHERE ID = ?", (expense_id,))
    expense = cur.fetchone()

    if expense:
        print(f"Expense ID: {expense[0]}")
        print(f"Date: {expense[1]}")
        print(f"Description: {expense[2]}")
        print(f"Category: {expense[3]}")
        print(f"Price: {expense[4]}")

        print("Select an option:")
        print("1. Edit expense")
        print("2. Delete expense")

        choice = int(input())

        if choice == 1:
            date = input("Enter the updated date (YYYY-MM-DD): ")
            description = input("Enter the updated description: ")
            category = input("Enter the updated category: ")
            price = input("Enter the updated price: ")

            cur.execute("UPDATE expenses SET Date = ?, description = ?, category = ?, price = ? WHERE ID = ?", (date, description, category, price, expense_id))
            conn.commit()

            print("Expense updated successfully!")
        elif choice == 2:
            cur.execute("DELETE FROM expenses WHERE ID = ?", (expense_id,))
            conn.commit()

            print("Expense deleted successfully!")
        else:
            print("Invalid choice.")
    else:
        print("Expense not found.")

def filter_expenses():
    print("Select a filtering option:")
    print("1. Filter by date range")
    print("2. Filter by category")
    print("3. Filter by price range")

    choice = int(input())

    if choice == 1:
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")

        cur.execute("SELECT * FROM expenses WHERE Date BETWEEN ? AND ?", (start_date, end_date))
        expenses = cur.fetchall()
        for expense in expenses:
            print(expense)
    elif choice == 2:
        cur.execute("SELECT DISTINCT category FROM expenses")
        categories = cur.fetchall()

        print("Select a category by number: ")
        for idx, category in enumerate(categories):
            print(f"{idx + 1}. {category[0]}")

        category_choice = int(input())
        selected_category = categories[category_choice - 1][0]

        cur.execute("SELECT * FROM expenses WHERE category = ?", (selected_category,))
        expenses = cur.fetchall()
        for expense in expenses:
            print(expense)
    elif choice == 3:
        min_price = float(input("Enter the minimum price: "))
        max_price = float(input("Enter the maximum price: "))

        cur.execute("SELECT * FROM expenses WHERE price BETWEEN ? AND ?", (min_price, max_price))
        expenses = cur.fetchall()
        for expense in expenses:
            print(expense)
    else:
        print("Invalid choice.")

def calculate_total_expenses():
    cur.execute("SELECT SUM(price) FROM expenses")
    total_expenses = cur.fetchone()[0]
    print(f"Total Expenses: {total_expenses}")

def calculate_average_expense():
    cur.execute("SELECT AVG(price) FROM expenses")
    average_expense = cur.fetchone()[0]
    print(f"Average Expense: {average_expense}")

def calculate_max_expense():
    cur.execute("SELECT MAX(price) FROM expenses")
    max_expense = cur.fetchone()[0]
    print(f"Maximum Expense: {max_expense}")

def calculate_min_expense():
    cur.execute("SELECT MIN(price) FROM expenses")
    min_expense = cur.fetchone()[0]
    print(f"Minimum Expense: {min_expense}")


def export_to_csv():
    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()

    filename = input("Enter the filename for the CSV export (e.g., expenses.csv): ")

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Date', 'Description', 'Category', 'Price'])
        writer.writerows(expenses)

    print(f"Expense data exported to {filename} successfully!")

def export_to_excel():
    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()

    filename = input("Enter the filename for the Excel export (e.g., expenses.xlsx): ")

    df = pd.DataFrame(expenses, columns=['ID', 'Date', 'Description', 'Category', 'Price'])
    df.to_excel(filename, index=False)

    print(f"Expense data exported to {filename} successfully!")

def import_from_csv():
    filename = input("Enter the filename of the CSV file to import: ")

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            expense_id, date, description, category, price = row
            cur.execute("INSERT INTO expenses (ID, Date, description, category, price) VALUES (?, ?, ?, ?, ?)",
                        (expense_id, date, description, category, price))

        conn.commit()

    print(f"Expense data imported from {filename} successfully!")


while True:
    print("Select an option:")
    print("1. Enter a new expense")
    print("2. View expenses summary")
    print("3. Modify an expense")
    print("4. Filter expenses")
    print("5. Calculate expense statistics")
    print("6. Export expense data")
    print("7. Import expense data")

    choice = int(input())

    if choice == 1:
        enter_new_expense()
    elif choice == 2:
        print("Select an option: ")
        print("1. View all expenses")
        print("2. View monthly expenses by category")

        view_choices = int(input())

        if view_choices == 1:
            view_all_expenses()
        elif view_choices == 2:
            view_monthly_expenses()
        else:
            print("Invalid choice.")
    elif choice == 3:
        modify_expense()
    elif choice == 4:
        filter_expenses()
    elif choice == 5:
        calculate_total_expenses()
        calculate_average_expense()
        calculate_max_expense()
        calculate_min_expense()
    elif choice == 6:
        print("Select an export option:")
        print("1. Export to CSV")
        print("2. Export to Excel")

        export_choice = int(input())

        if export_choice == 1:
            export_to_csv()
        elif export_choice == 2:
            export_to_excel()
        else:
            print("Invalid choice.")
    elif choice == 7:
        import_from_csv()
    else:
        print("Invalid choice.")

    repeat = input("Would you like to do something else? (y/n)\n")
    if repeat.lower() != "y":
        break

conn.close()
