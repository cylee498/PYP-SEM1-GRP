# CASE 5: FRESHWASH LAUNDRY - LAUNDRY STAFF MODULE
ORDERS_FILE = "orders.txt"
COMPLETED_FILE = "completed_services.txt"
SEP = "|"


# --- Helper Functions (File I/O & Validation) ---

def load_file(filename):
    data = []
    try:
        with open(filename, "r") as f:
            for line in f:
                if line.strip() != "":
                    data.append(line.strip().split(SEP))
    except FileNotFoundError:
        open(filename, "w").close()
    return data


def save_file(filename, data):
    try:
        with open(filename, "w") as f:
            for row in data:
                f.write(SEP.join(row) + "\n")
    except Exception:
        print("Error saving file.")


def valid_date(d):
    if len(d) != 10 or d[4] != "-" or d[7] != "-":
        return False
    year = d[0:4]
    month = d[5:7]
    day = d[8:10]
    if not year.isdigit() or not month.isdigit() or not day.isdigit():
        return False
    if int(month) < 1 or int(month) > 12:
        return False
    if int(day) < 1 or int(day) > 31:
        return False
    return True


# --- 1. CREATE: Record completed services ---

def record_completed():
    orders = load_file(ORDERS_FILE)
    completed = load_file(COMPLETED_FILE)
    order_id = input("Enter Order ID: ").strip().upper()

    for row in completed:
        if row[1] == order_id:
            print("Error: Service already recorded for this order.")
            return

    for row in orders:
        if row[0] == order_id and row[5] not in ["Cancelled", "Collected"]:
            date = input("Completion Date (YYYY-MM-DD): ").strip()
            if not valid_date(date):
                print("Error: Invalid date format.")
                return

            if len(completed) == 0:
                service_id = "SVC1001"
            else:
                last_id = completed[-1][0]
                next_number = int(last_id[3:]) + 1
                service_id = "SVC" + str(next_number)

            completed.append([service_id, row[0], row[2], row[3], date])
            row[5] = "Ready for Collection"
            row[7] = "Ready"
            save_file(COMPLETED_FILE, completed)
            save_file(ORDERS_FILE, orders)
            print("Recorded as", service_id, "- Order marked Ready for Collection.")
            return

    print("Error: Valid active Order ID not found.")


# --- 2. READ: View pending laundry orders and daily workload ---

def view_workload():
    orders = load_file(ORDERS_FILE)
    pending = 0
    washing = 0
    drying = 0

    print("\nOrderID | Service | Weight(kg) | Status | Date")
    print("-" * 55)
    for row in orders:
        if row[5] == "Pending":
            print(row[0], "|", row[2], "|", row[3], "|", row[5], "|", row[8])
            pending += 1
        elif row[5] == "Washing":
            print(row[0], "|", row[2], "|", row[3], "|", row[5], "|", row[8])
            washing += 1
        elif row[5] == "Drying":
            print(row[0], "|", row[2], "|", row[3], "|", row[5], "|", row[8])
            drying += 1

    total = pending + washing + drying
    print("-" * 55)
    print("Pending:", pending, "| Washing:", washing,
          "| Drying:", drying, "| Total:", total)


# --- 3. UPDATE: Update washing/drying status; mark ready for collection ---

def update_status():
    orders = load_file(ORDERS_FILE)
    order_id = input("Enter Order ID: ").strip().upper()

    for row in orders:
        if row[0] == order_id and row[5] not in ["Cancelled", "Collected"]:
            print("Current Status:", row[5])
            print("1. Washing  2. Drying  3. Ready for Collection")
            choice = input("New status (1-3): ").strip()

            if choice == "1":
                row[5] = "Washing"
                row[7] = "Uncollected"
            elif choice == "2":
                row[5] = "Drying"
                row[7] = "Uncollected"
            elif choice == "3":
                row[5] = "Ready for Collection"
                row[7] = "Ready"
            else:
                print("Error: Invalid choice.")
                return

            save_file(ORDERS_FILE, orders)
            print("Updated Order", order_id, "to", row[5])
            return

    print("Error: Valid Order ID not found.")


# --- 4. DELETE: Delete an incorrectly recorded service entry ---

def delete_entry():
    completed = load_file(COMPLETED_FILE)
    if len(completed) == 0:
        print("No completed service entries found.")
        return

    for row in completed:
        print(row[0], "| Order:", row[1], "|", row[2], "| Date:", row[4])

    service_id = input("Enter Service ID to delete: ").strip().upper()
    for i in range(len(completed)):
        if completed[i][0] == service_id:
            confirm = input("Confirm delete? (YES/NO): ").strip().upper()
            if confirm == "YES":
                completed.pop(i)
                save_file(COMPLETED_FILE, completed)
                print("Deleted", service_id)
            else:
                print("Deletion cancelled.")
            return

    print("Error: Service ID not found.")


# --- 5. REPORT: Daily workload and completed services report ---

def daily_report():
    date = input("Report Date (YYYY-MM-DD): ").strip()
    if not valid_date(date):
        print("Error: Invalid date format.")
        return

    orders = load_file(ORDERS_FILE)
    completed = load_file(COMPLETED_FILE)

    print("\n=== DAILY REPORT:", date, "===")
    print("-- Completed Services --")
    completed_count = 0
    total_weight = 0.0
    for row in completed:
        if row[4] == date:
            print(row[0], "| Order:", row[1], "|", row[2], "|", row[3], "kg")
            completed_count += 1
            total_weight += float(row[3])
    print("Completed Jobs:", completed_count,
          "| Total Weight:", round(total_weight, 2), "kg")

    print("\n-- Remaining Active Workload --")
    active_count = 0
    for row in orders:
        if row[8] == date and row[5] in ["Pending", "Washing", "Drying"]:
            print(row[0], "|", row[2], "|", row[3], "kg |", row[5])
            active_count += 1
    print("Active Orders for Date:", active_count)


# --- Role Menu ---

def staff_menu():
    while True:
        print("\n--- LAUNDRY STAFF MENU ---")
        print("1. Record Completed Service")
        print("2. View Pending Orders & Workload")
        print("3. Update Order Status")
        print("4. Delete Service Entry")
        print("5. Daily Workload & Completed Report")
        print("0. Exit")
        choice = input("Choice (0-5): ").strip()

        if choice == "1":
            record_completed()
        elif choice == "2":
            view_workload()
        elif choice == "3":
            update_status()
        elif choice == "4":
            delete_entry()
        elif choice == "5":
            daily_report()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    staff_menu()
