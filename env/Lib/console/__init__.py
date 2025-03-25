def update_console(text):
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.write(f"{text}")
    sys.stdout.flush()

def styled_print(text, fg_color, *, bg_color=None, bold=False, underline=False, italic=False, strikethrough=False, blink=False, reverse=False, link=None, end="\n"):
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