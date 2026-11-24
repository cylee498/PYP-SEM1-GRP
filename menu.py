# MAIN SYSTEM LAUNCHER (menu.py) - FreshWash Laundry (LSMS)
import admin
import counter
import finance
import staff
import customer


def create_file_if_missing(filename, rows):
    try:
        file = open(filename, "r")
        file.close()
    except FileNotFoundError:
        file = open(filename, "w")
        for row in rows:
            file.write(row + "\n")
        file.close()


def seed_initial_files():
    create_file_if_missing("services.txt", [
        "SRV101|Wash & Dry|5.00",
        "SRV102|Ironing Only|3.50",
        "SRV103|Dry Cleaning|12.00"
    ])
    create_file_if_missing("customers.txt", [
        "CUS101|Ali Ahmad|0123456789",
        "CUS102|Mei Ling|0198765432"
    ])
    create_file_if_missing("orders.txt", [
        "ORD101|CUS101|SRV101|4.0|No|20.00|Pending|Paid|Uncollected|2025-05-12",
        "ORD102|CUS102|SRV103|2.0|Yes|36.00|Washing|Unpaid|Uncollected|2025-05-12"
    ])
    create_file_if_missing("payments.txt", [
        "PAY101|ORD101|20.00|QR|2025-05-12|Valid"
    ])
    create_file_if_missing("completed_services.txt", [])


def main_menu():
    seed_initial_files()

    while True:
        print("\n==============================================")
        print("   FRESHWASH LAUNDRY MANAGEMENT SYSTEM (LSMS)")
        print("==============================================")
        print("1. Laundry Administrator")
        print("2. Service Counter Officer")
        print("3. Finance Officer")
        print("4. Laundry Staff")
        print("5. Customer (5-Member Expanded Role)")
        print("0. Exit System")
        print("==============================================")
        choice = input("Select Role (0-5): ").strip()

        if choice == "1":
            admin.admin_menu()
        elif choice == "2":
            counter.counter_menu()
        elif choice == "3":
            finance.finance_menu()
        elif choice == "4":
            staff.staff_menu()
        elif choice == "5":
            customer.customer_menu()
        elif choice == "0":
            print("Thank you for using FreshWash LSMS. Goodbye!")
            break
        else:
            print("Invalid role choice.")


if __name__ == "__main__":
    main_menu()
