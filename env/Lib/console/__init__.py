"""
This module provides various logging utilities with colored output support,
overwriting capabilities, and a progress bar function.

Functions:
    - overwrite: Clears the current line in the terminal and prints new text.
    - log: Standard print function alias.
    - supports_color: Checks if the terminal supports colored output.
    - debug: Prints debug messages with configurable color.
    - info: Prints informational messages with configurable color.
    - error: Prints error messages with configurable color.
    - fatal: Prints fatal error messages with a darkened color.
    - warn: Prints warning messages with configurable color.
    - progress_bar: Displays a progress bar for an iterable.
    - styled_print: Prints styled text with foreground and background color options.
    - clear: Clears the terminal screen.
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def overwrite(text):
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.write(f"{text}")
    sys.stdout.flush()

def log(*args, **kwargs):
    print(*args, **kwargs)

def supports_color():
    return os.getenv('TERM') != 'dumb' or sys.stdout.isatty()

def debug(*args, **kwargs):
    def hex_to_ansi(hex_color):
        if not hex_color or hex_color.lower() == "reset":
            return "\033[0m"

        match = re.fullmatch(r'#?([A-Fa-f0-9]{6})', hex_color)
        if not match:
            return "\033[0m"

        r, g, b = tuple(default_int(match.group(1)[i:i + 2], 16) for i in (0, 2, 4))
        return f"\033[38;2;{r};{g};{b}m"
    print(f"{hex_to_ansi(config["color_scheme"].get('debug', '#434343'))}{''.join(map(str, args))}\033[0m", **kwargs)

def info(*args, **kwargs):
    def hex_to_ansi(hex_color):
        if not hex_color or hex_color.lower() == "reset":
            return "\033[0m"

        match = re.fullmatch(r'#?([A-Fa-f0-9]{6})', hex_color)
        if not match:
            return "\033[0m"

        r, g, b = tuple(default_int(match.group(1)[i:i + 2], 16) for i in (0, 2, 4))
        return f"\033[38;2;{r};{g};{b}m"
    print(f"{hex_to_ansi(config["color_scheme"].get('info', '#9209B3'))}{''.join(map(str, args))}\033[0m", **kwargs)

def error(*args, **kwargs):
    def hex_to_ansi(hex_color):
        if not hex_color or hex_color.lower() == "reset":
            return "\033[0m"

        match = re.fullmatch(r'#?([A-Fa-f0-9]{6})', hex_color)
        if not match:
            return "\033[0m"

        r, g, b = tuple(default_int(match.group(1)[i:i + 2], 16) for i in (0, 2, 4))
        return f"\033[38;2;{r};{g};{b}m"
    print(f"{hex_to_ansi(config["color_scheme"].get('exception', '#F44350'))}{''.join(map(str, args))}\033[0m", **kwargs)


def progress_bar(iterable, *, prefix='', suffix='Complete', length=40, fill='█', print_end="\n", print_delay=0):
    total = len(iterable)

    if total == 0:
        print(f"{prefix} |{'-' * length}| 0.0% {suffix}")
        return

    def print_bar(iteration):
        percent = f"{100 * (iteration / float(total)):.1f}"
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * int(length - filled_length)

        clear_line = "\r" + " " * 50 + "\r"

        sys.stdout.write(clear_line)
        sys.stdout.write(f'\r{prefix}|{bar}| {percent}%{suffix}')
        sys.stdout.flush()

    for i, item in enumerate(iterable, 1):
        print_bar(i)
        if callable(item):
            try:
                item()
            except Exception as e:
                print(f"\nError executing function at index {i}: {e}")
        time.sleep(print_delay)

    print(print_end, end='')

def fatal(*args, **kwargs):
    def hex_to_ansi(hex_color):
        darken_factor = 0.7
        if not hex_color or hex_color.lower() == "reset":
            return "\033[0m"

        match = re.fullmatch(r'#?([A-Fa-f0-9]{6})', hex_color)
        if not match:
            return "\033[0m"

        r, g, b = (default_int(match.group(1)[i:i + 2], 16) for i in (0, 2, 4))
        r = max(0, int(r * darken_factor))
        g = max(0, int(g * darken_factor))
        b = max(0, int(b * darken_factor))
        return f"\033[1;38;2;{r};{g};{b}m"

    color = hex_to_ansi(config["color_scheme"].get('exception', '#F44350'))
    print(f"{color}{''.join(map(str, args))}\033[0m", **kwargs)

def warn(*args, **kwargs):
    def hex_to_ansi(hex_color):
        if not hex_color or hex_color.lower() == "reset":
            return "\033[0m"

        match = re.fullmatch(r'#?([A-Fa-f0-9]{6})', hex_color)
        if not match:
            return "\033[0m"

        r, g, b = tuple(default_int(match.group(1)[i:i + 2], 16) for i in (0, 2, 4))
        return f"\033[38;2;{r};{g};{b}m"
    print(f"{hex_to_ansi(config["color_scheme"].get('warning', '#FFC107'))}{''.join(map(str, args))}\033[0m", **kwargs)

def styled_print(text, fg_color, *, bg_color=None, bold=False, underline=False, italic=False, strikethrough=False, blink=False, reverse=False, link=None, end="\n"):
    def hex_to_ansi(hex_color):
        if not hex_color or hex_color.lower() == "reset":
            return "\033[0m"

        match = re.fullmatch(r'#?([A-Fa-f0-9]{6})', hex_color)
        if not match:
            return "\033[0m"

        r, g, b = tuple(default_int(match.group(1)[i:i + 2], 16) for i in (0, 2, 4))
        return f"\033[38;2;{r};{g};{b}m"
    style = hex_to_ansi(fg_color)
    if bg_color:
        style += hex_to_ansi(bg_color, is_bg=True)

    if bold:
        style += "\033[1m"
    if italic:
        style += "\033[3m"
    if underline:
        style += "\033[4m"
    if blink:
        style += "\033[5m"
    if reverse:
        style += "\033[7m"
    if strikethrough:
        style += "\033[9m"

    if link:
        text = f"[{text}]({link})"

    reset = "\033[0m"
    print(f"{style}{text}{reset}", end=end)