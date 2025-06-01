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
            datetime.strptime(data["start_date"], "%Y-%m-%d").date(),
            datetime.strptime(data["end_date"], "%Y-%m-%d").date(),
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
        print(f"Hi {self.name}, you currently have {balance} days of {leave_type.lower()} remaining.")

    def request_leave(self, leave_type, start_date, end_date):
        num_days = (end_date - start_date).days + 1

        if self.leave_balance.get_balance(leave_type) < num_days:
            # print(
            #     f"Hi {self.name}, your request for {num_days} days of {leave_type} was declined due to insufficient balance."
            # )
            return

        new_request = LeaveRequest(leave_type, start_date, end_date, num_days)
        self.leave_history.append(new_request)
        self.leave_balance.update_balance(leave_type, num_days)

        # print(
        #     f"Hi {self.name}, your {num_days}-day {leave_type.lower()} request from "
        #     f"{start_date.strftime('%B %d')} to {end_date.strftime('%B %d')} has been approved. "
        #     f"Enjoy your time off!"
        # )

    def cancel_leave(self, target_date):
        for leave in self.leave_history:
            if leave.start_date <= target_date <= leave.end_date and leave.status == "Pending":
                leave.status = "Cancelled"
                self.leave_balance.update_balance(leave.leave_type, -leave.num_days)
                print(
                    f"Hi {self.name}, your leave from {leave.start_date.strftime('%B %d')} "
                    f"to {leave.end_date.strftime('%B %d')} has been successfully cancelled and your balance refunded."
                )
                return
        print(
            f"Hi {self.name}, no matching pending leave was found on {target_date.strftime('%B %d')}. "
            "Please check your request."
        )

    def view_history(self, year=None):
        print(f"\n{self.name}'s Leave History:")
        found = False
        for leave in self.leave_history:
            if not year or leave.start_date.year == year:
                found = True
                print(
                    f"- {leave.leave_type} from {leave.start_date.strftime('%b %d')} "
                    f"to {leave.end_date.strftime('%b %d')} | {leave.status}"
                )
        if not found:
            print("No leaves taken yet...")
