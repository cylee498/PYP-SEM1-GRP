# ROLE 2: SERVICE COUNTER OFFICER (counter.py)
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


# 1. CREATE: Register customers and create laundry orders (auto charge + express)
def register_customer():
    customers = load_file("customers.txt")
    name = input("Customer Name: ").strip()
    phone = input("Phone (digits): ").strip()
    if name == "" or not phone.isdigit():
        print("Error: Invalid customer details.")
        return

    customer_id = next_id(customers, "CUS")
    customers.append([customer_id, name, phone])
    save_file("customers.txt", customers)
    print("Registered Customer:", customer_id)


def create_order():
    customers = load_file("customers.txt")
    services = load_file("services.txt")
    orders = load_file("orders.txt")

    if len(customers) == 0 or len(services) == 0:
        print("Error: Ensure customers and services exist first.")
        return

    customer_id = input("Customer ID: ").strip().upper()
    customer_found = False
    for customer in customers:
        if customer[0] == customer_id:
            customer_found = True
    if customer_found == False:
        print("Error: Customer ID not found.")
        return

    print("Available Services:")
    for service in services:
        print(service[0], "-", service[1], "(RM", service[2], "/kg)")

    service_id = input("Service ID: ").strip().upper()
    weight = input("Clothing Weight (kg): ").strip()
    answer = input("Express Service +50%? (Y/N): ").strip().upper()
    if answer == "Y":
        express = "Yes"
    else:
        express = "No"
    date = input("Order Date (YYYY-MM-DD): ").strip()

    if not is_positive_number(weight) or not valid_date(date):
        print("Error: Invalid weight or date.")
        return

    charge = calculate_charge(service_id, weight, express, services)
    if charge == None:
        print("Error: Service ID not found.")
        return

    order_id = next_id(orders, "ORD")
    orders.append([order_id, customer_id, service_id, weight, express, charge,
                   "Pending", "Unpaid", "Uncollected", date])
    save_file("orders.txt", orders)
    print("Order Created:", order_id, "| Calculated Charge: RM", charge)


def counter_add():
    print("1. Register Customer   2. Create Laundry Order")
    choice = input("Choice: ").strip()
    if choice == "1":
        register_customer()
    elif choice == "2":
        create_order()


# 2. READ: View and search customer orders
def counter_view():
    orders = load_file("orders.txt")
    keyword = input("Search by OrderID / CustomerID (or ENTER for all): ").strip().upper()
    for order in orders:
        if keyword == "" or keyword == order[0] or keyword == order[1]:
            print(" | ".join(order))


# 3. UPDATE: Update order details and order/collection status
def counter_update():
    orders = load_file("orders.txt")
    services = load_file("services.txt")
    order_id = input("Order ID to update: ").strip().upper()

    for order in orders:
        if order[0] == order_id:
            print("1. Edit Weight/Express (Pending only)   2. Mark Order as Collected")
            choice = input("Choice: ").strip()

            if choice == "1":
                if order[6] != "Pending":
                    print("Error: Processing already started.")
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
                print("Order updated. New Charge: RM", order[5])
            elif choice == "2":
                if order[6] != "Ready for Collection" or order[7] != "Paid":
                    print("Error: Order must be 'Ready for Collection' and 'Paid' first.")
                    return

                order[6] = "Collected"
                order[8] = "Collected"
                save_file("orders.txt", orders)
                print("Order marked as Collected.")
            return

    print("Order ID not found.")


# 4. DELETE: Cancel an order before processing begins
def counter_delete():
    orders = load_file("orders.txt")
    order_id = input("Order ID to cancel: ").strip().upper()

    for order in orders:
        if order[0] == order_id:
            if order[6] != "Pending":
                print("Blocked: Cannot cancel after processing begins (Status:", order[6] + ").")
                return
            order[6] = "Cancelled"
            save_file("orders.txt", orders)
            print("Order", order_id, "has been Cancelled.")
            return

    print("Order ID not found.")


# 5. REPORT: Daily order list
def counter_report():
    date = input("Enter Date (YYYY-MM-DD): ").strip()
    if not valid_date(date):
        print("Error: Invalid date.")
        return

    orders = load_file("orders.txt")
    count = 0
    print("\n=== DAILY ORDER LIST:", date, "===")
    for order in orders:
        if order[9] == date:
            print(order[0], "| Cust:", order[1], "| Srv:", order[2], "| RM", order[5], "| Status:", order[6])
            count += 1
    print("Total Orders on", date + ":", count)


def counter_menu():
    while True:
        print("\n--- SERVICE COUNTER OFFICER MENU ---")
        print("1. Register Customer / Create Order")
        print("2. View & Search Orders")
        print("3. Update Order / Collection Status")
        print("4. Cancel Order (Before Processing)")
        print("5. Daily Order List Report")
        print("0. Back")
        choice = input("Choice (0-5): ").strip()

        if choice == "1":
            counter_add()
        elif choice == "2":
            counter_view()
        elif choice == "3":
            counter_update()
        elif choice == "4":
            counter_delete()
        elif choice == "5":
            counter_report()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    counter_menu()
