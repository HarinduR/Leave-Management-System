import json
import os
from employee import Employee, LeaveBalance, LeaveRequest
from datetime import datetime

DATA_FILE = "employees.json" 


def load_employees():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    employees = {}
    for name, record in data["employees"].items():
        emp = Employee(name)

        balance = record["leave_balance"]
        emp.leave_balance = LeaveBalance(
            balance.get("Sick Leave", 0),
            balance.get("Annual Leave", 0),
            balance.get("Maternity Leave", 0)
        )

        for leave_data in record["leave_history"]:
            leave_obj = LeaveRequest.from_dict(leave_data)
            emp.leave_history.append(leave_obj)

        employees[name] = emp

    return employees


def save_employees(employees):
    data = {"employees": {}}

    for name, emp in employees.items():
        balance = {
            "Sick Leave": emp.leave_balance.sick_leave,
            "Annual Leave": emp.leave_balance.annual_leave,
            "Maternity Leave": emp.leave_balance.maternity_leave
        }

        history = [leave.to_dict() for leave in emp.leave_history]

        data["employees"][name] = {
            "leave_balance": balance,
            "leave_history": history
        }

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
    print("All employee data saved. Your boss will be proud!")


def add_employee(employees, name):
    if name in employees:
        print(f"Employee '{name}' already exists!")
    else:
        employees[name] = Employee(name)
        print(f"New employee '{name}' added to the system!")


def update_leave_history(employees, name, leave_request):
    if name not in employees:
        print("Oops! No such employee found.")
        return

    employees[name].leave_history.append(leave_request)
    save_employees(employees)
    print(f"Leave request added for {name} and saved to file.")
