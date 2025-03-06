import requests
import os
import sys
import json
import zipfile
import shutil
from io import BytesIO
import platform
import winreg
from tqdm import tqdm

VERSION = "1.0"
INSTALL_PATH = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Programs\\LuciaAPL\\"
BIN_PATH = os.path.join(INSTALL_PATH, "bin")

os.system("cls" if platform.system() == "Windows" else "clear")
os.system(f"title Lucia Installer - {VERSION}")


FAKE_TEMP = "" # os.path.abspath("env/assets/fake_temp.zip")


def add_to_path(bin_path):
    bin_path = os.path.abspath(bin_path)

    if platform.system() == "Windows":
        reg_key = r"Environment"

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_READ) as key:
            try:
                current_path, _ = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                current_path = ""

        if bin_path in current_path:
            print("BIN_PATH is already in user PATH.")
            return

        new_path_value = f"{current_path};{bin_path}" if current_path else bin_path
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path_value)

        print(f"Successfully added {bin_path} to user PATH. Restart your terminal for changes to take effect.")

    else:
        shell_rc_file = os.path.expanduser("~/.bashrc")
        export_line = f'export PATH="{bin_path}:$PATH"\n'

        if os.path.exists(shell_rc_file):
            with open(shell_rc_file, "r") as f:
                if export_line in f.readlines():
                    print("BIN_PATH is already in user PATH.")
                    return

        with open(shell_rc_file, "a") as f:
            f.write(f"\n# Added by script\n{export_line}")

        print(f"Successfully added {bin_path} to user PATH. Restart your shell or run 'source {shell_rc_file}'.")


def install():
    if os.path.exists(INSTALL_PATH):
        shutil.rmtree(INSTALL_PATH)
    if FAKE_TEMP and os.path.exists(FAKE_TEMP):
        print("Using fake temp zip for installation.")
        zip_file_path = FAKE_TEMP
    else:
        github_url = f"https://github.com/SirPigari/lucia/archive/refs/tags/Release{VERSION}.zip"
        extract_to = INSTALL_PATH

        os.makedirs(extract_to, exist_ok=True)

        response = requests.get(github_url, stream=True)
        if response.status_code == 200:
            zip_file_path = os.path.join(extract_to, "temp.zip")

            total_size = int(response.headers.get('Content-Length', 0))

            if not os.path.exists(zip_file_path):
                with open(zip_file_path, "wb") as file:
                    with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading", dynamic_ncols=True,
                              file=sys.stdout) as pbar:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                            pbar.update(len(chunk))
        else:
            print("Failed to download file. Check your internet connection.")
            return

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        temp_extract_dir = os.path.join(INSTALL_PATH, "temp_extract")
        os.makedirs(temp_extract_dir, exist_ok=True)

        zip_ref.extractall(temp_extract_dir)

        folder_name = f"lucia-Release{VERSION}"

        if folder_name:
            extracted_folder_path = os.path.join(temp_extract_dir, folder_name)

            print(f"Extracted folder: {extracted_folder_path}")

            release_dir = extracted_folder_path
            if os.path.isdir(release_dir):
                for item in os.listdir(release_dir):
                    s = os.path.join(release_dir, item)
                    d = os.path.join(INSTALL_PATH, item)
                    if os.path.isdir(s):
                        shutil.move(s, d)
                    else:
                        shutil.move(s, d)
            else:
                print("Failed to find extracted folder.")
                sys.exit(1)

        shutil.rmtree(temp_extract_dir)
    if not os.path.exists(FAKE_TEMP):
        os.remove(zip_file_path)  # Only remove the real downloaded file
    print("Download, extraction, and cleanup complete.")

    ENV_PATH = os.path.join(INSTALL_PATH, "env")
    config = {
        "moded": False,
        "debug": False,
        "debug_mode": "normal",
        "supports_color": True,
        "use_lucia_traceback": True,
        "warnings": True,
        "print_comments": False,
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

    os.makedirs(ENV_PATH, exist_ok=True)
    with open(f"{ENV_PATH}\\config.json", "w") as file:
        json.dump(config, file, indent=2)

    print("Environment activated.")
    add_to_path(BIN_PATH)
    print(f"Lucia installed to {INSTALL_PATH}")


if __name__ == "__main__":
    while True:
        print("----- Lucia Installer -----")
        print(" 1 - Install Lucia")
        print(" 2 - Uninstall Lucia")
        print(" 3 - Install using release zip")
        print(" 4 - Change INSTALL_PATH")
        print(" 5 - Help")
        print(" 6 - Exit")
        print("---------------------------")
        choice = input("Enter your choice: ")
        if choice == "1":
            print("Installing Lucia, do not close this terminal session...")
            try:
                install()
            except Exception as e:
                print(f"Failed to install Lucia: {e}")
                sys.exit(1)
        elif choice == "2":
            print("Uninstalling Lucia...")
            if os.path.exists(INSTALL_PATH):
                total_size = sum(
                    os.path.getsize(os.path.join(root, file)) for root, dirs, files in os.walk(INSTALL_PATH) for file in
                    files)
                with tqdm(total=total_size, unit='B', unit_scale=True, desc="Uninstalling", dynamic_ncols=True, file=sys.stdout) as pbar:
                    shutil.rmtree(INSTALL_PATH, onerror=lambda func, path, excinfo: pbar.update(os.path.getsize(path)))
                    pbar.update(total_size)
                print("Lucia uninstalled.")
            else:
                print("Lucia is not installed.")
        elif choice == "3":
            new_path = input("Enter the release zip path: ")
            if os.path.exists(new_path):
                FAKE_TEMP = new_path
                print(f"Release zip path: {FAKE_TEMP}")
            else:
                print("Invalid path.")
        elif choice == "4":
            new_path = input(f"Enter new INSTALL_PATH ('{INSTALL_PATH}'): ")
            if os.path.exists(new_path):
                INSTALL_PATH = new_path
                BIN_PATH = os.path.join(INSTALL_PATH, "bin")
                print(f"New INSTALL_PATH: {INSTALL_PATH}")
            else:
                print("Invalid path.")
        elif choice == "5":
            print("Help:")
            print("---------------------------")
            print("Variables:")
            print(f" - VERSION: The version of Lucia to install. Current version: {VERSION}")
            print(f" - INSTALL_PATH: The path where Lucia will be installed. Current path: {INSTALL_PATH}")
            print(f" - BIN_PATH: The path where Lucia binaries will be stored. Current path: {BIN_PATH}")
            print(f" - FAKE_TEMP: A fake temp zip file path for testing purposes. Also known as 'Release zip'. Current path: {FAKE_TEMP}")
            print("---------------------------")
            print("Functions:")
            print(" 1 - Install Lucia: Downloads and installs Lucia.")
            print(" 2 - Uninstall Lucia: Removes Lucia from the system.")
            print(" 3 - Install using fake temp zip: Installs Lucia using a release zip file.")
            print(" 4 - Change INSTALL_PATH: Changes the installation path.")
            print(" 5 - Help: Shows this help message.")
            print(" 6 - Exit: Exits the installer.")
        elif choice == "6":
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice. Exiting...")
            sys.exit()
        print("---------------------------")
        print("\n")
