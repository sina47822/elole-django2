from datetime import timedelta, datetime
from stylist.models import WorkDay

def split_work_hours(stylist, date, service_duration):
    """
    Get available time slots for a specific stylist, date, and service duration.
    
    :param stylist: Stylist instance
    :param date: A specific date to check (WorkDay instance)
    :param service_duration: Duration of the service (timedelta)
    :return: A list of available time slots (start and end times)
    """
    available_slots = []

    # Fetch the workday for the stylist
    try:
        workday = WorkDay.objects.get(stylist=stylist, day=date)
    except WorkDay.DoesNotExist:
        return available_slots  # No workday available for that stylist on that date

    # Loop through each available hour range
    for work_hour in workday.hour.all():
        start_time = datetime.combine(date, work_hour.start_time)
        end_time = datetime.combine(date, work_hour.end_time)

        current_time = start_time

        # Split the time based on service duration
        while current_time + service_duration <= end_time:
            next_time = current_time + service_duration
            available_slots.append((current_time.time(), next_time.time()))
            current_time = next_time

    return available_slots