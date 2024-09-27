from django import template
from datetime import timedelta, datetime, time

register = template.Library()

@register.filter
def add_minutes(time, minutes):
    """Adds minutes to a time object."""
    return time + timedelta(minutes=minutes)


@register.filter
def add_minutes_review(hour, minutes):
    """Ensure 'hour' is a datetime.time or string and 'minutes' is an integer."""
    
    # Check if hour is a string and convert it to datetime.time object if necessary
    if isinstance(hour, str):
        try:
            # Convert string (e.g., "09:00") to datetime.time object
            hour = datetime.strptime(hour, '%H:%M').time()
        except ValueError:
            return hour  # If parsing fails, return the original hour value

    # Ensure 'hour' is a datetime.time object and 'minutes' is an integer
    if isinstance(hour, time) and isinstance(minutes, int):
        # Combine with today's date to create a datetime object
        full_datetime = datetime.combine(datetime.today(), hour)
        # Add minutes using timedelta
        new_time = full_datetime + timedelta(minutes=minutes)
        # Return formatted time string (HH:MM)
        return new_time.time().strftime('%H:%M')
    else:
        return hour  # If conditions are not met, return the original hour



