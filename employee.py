from datetime import datetime

class LeaveBalance:
    def __init__(self, sick=5, annual=10, maternity=0):
        self.sick_leave = sick
        self.annual_leave = annual
        self.maternity_leave = maternity

    def get_balance(self, leave_type):
        if leave_type == "Sick Leave":
            return self.sick_leave
        elif leave_type == "Annual Leave":
            return self.annual_leave
        elif leave_type == "Maternity Leave":
            return self.maternity_leave
        else:
            return 0  

    def update_balance(self, leave_type, days):
        if leave_type == "Sick Leave":
            self.sick_leave -= days
        elif leave_type == "Annual Leave":
            self.annual_leave -= days
        elif leave_type == "Maternity Leave":
            self.maternity_leave -= days

class LeaveRequest:
    def __init__(self, leave_type, start_date, end_date, num_days, status="Pending"):
        self.leave_type = leave_type
        self.start_date = start_date
        self.end_date = end_date
        self.num_days = num_days
        self.status = status

    def to_dict(self):
        return {
            "leave_type": self.leave_type,
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "end_date": self.end_date.strftime("%Y-%m-%d"),
            "num_days": self.num_days,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return LeaveRequest(
            data["leave_type"],
            datetime.strptime(data["start_date"], "%Y-%m-%d"),
            datetime.strptime(data["end_date"], "%Y-%m-%d"),
            data["num_days"],
            data["status"]
        )

class Employee:
    def __init__(self, name):
        self.name = name
        self.leave_balance = LeaveBalance()
        self.leave_history = []

    def check_balance(self, leave_type):
        balance = self.leave_balance.get_balance(leave_type)
        print(f"{self.name}, you have {balance} {leave_type.lower()}s left.")

    def request_leave(self, leave_type, start_date, end_date):
        num_days = (end_date - start_date).days + 1

        if self.leave_balance.get_balance(leave_type) < num_days:
            print("Not enough leaves left, Try fewer days or different type.")
            return

        new_request = LeaveRequest(leave_type, start_date, end_date, num_days)
        self.leave_history.append(new_request)
        self.leave_balance.update_balance(leave_type, num_days)

        print(f"{num_days} day(s) of {leave_type} requested from {start_date} to {end_date}.")

    def cancel_leave(self, target_date):
        for leave in self.leave_history:
            if leave.start_date <= target_date <= leave.end_date and leave.status.lower() == "pending":
                leave.status = "Cancelled"
                self.leave_balance.update_balance(leave.leave_type, -leave.num_days)
                print(f"Your leave from {leave.start_date} has been cancelled and balance refunded!")
                return
        print("No matching leave found to cancel on that date.")

    def view_history(self, year=None):
        print(f"\n{self.name}'s Leave History:")
        for leave in self.leave_history:
            if not year or leave.start_date.year == year:
                print(f"- {leave.leave_type} from {leave.start_date.date()} to {leave.end_date.date()} | {leave.status}")
        if not self.leave_history:
            print("No leaves taken yet... time to plan a trip maybe?")
