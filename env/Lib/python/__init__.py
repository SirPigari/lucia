def pyexec(__code, __globals, __locals):
	exec(__code, __globals, __locals)

def pyeval(__code, __globals, __locals):
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