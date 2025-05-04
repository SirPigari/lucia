def _custom_serializer(obj):
	if hasattr(obj, '__json__'):
		return obj.__json__()
	elif hasattr(obj, 'to_json'):
		return obj.to_json()
	else:
		return og_dumps(obj, indent=4)


def get_config(key, default=None):
	return config.get(key, default)

def set(key, value):
	config[key] = value

def set_config(key, value):
	config[key] = value

def save():
	with open(config["config_file"], "w") as file:
		json.dump(config, file, indent=2, default=_custom_serializer)

def get_color(color):
	return config["color_scheme"].get(color, "#FFFFFF")

for key, value in config.items():
	globals()[key] = value