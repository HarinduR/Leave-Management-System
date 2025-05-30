from datetime import datetime
import dateutil.parser

def validate_date_range(start_date, end_date):
    today = datetime.now().date()

    if start_date < today:
        print("Start date is in the past.")
        return False
    if end_date < start_date:
        print("End date is before start date.")
        return False
    return True

def parse_natural_date(natural_str):
    try:
        date = dateutil.parser.parse(natural_str, fuzzy=True)
        return date.date()
    except Exception as e:
        print(f"Couldn’t understand that date: '{natural_str}'. Error: {e}")
        return None
