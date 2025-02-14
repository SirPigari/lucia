import os
import sys
import ctypes
import shutil
import subprocess
import winreg
import tkinter as tk

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    script = sys.argv[0]
    params = " ".join(f'"{arg}"' for arg in sys.argv[1:])

    try:
        subprocess.run(["powershell", "Start-Process", "python", f"'{script}' {params}", "-Verb", "RunAs"], check=True)
    except subprocess.CalledProcessError:
        print("Failed to elevate privileges.")
    sys.exit()


def add_to_path(script_path):
    script_dir = os.path.dirname(script_path)
    os.chdir(script_dir)

    os.environ["PATH"] += os.pathsep + script_dir

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"System\CurrentControlSet\Control\Session Manager\Environment",
                            0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
            current_path, _ = winreg.QueryValueEx(key, "Path")

            if script_dir not in current_path:
                new_path = current_path + os.pathsep + script_dir
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                print(f"Successfully added {script_dir} to PATH.")
            else:
                print(f"{script_dir} is already in PATH.")
        os.system(
            'powershell -Command "$env:Path = [System.Environment]::GetEnvironmentVariable(\'Path\', [System.EnvironmentVariableTarget]::Machine)"')
    except PermissionError:
        print("Permission denied! Run this script as an administrator.")
    except Exception as e:
        print(f"An error occurred: {e}")


def copy_files_to_appdata():
    appdata_path = os.getenv('APPDATA')
    lucia_dir = os.path.join(appdata_path, 'Lucia')

    if not os.path.exists(lucia_dir):
        os.makedirs(lucia_dir)
        print(f"Created directory: {lucia_dir}")

    for item in os.listdir("."):
        s = os.path.join(".", item)
        d = os.path.join(lucia_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    print(f"Files copied to {lucia_dir}.")
    return lucia_dir


if __name__ == "__main__":
    if not is_admin():
        run_as_admin()

    lucia_dir = copy_files_to_appdata()

    add_to_path(lucia_dir)
