def pyexec(__code, __globals=None, __locals=None):
	if __globals is None:
		__globals = {}
	if __locals is None:
		__locals = {}
	__locals = dict(__locals)
	__globals = dict(__globals)
	return exec(__code, __globals, __locals)

def pyeval(__code, __globals=None, __locals=None):
	if __globals is None:
		__globals = {}
	if __locals is None:
		__locals = {}
	__locals = dict(__locals)
	__globals = dict(__globals)
	return eval(__code, __globals, __locals)

def pycompile(__code, __filename, __mode):
	return compile(__code, __filename, __mode)

def pyimport(__name):
	return importlib.import_module(__name)

def pygetattr(__obj, __attr):
	return getattr(__obj, __attr)

def pysetattr(__obj, __attr, __value):
	return setattr(__obj, __attr, __value)

def pydelattr(__obj, __attr):
	return delattr(__obj, __attr)

def pyhasattr(__obj, __attr):
	return hasattr(__obj, __attr)

def pytype(__obj):
	return type(__obj)

def pycall(__obj, *args, **kwargs):
	return __obj(*args, **kwargs)

def pybool(__obj):
	if hasattr(__obj, 'literal'):
		return __obj.literal
	return bool(__obj)