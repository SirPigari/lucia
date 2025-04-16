def get_config(key, default=None):
	return config.get(key, default)

def set(key, value):
	config[key] = value
	save()

def save():
	with open(CONFIG_FILE, "w") as file:
		json.dump(config, file, indent=2)

def get_color(color):
	return config["color_scheme"].get(color, "#FFFFFF")

for key, value in config.items():
	globals()[key] = value