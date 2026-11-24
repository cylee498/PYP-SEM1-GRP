# ROLE 5 (EXPANDED): CUSTOMER (customer.py)
SEP = "|"
EXPRESS_SURCHARGE = 1.50


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


def is_positive_number(value):
    parts = value.split(".")
    if len(parts) > 2:
        return False
    for part in parts:
        if not part.isdigit():
            return False
    if float(value) <= 0:
        return False
    return True


def calculate_charge(service_id, weight, express, services):
    for service in services:
        if service[0] == service_id:
            total = float(service[2]) * float(weight)
            if express == "Yes":
                total = total * EXPRESS_SURCHARGE
            return f"{total:.2f}"
    return None


# 1. CREATE: Submit a laundry order
def customer_add_order(customer_id):
    services = load_file("services.txt")
    orders = load_file("orders.txt")

    if len(services) == 0:
        print("No laundry services configured yet.")
        return

    for service in services:
        print(service[0], "-", service[1], "(RM", service[2], "/kg)")

    service_id = input("Service ID: ").strip().upper()
    weight = input("Weight (kg): ").strip()
    answer = input("Express +50%? (Y/N): ").strip().upper()
    if answer == "Y":
        express = "Yes"
    else:
        express = "No"
    date = input("Date (YYYY-MM-DD): ").strip()

    if not is_positive_number(weight) or not valid_date(date):
        print("Error: Invalid weight or date.")
        return

    charge = calculate_charge(service_id, weight, express, services)
    if charge == None:
        print("Error: Invalid Service ID.")
        return

    order_id = next_id(orders, "ORD")
    orders.append([order_id, customer_id, service_id, weight, express, charge,
                   "Pending", "Unpaid", "Uncollected", date])
    save_file("orders.txt", orders)
    print("Order Submitted:", order_id, "| Total: RM", charge)


# 2. READ: View available laundry services, order status and payment status
def customer_view(customer_id):
    print("\n-- Available Services --")
    for service in load_file("services.txt"):
        print(service[0], "|", service[1], "| RM", service[2], "/kg")

    print("\n-- Your Active Orders --")
    for order in load_file("orders.txt"):
        if order[1] == customer_id and order[6] != "Cancelled" and order[6] != "Collected":
            print(order[0], "| Srv:", order[2], "| RM", order[5], "| Order:",
                  order[6], "| Pay:", order[7], "| Collect:", order[8])


# 3. UPDATE: Update their own order before processing begins
def customer_update(customer_id):
    orders = load_file("orders.txt")
    services = load_file("services.txt")
    order_id = input("Your Order ID to update: ").strip().upper()

    for order in orders:
        if order[0] == order_id and order[1] == customer_id:
            if order[6] != "Pending":
                print("Blocked: Processing has already started.")
                return

            weight = input("New Weight (kg): ").strip()
            answer = input("Express? (Y/N): ").strip().upper()
            if answer == "Y":
                express = "Yes"
            else:
                express = "No"

            if not is_positive_number(weight):
                print("Error: Invalid weight.")
                return

            order[3] = weight
            order[4] = express
            order[5] = calculate_charge(order[2], weight, express, services)
            save_file("orders.txt", orders)
            print("Updated! New Total: RM", order[5])
            return

    print("Order ID not found under your account.")


# 4. DELETE: Cancel their own order before processing begins
def customer_delete(customer_id):
    orders = load_file("orders.txt")
    order_id = input("Your Order ID to cancel: ").strip().upper()

    for order in orders:
        if order[0] == order_id and order[1] == customer_id:
            if order[6] != "Pending":
                print("Blocked: Cannot cancel once processing begins.")
                return
            order[6] = "Cancelled"
            save_file("orders.txt", orders)
            print("Order", order_id, "cancelled.")
            return

    print("Order ID not found under your account.")


# 5. REPORT: Previous laundry orders
def customer_report(customer_id):
    orders = load_file("orders.txt")
    total_spent = 0.0

    print("\n=== ORDER HISTORY FOR", customer_id, "===")
    for order in orders:
        if order[1] == customer_id:
            print(order[0], "| Date:", order[9], "| Srv:", order[2], "| RM",
                  order[5], "| Status:", order[6], "| Pay:", order[7])
            if order[7] == "Paid":
                total_spent += float(order[5])
    print("Total Paid Spend: RM", f"{total_spent:.2f}")


def customer_menu():
    customers = load_file("customers.txt")
    customer_id = input("Enter your Customer ID (e.g. CUS101): ").strip().upper()

    customer_found = False
    for customer in customers:
        if customer[0] == customer_id:
            customer_found = True
    if customer_found == False:
        print("Customer ID not registered. Please register at the Service Counter first.")
        return

    while True:
        print("\n--- CUSTOMER MENU (" + customer_id + ") ---")
        print("1. Submit Laundry Order")
        print("2. View Services & Active Order Status")
        print("3. Update Pending Order")
        print("4. Cancel Pending Order")
        print("5. My Order History Report")
        print("0. Back")
        choice = input("Choice (0-5): ").strip()

        if choice == "1":
            customer_add_order(customer_id)
        elif choice == "2":
            customer_view(customer_id)
        elif choice == "3":
            customer_update(customer_id)
        elif choice == "4":
            customer_delete(customer_id)
        elif choice == "5":
            customer_report(customer_id)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    customer_menu()
