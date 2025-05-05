def start(cmd):
    os.system(cmd)

def getcwd():
    return os.getcwd()

def title(title):
    os.system(f"title {title}")

def listdir(path='.'):
    return os.listdir(path)