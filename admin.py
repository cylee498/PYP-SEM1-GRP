# ROLE 1: LAUNDRY ADMINISTRATOR (admin.py)
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


# 1. CREATE: Add new laundry service types and customer records
def add_record():
    print("1. Add Service Type   2. Add Customer")
    choice = input("Choice: ").strip()

    if choice == "1":
        services = load_file("services.txt")
        name = input("Service Name (e.g. Wash & Dry): ").strip()
        rate = input("Price per kg (RM): ").strip()
        if name == "" or not is_positive_number(rate):
            print("Error: Invalid name or price.")
            return
        service_id = next_id(services, "SRV")
        services.append([service_id, name, f"{float(rate):.2f}"])
        save_file("services.txt", services)
        print("Added Service:", service_id, name)
    elif choice == "2":
        customers = load_file("customers.txt")
        name = input("Customer Name: ").strip()
        phone = input("Phone Number (digits): ").strip()
        if name == "" or not phone.isdigit():
            print("Error: Invalid name or digits-only phone.")
            return
        customer_id = next_id(customers, "CUS")
        customers.append([customer_id, name, phone])
        save_file("customers.txt", customers)
        print("Added Customer:", customer_id, name)
    else:
        print("Invalid choice.")


# 2. READ: View service types, customers, laundry orders and payment info
def view_records():
    print("1. Services  2. Customers  3. Orders  4. Payments")
    choice = input("View which record? (1-4): ").strip()

    if choice == "1":
        filename = "services.txt"
    elif choice == "2":
        filename = "customers.txt"
    elif choice == "3":
        filename = "orders.txt"
    elif choice == "4":
        filename = "payments.txt"
    else:
        print("Invalid choice.")
        return

    rows = load_file(filename)
    if len(rows) == 0:
        print("No records found.")
        return
    for row in rows:
        print(" | ".join(row))


# 3. UPDATE: Update service type details (price) and customer records
def update_record():
    print("1. Update Service Price   2. Update Customer")
    choice = input("Choice: ").strip()

    if choice == "1":
        services = load_file("services.txt")
        service_id = input("Service ID: ").strip().upper()
        for service in services:
            if service[0] == service_id:
                name = input("New Name (blank to keep '" + service[1] + "'): ").strip()
                rate = input("New Rate/kg (blank to keep " + service[2] + "): ").strip()
                if name != "":
                    service[1] = name
                if rate != "":
                    if not is_positive_number(rate):
                        print("Error: Invalid rate.")
                        return
                    service[2] = f"{float(rate):.2f}"
                save_file("services.txt", services)
                print("Service updated.")
                return
        print("Service ID not found.")
    elif choice == "2":
        customers = load_file("customers.txt")
        customer_id = input("Customer ID: ").strip().upper()
        for customer in customers:
            if customer[0] == customer_id:
                name = input("New Name (blank to keep '" + customer[1] + "'): ").strip()
                phone = input("New Phone (blank to keep " + customer[2] + "): ").strip()
                if name != "":
                    customer[1] = name
                if phone != "":
                    if not phone.isdigit():
                        print("Error: Invalid phone.")
                        return
                    customer[2] = phone
                save_file("customers.txt", customers)
                print("Customer updated.")
                return
        print("Customer ID not found.")


# 4. DELETE: Delete service type or customer (blocked if linked to active orders)
def delete_record():
    orders = load_file("orders.txt")
    print("1. Delete Service Type   2. Delete Customer")
    choice = input("Choice: ").strip()

    if choice == "1":
        services = load_file("services.txt")
        service_id = input("Service ID to delete: ").strip().upper()
        for order in orders:
            if order[2] == service_id and order[6] != "Cancelled" and order[6] != "Collected":
                print("Blocked: Service is linked to active Order", order[0])
                return
        for i in range(len(services)):
            if services[i][0] == service_id:
                services.pop(i)
                save_file("services.txt", services)
                print("Deleted Service", service_id)
                return
        print("Service ID not found.")
    elif choice == "2":
        customers = load_file("customers.txt")
        customer_id = input("Customer ID to delete: ").strip().upper()
        for order in orders:
            if order[1] == customer_id and order[6] != "Cancelled" and order[6] != "Collected":
                print("Blocked: Customer has active Order", order[0])
                return
        for i in range(len(customers)):
            if customers[i][0] == customer_id:
                customers.pop(i)
                save_file("customers.txt", customers)
                print("Deleted Customer", customer_id)
                return
        print("Customer ID not found.")


# 5. REPORT: Overall business report (+ Uncollected laundry unique feature)
def business_report():
    services = load_file("services.txt")
    customers = load_file("customers.txt")
    orders = load_file("orders.txt")
    payments = load_file("payments.txt")

    revenue = 0.0
    for payment in payments:
        if payment[5] == "Valid":
            revenue += float(payment[2])

    active_orders = 0
    uncollected = []
    for order in orders:
        if order[6] != "Cancelled" and order[6] != "Collected":
            active_orders += 1
        if order[6] == "Ready for Collection" and order[8] != "Collected":
            uncollected.append(order)

    print("\n=== OVERALL BUSINESS REPORT ===")
    print("Total Service Types :", len(services))
    print("Total Customers     :", len(customers))
    print("Total Orders        :", len(orders), "(Active:", active_orders, ")")
    print("Total Paid Revenue  : RM", f"{revenue:.2f}")
    print("\n--- Uncollected Ready Laundry Report ---")
    if len(uncollected) == 0:
        print("None.")
    for order in uncollected:
        print(order[0], "| Customer:", order[1], "| Charge: RM", order[5], "| Date:", order[9])


def admin_menu():
    while True:
        print("\n--- LAUNDRY ADMINISTRATOR MENU ---")
        print("1. Add Service / Customer")
        print("2. View All Records")
        print("3. Update Service / Customer")
        print("4. Delete Service / Customer")
        print("5. Overall Business & Uncollected Report")
        print("0. Back")
        choice = input("Choice (0-5): ").strip()

        if choice == "1":
            add_record()
        elif choice == "2":
            view_records()
        elif choice == "3":
            update_record()
        elif choice == "4":
            delete_record()
        elif choice == "5":
            business_report()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    admin_menu()
