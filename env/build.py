import sys
import os
import shutil
import psutil
from tqdm import tqdm
import tempfile
import pathspec


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
INSTALLER_ICON = os.path.abspath("env/assets/installer.ico").replace("\\", "/")
DATA_PATH = os.path.abspath(".").replace("\\", "/")
FILE = os.path.abspath("lucia.py").replace("\\", "/")
EXE_PATH = os.path.join(BIN_PATH, "lucia.exe").replace("\\", "/")

kill_process("lucia.exe")

print("Building lucia.exe...")

print(BUILD_PATH)
print(BIN_PATH)
print(INSTALLER_ICON)
print(DATA_PATH)
print(FILE)
print(EXE_PATH)


paths = [
    "env\\Lib",
	"env\\activate.py",
	"env\\config.json",
	"env\\build.py",
	"env\\assets\\installer.ico",
    "lucia.py",
    "interpreter.py",
    "pparser.py",
    "lexer.py",
    "LICENSE",
    "installer.py",
]

TEMP_PATH = "temp/"
os.makedirs(TEMP_PATH, exist_ok=True)
for p in paths:
	shutil.copy(p, os.path.join(TEMP_PATH, p))

for root, dirs, files in os.walk(TEMP_PATH):
	for file in files:
		if file.endswith(".pyc"):
			os.remove(os.path.join(root, file))

PATHS = " ".join([f"--add-data \"{os.path.abspath(p).replace('\\', '/')}\"{os.pathsep}{p}" for p in paths])


command = (f"python -m PyInstaller --noconfirm --noconsole --onefile --clean "
	f"--icon={INSTALLER_ICON} {PATHS} "
	f"--distpath \"{BIN_PATH}\" --workpath \"{BUILD_PATH}\" "
	f"--specpath \"{BUILD_PATH}\" \"{FILE}\"")

print(command)

os.system(command)