from ai import get_intent_and_entities, generate_natural_response
from database import load_employees, save_employees, add_employee
from utils import parse_natural_date, validate_date_range
from datetime import datetime, timedelta

print("\nWelcome to the Leave Management System")

employees = load_employees()

user_name = input("\n\nEnter your name to log in: ").strip().title()
add_employee(employees, user_name)
employee = employees[user_name]

while True:
    print("\nType your request (or type 'exit' to leave):")
    user_input = input("You: ").strip() #input request

    if user_input.lower() in ["exit", "quit", "bye"]:   #exit handel done 
        print("\nGoodbye! Your data is saved.")
        save_employees(employees)
        break

    #extract data from query
    result = get_intent_and_entities(user_input)
    intent = result.get("intent")
    leave_type = result.get("leave_type")
    start_phrase = result.get("start_date")
    end_phrase = result.get("end_date")
    num_days = result.get("num_days")

    if intent == "check_balance":
        if leave_type:
            balance = employee.leave_balance.get_balance(leave_type)
            response = generate_natural_response(
                name=user_name,
                intent="check_balance",
                leave_type=leave_type,
                balance=balance
            )
            print(response)
        else:
            print("I couldn't figure out which leave type. Try again with more details.")

    elif intent == "request_leave":
        if not all([leave_type, start_phrase, num_days]):
            print("Incomplete info to request leave. Please try again.")
            continue

        start_date = parse_natural_date(start_phrase)
        if not start_date:
            print("Could not understand the start date.")
            continue

        if not end_phrase:
            end_date = start_date + timedelta(days=num_days - 1)
        else:
            end_date = parse_natural_date(end_phrase)
            if not end_date:
                print("Could not understand the end date.")
                continue

        if not validate_date_range(start_date, end_date):
            continue

        # Check balance first
        balance = employee.leave_balance.get_balance(leave_type)
        if balance < num_days:
            response = generate_natural_response(
                name=user_name,
                intent="request_leave",
                leave_type=leave_type,
                num_days=num_days,
                start=start_date.strftime("%Y-%m-%d"),
                end=end_date.strftime("%Y-%m-%d"),
                balance=balance,
                status="Declined"
            )
            print(response)
            continue

        employee.request_leave(leave_type, start_date, end_date)
        response = generate_natural_response(
            name=user_name,
            intent="request_leave",
            leave_type=leave_type,
            num_days=num_days,
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d"),
            status="Approved"
        )
        print(response)

    elif intent == "cancel_leave":
        if not start_phrase:
            print("Please provide the date of the leave you want to cancel.")
            continue

        cancel_date = parse_natural_date(start_phrase)
        if not cancel_date:
            print("Couldn't understand the cancellation date.")
            continue

        found = False
        for leave in employee.leave_history:
            if leave.start_date <= cancel_date <= leave.end_date and leave.status == "Pending":
                found = True
                break

        if found:
            employee.cancel_leave(cancel_date)
            response = generate_natural_response(
                name=user_name,
                intent="cancel_leave",
                leave_type=leave.leave_type,
                start=leave.start_date.strftime("%Y-%m-%d"),
                status="Cancelled"
            )
        else:
            response = generate_natural_response(
                name=user_name,
                intent="cancel_leave",
                start=cancel_date.strftime("%Y-%m-%d"),
                status="Not Found"
            )
        print(response)

    elif intent == "view_history":
        print(f"\n{user_name}'s Leave History:")
        history_found = False
        for leave in employee.leave_history:
            if leave.start_date.year == datetime.now().year:
                print(f"- {leave.leave_type} from {leave.start_date} to {leave.end_date} | {leave.status}")
                history_found = True
        if not history_found:
            print("No leaves taken yet...")

    else:
        print("Sorry, I couldn't understand your request. Try saying it differently.")
