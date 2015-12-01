import re

MILLISECONDS = 'milliseconds'
SECONDS = 'seconds'
MINUTES = 'minutes'
HOURS = 'hours'
DAYS = 'days'
WEEKS = 'weeks'
MONTHS = 'months'
YEARS = 'years'

TIME_UNITS = (
    MILLISECONDS,
    SECONDS,
    MINUTES,
    HOURS,
    DAYS,
    WEEKS,
    MONTHS,
    YEARS
)

time_pattern = re.compile(ur'^(?P<value>[0-9]+)(?P<unit>[a-zA-Z]+)$')


def parse_time(time_unit):
    match = time_pattern.match(time_unit)
    if match:
        value, unit = match.groups()

        if unit.lower() not in TIME_UNITS:
            raise ValueError("Invalid time unit: %s" % unit)

        return int(value), unit