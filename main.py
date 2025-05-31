from ai import get_intent_and_entities
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
    user_input = input("You: ").strip()

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Goodbye! Your data is saved.")
        save_employees(employees)
        break

    result = get_intent_and_entities(user_input)
    intent = result.get("intent")
    leave_type = result.get("leave_type")
    start_phrase = result.get("start_date")
    end_phrase = result.get("end_date")
    num_days = result.get("num_days")

    if intent == "check_balance":
        if leave_type:
            employee.check_balance(leave_type)
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
            from datetime import timedelta
            end_date = start_date + timedelta(days=num_days - 1)
        else:
            end_date = parse_natural_date(end_phrase)
            if not end_date:
                print("Could not understand the end date.")
                continue

        if not validate_date_range(start_date, end_date):
            continue

        employee.request_leave(leave_type, start_date, end_date)

    elif intent == "cancel_leave":
        if not start_phrase:
            print("Please provide the date of the leave you want to cancel.")
            continue

        cancel_date = parse_natural_date(start_phrase)
        if not cancel_date:
            print("Couldn't understand the cancellation date.")
            continue

        # print(f"Trying to cancel leave on: {cancel_date}")
        employee.cancel_leave(cancel_date)

    elif intent == "view_history":
        current_year = datetime.now().year
        employee.view_history(current_year)

    else:
        print("Sorry, I couldn't understand your request. Try saying it differently.")
