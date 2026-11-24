# ROLE 3: FINANCE OFFICER (finance.py)
SEP = "|"


def load_file(filename):
    rows = []
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line != "":
                    rows.append(line.split(SEP))
    except FileNotFoundError:
        open(filename, "w").close()
    return rows


def save_file(filename, rows):
    try:
        with open(filename, "w") as file:
            for row in rows:
                file.write(SEP.join(row) + "\n")
    except Exception:
        print("Error saving", filename)


def next_id(rows, prefix):
    if len(rows) == 0:
        return prefix + "101"
    last_id = rows[-1][0]
    number = int(last_id[len(prefix):])
    return prefix + str(number + 1)


def valid_date(date):
    if len(date) != 10 or date[4] != "-" or date[7] != "-":
        return False
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    if not year.isdigit() or not month.isdigit() or not day.isdigit():
        return False
    month = int(month)
    day = int(day)
    if month < 1 or month > 12 or day < 1 or day > 31:
        return False
    return True


# 1. CREATE: Record customer payments
def finance_add_payment():
    orders = load_file("orders.txt")
    payments = load_file("payments.txt")
    order_id = input("Enter Order ID to pay: ").strip().upper()

    for order in orders:
        if order[0] == order_id:
            if order[6] == "Cancelled" or order[7] == "Paid":
                print("Error: Order is already Paid or Cancelled.")
                return

            print("Amount Due: RM", order[5])
            method = input("Payment Method (Cash/Card/QR): ").strip()
            date = input("Payment Date (YYYY-MM-DD): ").strip()
            if method == "" or not valid_date(date):
                print("Error: Invalid method or date.")
                return

            payment_id = next_id(payments, "PAY")
            payments.append([payment_id, order_id, order[5], method, date, "Valid"])
            order[7] = "Paid"
            save_file("payments.txt", payments)
            save_file("orders.txt", orders)
            print("Payment Recorded:", payment_id)
            return

    print("Order ID not found.")


# 2. READ: View outstanding payments
def finance_view():
    orders = load_file("orders.txt")
    total_due = 0.0
    print("\n=== OUTSTANDING PAYMENTS ===")
    for order in orders:
        if order[7] == "Unpaid" and order[6] != "Cancelled":
            print(order[0], "| Customer:", order[1], "| Due: RM", order[5], "| Status:", order[6])
            total_due += float(order[5])
    print("Total Outstanding: RM", f"{total_due:.2f}")


# 3. UPDATE: Update payment status
def finance_update():
    orders = load_file("orders.txt")
    order_id = input("Enter Order ID: ").strip().upper()

    for order in orders:
        if order[0] == order_id:
            print("Current Payment Status:", order[7])
            status = input("New Status (Paid/Unpaid/Refunded): ").strip().capitalize()
            if status not in ["Paid", "Unpaid", "Refunded"]:
                print("Error: Invalid status.")
                return
            order[7] = status
            save_file("orders.txt", orders)
            print("Updated Order", order_id, "payment status to", status)
            return

    print("Order ID not found.")


# 4. DELETE: Void or delete an incorrectly recorded payment (with confirmation)
def finance_delete():
    payments = load_file("payments.txt")
    orders = load_file("orders.txt")

    for payment in payments:
        print(" | ".join(payment))

    payment_id = input("Payment ID to void/delete: ").strip().upper()
    for i in range(len(payments)):
        if payments[i][0] == payment_id:
            answer = input("Confirm void/delete " + payment_id + "? (YES/NO): ").strip().upper()
            if answer == "YES":
                order_id = payments[i][1]
                payments.pop(i)
                for order in orders:
                    if order[0] == order_id:
                        order[7] = "Unpaid"
                save_file("payments.txt", payments)
                save_file("orders.txt", orders)
                print("Payment deleted and Order", order_id, "reverted to Unpaid.")
            return

    print("Payment ID not found.")


# 5. REPORT: Daily income report and monthly sales summary
def finance_report():
    payments = load_file("payments.txt")
    day = input("Enter Date for Daily Income (YYYY-MM-DD): ").strip()
    if not valid_date(day):
        print("Error: Invalid date.")
        return

    month = day[0:7]
    daily_sum = 0.0
    monthly_sum = 0.0
    for payment in payments:
        if payment[5] == "Valid":
            if payment[4] == day:
                daily_sum += float(payment[2])
            if payment[4][0:7] == month:
                monthly_sum += float(payment[2])

    print("\n=== FINANCE REPORT ===")
    print("Daily Income (" + day + ")    : RM", f"{daily_sum:.2f}")
    print("Monthly Sales (" + month + ") : RM", f"{monthly_sum:.2f}")


def finance_menu():
    while True:
        print("\n--- FINANCE OFFICER MENU ---")
        print("1. Record Customer Payment")
        print("2. View Outstanding Payments")
        print("3. Update Payment Status")
        print("4. Void / Delete Payment")
        print("5. Daily Income & Monthly Sales Report")
        print("0. Back")
        choice = input("Choice (0-5): ").strip()

        if choice == "1":
            finance_add_payment()
        elif choice == "2":
            finance_view()
        elif choice == "3":
            finance_update()
        elif choice == "4":
            finance_delete()
        elif choice == "5":
            finance_report()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    finance_menu()
