from datetime import datetime, timedelta
import dateutil.parser
import calendar

def validate_date_range(start_date, end_date):
    today = datetime.now().date()

    if start_date < today:
        print("Start date is in the past. Are you a time traveler?")
        return False
    if end_date < start_date:
        print("End date is before start date. Time flows forward, remember?")
        return False
    return True

def parse_natural_date(natural_str):
    try:
        date = dateutil.parser.parse(natural_str, fuzzy=True)
        return date.date()
    except Exception as e:
        print(f"Couldn’t understand that date: '{natural_str}'. Error: {e}")
        return None

def is_leap_year(year):
    return calendar.isleap(year)

PUBLIC_HOLIDAYS = [
    "2025-01-01",  
    "2025-04-14",
    "2025-12-25",
]

def is_public_holiday(date_obj):
    return date_obj.strftime("%Y-%m-%d") in PUBLIC_HOLIDAYS
