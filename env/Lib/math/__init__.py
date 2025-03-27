# Constants
import decimal


e = Decimal(math.e)
pi = Decimal(math.pi)
tau = Decimal(math.tau)
inf = Decimal(math.inf)
nan = Decimal(math.nan)

E = e
PI = pi
TAU = tau
INF = inf
NAN = nan

# Functions
def log(x, base=None):
    if base is None:
        return math.log(x)
    return Decimal(math.log(x, base))


def getPi(n=2):
    n = int(n)
    with decimal.localcontext() as ctx:
        ctx.prec = n + 5
        a = Decimal(1)
        b = Decimal(1) / Decimal(2).sqrt()
        t = Decimal(1) / Decimal(4)
        p = Decimal(1)
        for iteration in range(0, 100):
            an = (a + b) / 2
            bn = (a * b).sqrt()
            tn = t - p * (a - an) ** 2
            pn = 2 * p
            a, b, t, p = an, bn, tn, pn
        pi = (a + b) ** 2 / (4 * t)
        return Decimal(str(pi)[:n + 2])

def abs(x):
    return Decimal(math.fabs(x))

def acos(x):
    return Decimal(math.acos(x))

def acosh(x):
    return Decimal(math.acosh(x))

def asin(x):
    return Decimal(math.asin(x))

def asinh(x):
    return Decimal(math.asinh(x))

def atan(x):
    return Decimal(math.atan(x))

def atan2(y, x):
    return Decimal(math.atan2(y, x))

def atanh(x):
    return Decimal(math.atanh(x))

def ceil(x):
    return Decimal(math.ceil(x))

def comb(n, k):
    return Decimal(math.comb(n, k))

def copysign(x, y):
    return Decimal(math.copysign(x, y))

def cos(x):
    return Decimal(math.cos(x))

def cosh(x):
    return Decimal(math.cosh(x))

def degrees(x):
    return Decimal(math.degrees(x))

def dist(p, q):
    return Decimal(math.dist(p, q))

def erf(x):
    return Decimal(math.erf(x))

def erfc(x):
    return Decimal(math.erfc(x))

def exp(x):
    return Decimal(math.exp(x))

def expm1(x):
    return Decimal(math.expm1(x))

def sin(x):
    return Decimal(math.sin(x))

def sinh(x):
    return Decimal(math.sinh(x))

def sqrt(x):
    return Decimal(math.sqrt(x))

def tan(x):
    return Decimal(math.tan(x))

def tanh(x):
    return Decimal(math.tanh(x))

def trunc(x):
    return Decimal(math.trunc(x))

def factorial(x):
    return Decimal(math.factorial(x))

def floor(x):
    return Decimal(math.floor(x))

def fmod(x, y):
    return Decimal(math.fmod(x, y))

def frexp(x):
    return Decimal(math.frexp(x))

def fsum(iterable):
    return Decimal(math.fsum(iterable))

def gamma(x):
    return Decimal(math.gamma(x))

def gcd(x, y):
    return Decimal(math.gcd(x, y))