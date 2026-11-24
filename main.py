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
    y, m, day = d[0:4], d[5:7], d[8:10]
    if not (y.isdigit() and m.isdigit() and day.isdigit()):
        return False
    return 1 <= int(m) <= 12 and 1 <= int(day) <= 31


# --- 1. CREATE: Record completed services ---

def staff_record_completed():
    orders = load_file(ORDERS_FILE)
    completed = load_file(COMPLETED_FILE)
    oid = input("Enter Order ID: ").strip().upper()

    for c in completed:
        if c[1] == oid:
            print("Error: Service already recorded for this order.")
            return

    for o in orders:
        if o[0] == oid and o[5] not in ["Cancelled", "Collected"]:
            date = input("Completion Date (YYYY-MM-DD): ").strip()
            if not valid_date(date):
                print("Error: Invalid date format.")
                return
            next_num = int(completed[-1][0][3:]) + 1 if completed else 1001
            sid = "SVC" + str(next_num)
            completed.append([sid, o[0], o[2], o[3], date])
            o[5], o[7] = "Ready for Collection", "Ready"
            save_file(COMPLETED_FILE, completed)
            save_file(ORDERS_FILE, orders)
            print("Recorded as", sid, "- Order marked Ready for Collection.")
            return
    print("Error: Valid active Order ID not found.")


# --- 2. READ: View pending laundry orders and daily workload ---

def staff_view_workload():
    orders = load_file(ORDERS_FILE)
    counts = {"Pending": 0, "Washing": 0, "Drying": 0}
    print("\nOrderID | Service | Weight(kg) | Status | Date")
    print("-" * 55)
    for o in orders:
        if o[5] in counts:
            print(o[0], "|", o[2], "|", o[3], "|", o[5], "|", o[8])
            counts[o[5]] += 1
    total = counts["Pending"] + counts["Washing"] + counts["Drying"]
    print("-" * 55)
    print("Pending:", counts["Pending"], "| Washing:", counts["Washing"],
          "| Drying:", counts["Drying"], "| Total:", total)


# --- 3. UPDATE: Update washing/drying status; mark ready for collection ---

def staff_update_status():
    orders = load_file(ORDERS_FILE)
    oid = input("Enter Order ID: ").strip().upper()
    for o in orders:
        if o[0] == oid and o[5] not in ["Cancelled", "Collected"]:
            print("Current Status:", o[5])
            print("1. Washing  2. Drying  3. Ready for Collection")
            ch = input("New status (1-3): ").strip()
            status_map = {"1": "Washing", "2": "Drying", "3": "Ready for Collection"}
            if ch not in status_map:
                print("Error: Invalid choice.")
                return
            o[5] = status_map[ch]
            o[7] = "Ready" if ch == "3" else "Uncollected"
            save_file(ORDERS_FILE, orders)
            print("Updated Order", oid, "to", o[5])
            return
    print("Error: Valid Order ID not found.")


# --- 4. DELETE: Delete an incorrectly recorded service entry ---

def staff_delete_entry():
    completed = load_file(COMPLETED_FILE)
    if not completed:
        print("No completed service entries found.")
        return
    for c in completed:
        print(c[0], "| Order:", c[1], "|", c[2], "| Date:", c[4])
    sid = input("Enter Service ID to delete: ").strip().upper()
    for i in range(len(completed)):
        if completed[i][0] == sid:
            if input("Confirm delete? (YES/NO): ").strip().upper() == "YES":
                completed.pop(i)
                save_file(COMPLETED_FILE, completed)
                print("Deleted", sid)
            else:
                print("Deletion cancelled.")
            return
    print("Error: Service ID not found.")


# --- 5. REPORT: Daily workload and completed services report ---

def staff_daily_report():
    date = input("Report Date (YYYY-MM-DD): ").strip()
    if not valid_date(date):
        print("Error: Invalid date format.")
        return
    orders = load_file(ORDERS_FILE)
    completed = load_file(COMPLETED_FILE)

    print("\n=== DAILY REPORT:", date, "===")
    print("-- Completed Services --")
    comp_count, comp_kg = 0, 0.0
    for c in completed:
        if c[4] == date:
            print(c[0], "| Order:", c[1], "|", c[2], "|", c[3], "kg")
            comp_count += 1
            comp_kg += float(c[3])
    print("Completed Jobs:", comp_count, "| Total Weight:", round(comp_kg, 2), "kg")

    print("\n-- Remaining Active Workload --")
    active = 0
    for o in orders:
        if o[8] == date and o[5] in ["Pending", "Washing", "Drying"]:
            print(o[0], "|", o[2], "|", o[3], "kg |", o[5])
            active += 1
    print("Active Orders for Date:", active)


# --- Role Menu ---

def laundry_staff_menu():
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
            staff_record_completed()
        elif choice == "2":
            staff_view_workload()
        elif choice == "3":
            staff_update_status()
        elif choice == "4":
            staff_delete_entry()
        elif choice == "5":
            staff_daily_report()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    laundry_staff_menu()
