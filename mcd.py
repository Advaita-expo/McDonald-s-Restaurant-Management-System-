
import mysql.connector
import csv


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password_here",
    database="mcdonalds"
)

cursor = conn.cursor()

def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS managers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ManagerName VARCHAR(255) NOT NULL,
            Password VARCHAR(255) NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            EmployeeName VARCHAR(255) NOT NULL,
            Role VARCHAR(255) NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ItemName VARCHAR(255) NOT NULL,
            Price DECIMAL(10, 2) NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ItemName VARCHAR(255) NOT NULL,
            Quantity INT NOT NULL,
            Total DECIMAL(10, 2) NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            EmployeeName VARCHAR(255) NOT NULL,
            Amount DECIMAL(10, 2) NOT NULL
        )
    ''')

    conn.commit()

def sign_up_manager():
    print("\n=== New Manager Registration ===")
    u = input("Enter Manager Name: ")
    p = input("Enter Password: ")
    cursor.execute("INSERT INTO managers (ManagerName, Password) VALUES (%s, %s)", (u, p))
    conn.commit()
    print(f"\nManager {u} successfully registered.\n")

def login_manager():
    print("\n=== Manager Login ===")
    un = input("Username: ")
    ps = input("Password: ")
    cursor.execute("SELECT * FROM managers WHERE ManagerName = %s AND Password = %s", (un, ps))
    manager = cursor.fetchone()
    if manager:
        while True:
            print("""
            === Manager Menu ===
            1. Employee Management
            2. Menu Management
            3. Order Management
            4. Transactions
            5. Sign Out
            """)
            choice = input("Enter your choice: ")
            if choice == "1":
                employee_management_menu()
            elif choice == "2":
                menu_management_menu()
            elif choice == "3":
                order_management_menu()
            elif choice == "4":
                transaction_menu()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Invalid manager credentials. Please try again.")

def employee_management_menu():
    while True:
        print("""
        === Employee Management ===
        1. Show Employees
        2. Add Employee
        3. Remove Employee
        4. Back
        """)
        choice = input("Enter your choice: ")
        if choice == "1":
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()
            for employee in employees:
                print(employee)
        elif choice == "2":
            name = input("Enter employee name: ")
            role = input("Enter employee role: ")
            cursor.execute("INSERT INTO employees (EmployeeName, Role) VALUES (%s, %s)", (name, role))
            conn.commit()
            print(f"\nEmployee {name} added successfully.\n")
        elif choice == "3":
            name = input("Enter employee name to remove: ")
            cursor.execute("DELETE FROM employees WHERE EmployeeName = %s", (name,))
            if cursor.rowcount > 0:
                conn.commit()
                print(f"\nEmployee {name} removed successfully.\n")
            else:
                print(f"\nEmployee {name} not found.\n")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def menu_management_menu():
    while True:
        print("""
        === Menu Management ===
        1. Show Menu Items
        2. Add Menu Item
        3. Remove Menu Item
        4. Back
        """)
        choice = input("Enter your choice: ")
        if choice == "1":
            cursor.execute("SELECT * FROM menu_items")
            menu_items = cursor.fetchall()
            for item in menu_items:
                print(item)
        elif choice == "2":
            item_name = input("Enter menu item name: ")
            price = float(input("Enter item price: "))
            cursor.execute("INSERT INTO menu_items (ItemName, Price) VALUES (%s, %s)", (item_name, price))
            conn.commit()
            print(f"\nMenu item {item_name} added successfully.\n")
        elif choice == "3":
            item_name = input("Enter menu item name to remove: ")
            cursor.execute("DELETE FROM menu_items WHERE ItemName = %s", (item_name,))
            if cursor.rowcount > 0:
                conn.commit()
                print(f"\nMenu item {item_name} removed successfully.\n")
            else:
                print(f"\nMenu item {item_name} not found.\n")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def order_management_menu():
    while True:
        print("""
        === Order Management ===
        1. Show Orders
        2. Add Order
        3. Back
        """)
        choice = input("Enter your choice: ")
        if choice == "1":
            cursor.execute("SELECT * FROM orders")
            orders = cursor.fetchall()
            for order in orders:
                print(order)
        elif choice == "2":
            item_name = input("Enter item name: ")
            quantity = int(input("Enter quantity: "))
            total = float(input("Enter total amount: "))
            cursor.execute("INSERT INTO orders (ItemName, Quantity, Total) VALUES (%s, %s, %s)", (item_name, quantity, total))
            conn.commit()
            print("\nOrder added successfully.\n")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def transaction_menu():
    while True:
        print("""
        === Transaction Management ===
        1. Show Transactions
        2. Add Transaction
        3. Back
        """)
        choice = input("Enter your choice: ")
        if choice == "1":
            cursor.execute("SELECT * FROM transactions")
            transactions = cursor.fetchall()
            for transaction in transactions:
                print(transaction)
        elif choice == "2":
            employee_name = input("Enter employee name: ")
            amount = float(input("Enter transaction amount: "))
            cursor.execute("INSERT INTO transactions (EmployeeName, Amount) VALUES (%s, %s)", (employee_name, amount))
            conn.commit()
            print("\nTransaction added successfully.\n")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def admin_login():
    print("\n=== Admin Login ===")
    un = input("Admin Username: ")
    ps = input("Admin Password: ")
    if un == "admin" and ps == "mcdonalds":
        while True:
            print("""
            === Admin Menu ===
            1. Show Managers
            2. Show All Transactions
            3. Back
            """)
            choice = input("Enter your choice: ")
            if choice == "1":
                cursor.execute("SELECT * FROM managers")
                managers = cursor.fetchall()
                for manager in managers:
                    print(manager)
            elif choice == "2":
                cursor.execute("SELECT * FROM transactions")
                transactions = cursor.fetchall()
                for transaction in transactions:
                    print(transaction)
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Invalid admin credentials. Please try again.")

if __name__ == "__main__":
    create_tables()

    while True:
        print("""
        === Welcome to McDonald's Management System ===
        1. Manager Login
        2. Admin Login
        3. Sign Up Manager
        4. Exit
        """)
        option = input("Enter your choice: ")

        if option == "1":
            login_manager()
        elif option == "2":
            admin_login()
        elif option == "3":
            sign_up_manager()
        elif option == "4":
            print("Exiting McDonald's Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
