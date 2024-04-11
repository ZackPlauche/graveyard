def listify(list_, ordered=False) -> str:
    """ Turn a list into a string representaton of the list. Either numbered
    or bulleted.  """
    if ordered:
        return '\n'.join([f'{i}. {answer}' for i, answer in enumerate(list_, 1)])
    return '\n'.join([f'• {answer}' for answer in list_])


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def create_total_time_string(seconds):
    hours, minutes = convert_seconds_to_hours_minutes(seconds)
    minute_suffix = 'minutes' if minutes != 1 else 'minute'
    hour_suffix = 'hours' if hours != 1 else 'hour'
    total_time = f'{minutes} {minute_suffix}'
    if hours:
        total_time = f'{hours} {hour_suffix} ' + total_time
    return total_time


def convert_seconds_to_hours_minutes(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    hours = int(hours)
    minutes = int(minutes)
    return hours, minutes
