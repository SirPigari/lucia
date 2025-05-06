import os
import sys
import json

def hex_to_ansi(hex_color):
    if not hex_color or hex_color.lower() == "reset":
        return "\033[0m"
    match = re.fullmatch(r'#?([A-Fa-f0-9]{6})', hex_color)
    if not match:
        return "\033[0m"
    r, g, b = [int(match.group(1)[i:i+2], 16) for i in (0, 2, 4)]
    return f"\033[38;2;{r};{g};{b}m"

VERSION = "1.3.1"
ENV_PATH = os.path.abspath(os.path.dirname(__file__))
config = {
  "moded": False,
  "debug": False,
  "debug_mode": "normal",
  "supports_color": True,
  "use_lucia_traceback": True,
  "warnings": True,
  "use_predefs": True,
  "print_comments": False,
  "allow_fetch": True,
  "execute_code_blocks": {
      "C": True,
      "ASM": True,
      "PY": True
  },
  "lucia_file_extensions": [".lucia", ".luc", ".lc", ".l"],
  "home_dir": ENV_PATH,
  "recursion_limit": 9999,
  "version": VERSION,
  "color_scheme": {
    "exception": "#F44350",
    "warning": "#FFC107",
    "debug": "#434343",
    "comment": "#757575",
    "input_arrows": "#136163",
    "input_text": "#BCBEC4",
    "output_text": "#BCBEC4",
    "info": "#9209B3"
  }
}

with open(f"{ENV_PATH}/config.json", "w") as file:
    json.dump(config, file, indent=2)

print("Environment activated.")