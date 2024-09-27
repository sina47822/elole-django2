from datetime import datetime, timedelta
from stylist.models import Stylist, WorkDay, SpecificWorkHour, WorkHour

def get_available_hours(workday):
    general_hours = list(workday.general_hours.all())
    specific_hours = list(workday.specific_work_hours.all())

    available_hours = []
    
    # Convert WorkHour into time slots
    for wh in general_hours:
        available_hours.append((wh.start_time, wh.end_time))

    # Adjust available hours based on specific hours
    for sh in specific_hours:
        if sh.pros_minus:  # If True, add the specific time slot
            available_hours.append((sh.start_time, sh.end_time))
        else:  # If False, remove the specific time slot
            available_hours = [
                (start, end) for start, end in available_hours
                if not (start == sh.start_time and end == sh.end_time)
            ]

    return available_hours