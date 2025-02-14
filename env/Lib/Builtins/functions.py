import sys

str_ = str
int_ = int
float_ = float

def print(*args, end='\n'):
    args2 = []
    for arg in args:
        arg = str(arg)
        try:
            float_value = float(arg)
            if float_value.is_integer():
                arg = str(int(float_value))
            else:
                arg = str(float_value)
        except ValueError:
            pass
        args2.append(arg)
    sys.stdout.write(f"{' '.join(args2)}{end}")

def input(prompt=''):
    sys.stdout.write(prompt)
    return sys.stdin.readline().strip()

def len(obj):
    return obj.__len__()

def str(obj):
    return str_(obj)

def int(obj):
    return int_(obj)

def float(obj):
    return float_(obj)
