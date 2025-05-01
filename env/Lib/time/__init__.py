import datetime

#define time

def now():
    """Returns the current local date and time."""
    return datetime.datetime.now()

def today():
    """Returns the current local date."""
    return datetime.date.today()

def utcnow():
    """Returns the current UTC date and time."""
    return datetime.datetime.now(datetime.UTC)

def localtime():
    """Returns the current local time."""
    return datetime.datetime.now().time()

def strftime(format):
    """Formats a date or time according to the given format string."""
    return datetime.datetime.now().strftime(format)

def strptime(date_string, format):
    """Parses a date string according to the given format string."""
    return datetime.datetime.strptime(date_string, format)

def sleep(seconds):
    """Suspends execution for the given number of seconds."""
    time.sleep(seconds)

def time():
    """Returns the current time in seconds since the epoch."""
    return datetime.datetime.now().timestamp()

def mktime(t):
    """Converts a time tuple to seconds since the epoch."""
    return datetime.datetime(*t).timestamp()

def asctime(t=None):
    """Converts a time tuple to a string."""
    if t is None:
        t = datetime.datetime.now()
    return t.strftime("%a %b %d %H:%M:%S %Y")
