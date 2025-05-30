def randint(a, b):
    return random.randint(int(a), int(b))

def choice(seq):
    return random.choice(seq)

def shuffle(seq):
    random.shuffle(seq)
    return seq

def seed(a=None, version=2):
    random.seed(a, version)
    return a

def randbool(chance=0.5):
    return Boolean(random.random() < chance)

def getstate():
    return random.getstate()

def setstate(state):
    return random.setstate(state)

def getrandbits(k):
    return random.getrandbits(k)

def randrange(start, stop=None, step=1):
    return random.randrange(int(start), int(stop), int(step))

def uniform(a, b):
    return random.uniform(a, b)