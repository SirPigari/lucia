import sys
import os
import shutil
import psutil
from tqdm import tqdm
import tempfile
import pathspec
import subprocess
import json


def kill_process(process_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'] == process_name:
            try:
                proc.kill()
                print(f"Killed process: {process_name}")
            except Exception as e:
                print(f"Failed to kill {process_name}: {e}")


def delete_folder_with_progress(folder_path):
    if os.path.exists(folder_path):
        print(f"Deleting folder: {folder_path}")
        files = list(os.scandir(folder_path))
        print(f"Found {len(files)} files.")
        with tqdm(total=len(files), desc="Deleting build folder", unit=" file") as pbar:
            for entry in files:
                try:
                    if entry.is_file() or entry.is_symlink():
                        os.unlink(entry.path)
                    elif entry.is_dir():
                        shutil.rmtree(entry.path)
                except Exception as e:
                    print(f"Error deleting {entry.path}: {e}")
                pbar.update(1)
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)


os.chdir(os.path.dirname(__file__))
os.chdir("../")

BUILD_PATH = os.path.abspath("env/build").replace("\\", "/")
BIN_PATH = os.path.abspath("env/bin").replace("\\", "/")
LUCIA_ICON = os.path.abspath("env/assets/lucia_logo_small.ico").replace("\\", "/")
INSTALLER_ICON2 = os.path.abspath("env/assets/installer2.ico").replace("\\", "/")
DATA_PATH = os.path.abspath(".").replace("\\", "/")
FILE = os.path.abspath("lucia.py").replace("\\", "/")
FILE2 = os.path.abspath("installer.py").replace("\\", "/")
EXE_PATH = os.path.join(BIN_PATH, "lucia.exe").replace("\\", "/")
VERSION = "1.3.1"

kill_process("lucia.exe")

print("Building lucia.exe...")

print(BUILD_PATH)
print(BIN_PATH)
print(LUCIA_ICON)
print(DATA_PATH)
print(FILE)
print(EXE_PATH)

command = (f"python -m PyInstaller --noconfirm --onefile --clean --log-level TRACE "
           f"--icon={LUCIA_ICON} "
           f"--distpath \"{BIN_PATH}\" --workpath \"{BUILD_PATH}\" "
           f"--specpath \"{BUILD_PATH}\" \"{FILE}\""
           )

print(command)

os.system(command)

NSIS_PATH = "C:\\Program Files (x86)\\NSIS"
NSI_INSTALLER_PATH = os.path.abspath("installer/LuciaInstaller.nsi").replace("\\", "/")
CONFIG_PATH = os.path.abspath("env/config.json").replace("\\", "/")
OG_CONFIG = {}

with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
    try:
        OG_CONFIG = json.load(config_file)
    except Exception as e:
        print(f"Error reading config file: {e}")
        exit(-1)

ENV_PATH = "NOT_ACTIVATED"
config_to_place = {
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

with open(CONFIG_PATH, "w") as file:
    json.dump(config_to_place, file, indent=2)

RUN_FILE_PATH = os.path.abspath("env/bin/tcc/run.txt").replace("\\", "/")
OG_RUN_FILE = ""
with open(RUN_FILE_PATH, "r", encoding="utf-8") as run_file:
    try:
        OG_RUN_FILE = run_file.read()
    except Exception as e:
        print(f"Error reading run file: {e}")
        exit(-1)
with open(RUN_FILE_PATH, "w", encoding="utf-8") as run_file:
    try:
        run_file.write("{tcc_path} -run {source_path}")
    except Exception as e:
        print(f"Error writing run file: {e}")
        exit(-1)

print("Building installer...")
installer_command = [f"{NSIS_PATH}\\makensis.exe", NSI_INSTALLER_PATH]

print(installer_command)

subprocess.run(installer_command, shell=True)

print("Build successful.")

with open(CONFIG_PATH, "w", encoding="utf-8") as config_file:
    try:
        json.dump(OG_CONFIG, config_file, indent=2)
    except Exception as e:
        print(f"Error writing config file: {e}")
        exit(-1)

with open(RUN_FILE_PATH, "w", encoding="utf-8") as run_file:
    try:
        run_file.write(OG_RUN_FILE)
    except Exception as e:
        print(f"Error writing run file: {e}")
        exit(-1)

os.chdir(DATA_PATH)
TEST_PATH = os.path.abspath("tests").replace("\\", "/")
TEST_FILES = os.listdir(TEST_PATH)

print("Starting tests...")
print(TEST_FILES)
print(TEST_PATH)
for file in TEST_FILES:
    if os.path.isfile(f"tests/{file}"):
        os.system(f"{EXE_PATH} {os.path.abspath(f"tests/{file}").replace('\\', '/')} --timer")

print("Tests completed.")

print("Cleaning up build folder...")
delete_folder_with_progress(BUILD_PATH)

print("Starting lucia.exe...")
os.system(EXE_PATH)
