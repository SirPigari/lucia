import sys
import os
import shutil
import psutil
from tqdm import tqdm
import tempfile
import pathspec
import subprocess


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
LUCIA_ICON = os.path.abspath("env/assets/lucia_icon_rounded.ico").replace("\\", "/")
INSTALLER_ICON2 = os.path.abspath("env/assets/installer2.ico").replace("\\", "/")
DATA_PATH = os.path.abspath(".").replace("\\", "/")
FILE = os.path.abspath("lucia.py").replace("\\", "/")
FILE2 = os.path.abspath("installer.py").replace("\\", "/")
EXE_PATH = os.path.join(BIN_PATH, "lucia.exe").replace("\\", "/")
VERSION = "1.1.2"

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

installer_command = [f"{NSIS_PATH}\\makensis.exe", NSI_INSTALLER_PATH]

print(installer_command)

subprocess.run(installer_command, shell=True)

print("Build successful.")

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
