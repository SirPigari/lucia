import os
import sys
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    os.environ['TCL_LIBRARY'] = os.path.join(base_path, "tcl/tcl8.6")
    os.environ['TK_LIBRARY'] = os.path.join(base_path, "tcl/tk8.6")
else:
    os.environ['TCL_LIBRARY'] = r"E:\Python\Python313\tcl\tcl8.6"
    os.environ['TK_LIBRARY'] = r"E:\Python\Python313\tcl\tk8.6"
import requests
import zipfile
import shutil
from pathlib import Path
import json
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import _winapi as winapi
import threading
import subprocess
from io import BytesIO
import winreg as reg
import ctypes
import platform
import random
import winshell
import pythoncom
from win32com.client import Dispatch
import time
import traceback
import urllib.request

if getattr(sys, 'frozen', False):
    # If running as a bundled app, use _MEIPASS to get the resource path
    base_path = sys._MEIPASS
else:
    # If running normally (i.e. during development)
    base_path = os.path.join(os.path.dirname(__file__), "env\\assets")

os.chdir(base_path)


version = "1.0"


def is_python_installed():
    try:
        subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def install_python():
    python_installer_url = "https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe"
    installer_path = "python_installer.exe"

    print("Downloading Python 3.13.2...")
    urllib.request.urlretrieve(python_installer_url, installer_path)

    print("Installing Python 3.13.2...")
    subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"], check=True)
    os.remove(installer_path)

    print("Python 3.13.2 installed successfully. Please restart your terminal.")
    sys.exit(0)


def is_pyinstaller_installed():
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def install_pyinstaller():
    print("Installing pyinstaller...")
    subprocess.run(["python", "-m", "pip", "install", "pyinstaller"], check=True)
    print("PyInstaller installed successfully.")

def is_admin():
    """Check if the script is run as administrator."""
    if platform.system() == "Windows":
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    else:
        return os.geteuid() == 0


def run_as_admin():
    """Re-run the script with admin privileges."""
    if platform.system() == "Windows":
        # Command to run the script with admin privileges
        script = sys.executable + ' ' + __file__
        # Use subprocess to invoke the script in a hidden window
        subprocess.run(['powershell', '-Command', f'Start-Process cmd.exe -ArgumentList "/c {script}" -Verb RunAs -WindowStyle Hidden'])
    else:
        print("Linux/Unix systems are not supported.")


class Installer:
    def __init__(self, version="1.0"):
        self.version = version
        self.root = tk.Tk()
        if os.path.exists("installer.ico"):
            self.root.iconbitmap(os.path.join(base_path, "installer.ico"))
        self.root.title(f"Lucia Installer - {self.version}")
        self.root.geometry("625x385")
        self.root.resizable(False, False)

        self.default_path = Path(f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\LuciaAPL\\")
        self.installed_path = Path(self.default_path)

        self.installed_version = self.get_installed_version()

        self.add_image()

        self.frame_right = ttk.Frame(self.root)
        self.frame_right.place(relx=0.25, relwidth=0.75, relheight=1)

        self.title_label = ttk.Label(self.frame_right, text=f"Lucia Installer - Version {self.version}", font=("Helvetica", 16))
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.install_path_label = ttk.Label(self.frame_right, text="Install Path:")
        self.install_path_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.install_path_var = tk.StringVar()
        self.install_path_var.set(self.default_path)

        self.install_path_entry = ttk.Entry(self.frame_right, textvariable=self.install_path_var, width=50)
        self.install_path_entry.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.browse_button = ttk.Button(self.frame_right, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=2, column=1, padx=10, pady=5)

        self.precompile_var = tk.BooleanVar()
        self.precompile_checkbox = ttk.Checkbutton(self.frame_right, text="Compile to .exe", variable=self.precompile_var)
        self.precompile_checkbox.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="w")

        self.download_libraries_var = tk.BooleanVar()
        self.download_libraries_checkbox = ttk.Checkbutton(self.frame_right, text="Download Additional Libraries", variable=self.download_libraries_var)
        self.download_libraries_checkbox.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="w")

        self.add_to_path_var = tk.BooleanVar()
        self.add_to_path_checkbox = ttk.Checkbutton(self.frame_right, text="Add 'lucia' to PATH", variable=self.add_to_path_var)
        self.add_to_path_checkbox.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="w")

        self.install_button = ttk.Button(self.frame_right, text="Install", command=self.install)
        self.install_button.place(relx=0.05, rely=0.6, relwidth=0.2, height=25)

        if self.installed_version:
            self.show_existing_installation_options()

        self.close_button = ttk.Button(self.root, text="Close", command=self.on_closing)
        self.close_button.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def get_installed_version(self):
        try:
            newest_version = None
            versions = os.listdir(self.default_path)
            for version in versions:
                if version.startswith("lucia-Release"):
                    version = version.replace("lucia-Release", "")
                    if not newest_version or version > newest_version:
                        newest_version = version
            return newest_version
        except Exception as e:
            print(f"Error getting installed version: {e}")
            return None

    def add_image(self):
        image_path = f"{base_path}\\placeholder.png"
        try:
            img = Image.open(image_path)
            img = img.resize((156, 385), Image.LANCZOS)
            self.img = ImageTk.PhotoImage(img)
            image_label = ttk.Label(self.root, image=self.img)
            image_label.place(relheight=1, relwidth=0.25)
        except Exception as e:
            print(f"Error loading image: {e}")

    def show_existing_installation_options(self):
        if self.installed_version and self.version > self.installed_version:
            upgrade_button = ttk.Button(self.frame_right, text=f"Upgrade to {self.version}", command=self.upgrade)
            upgrade_button.place(relx=0.0, rely=0.6, relwidth=0.2, height=25)  # Simulating column 0
            return

        elif self.installed_version == self.version:
            self.install_button.destroy()
            self.frame_right.update_idletasks()
            self.frame_right.update()
            uninstall_button = ttk.Button(self.frame_right, text="Uninstall", command=self.uninstall)
            uninstall_button.place(relx=0.0, rely=0.6, relwidth=0.2, height=25)  # Simulating column 1

            modify_button = ttk.Button(self.frame_right, text="Repair or Modify", command=self.modify)
            modify_button.place(relx=0.25, rely=0.6, relwidth=0.3, height=25)  # Simulating column 2
            messagebox.showinfo("Info", "Lucia APL is already installed with the latest version.")
            return

        elif self.installed_version:
            self.install_button.destroy()
            self.frame_right.update_idletasks()
            self.frame_right.update()
            uninstall_button = ttk.Button(self.frame_right, text="Uninstall", command=self.uninstall)
            uninstall_button.place(relx=0.0, rely=0.6, relwidth=0.2, height=25)  # Simulating column 1

            modify_button = ttk.Button(self.frame_right, text="Repair or Modify", command=self.modify)
            modify_button.place(relx=0.25, rely=0.6, relwidth=0.3, height=25)  # Simulating column 2
            return

    def uninstall(self):
        try:
            if self.installed_path.exists():
                d = tk.Toplevel(master=self.root)
                d.title("Uninstalling Lucia")
                if os.path.exists("installer.ico"):
                    d.iconbitmap("installer.ico")
                d.geometry("300x100")
                d.resizable(False, False)
                d.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())

                download_bar = ttk.Progressbar(d, length=200, mode='determinate')
                download_bar.place(y=20, x=50)
                d.update_idletasks()

                def uninstall_process():
                        for i in range(8):
                            download_bar.step(100 // 9)
                            d.update_idletasks()
                            d.after(random.randint(100, 500))
                        shutil.rmtree(self.installed_path)
                        download_bar.step(100 // 9)
                        d.after(random.randint(500, 1000))
                        d.destroy()
                        messagebox.showinfo("Success", "Lucia has been uninstalled.")
                        self.root.quit()
                threading.Thread(target=uninstall_process, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during uninstallation: {e}")

    def modify(self):
        try:
            if self.installed_path.exists():
                shutil.rmtree(self.installed_path)
                self.install()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during modification: {e}")

    def upgrade(self):
        messagebox.showinfo("Upgrade", f"Upgrading Lucia to version {self.version}.")

    def browse_folder(self):
        folder_selected = filedialog.askdirectory(initialdir=self.default_path)
        if folder_selected:
            self.install_path_var.set(folder_selected)

    def install(self):
        d = tk.Toplevel(master=self.root)
        d.title("Installing Lucia")
        if os.path.exists("installer.ico"):
            d.iconbitmap("installer.ico")
        d.geometry("300x100")
        d.resizable(False, False)
        d.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())

        download_bar = ttk.Progressbar(d, length=200, mode='determinate')
        download_bar.place(y=20, x=50)
        d.update_idletasks()

        def install_process():
            install_path = self.install_path_var.get()
            os.makedirs(install_path, exist_ok=True)
            precompile = self.precompile_var.get()
            download_libraries = self.download_libraries_var.get()
            add_to_path = self.add_to_path_var.get()

            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            log_dir = os.path.join(install_path, f"lucia-Release{self.version}", "env", "logs")
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, f"{timestamp}.log")

            assets_dir = base_path

            # Function to write logs
            def write_log(message):
                with open(log_file, 'a', encoding='utf-8-sig') as log:
                    log.write(message + "\n")

            def log_exception():
                exc_type, exc_value, exc_tb = sys.exc_info()
                exception_details = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
                write_log(f"ERROR: {exception_details}")
                messagebox.showerror("Error", f"An error occurred. Check the log file at: {log_file}")
                d.destroy()

            steps = 5  # Including the unzip step
            if precompile:
                steps += 1
            if download_libraries:
                steps += 4
            if add_to_path:
                steps += 2
            step = 200 // steps
            download_bar.step(step)

            if not install_path:
                messagebox.showerror("Error", "Please select a valid install path.")
                d.destroy()
                return

            if not os.path.exists(install_path):
                messagebox.showerror("Error", "The install path does not exist.")
                d.destroy()
                return

            if not os.path.isdir(install_path):
                messagebox.showerror("Error", "The install path is not a directory.")
                d.destroy()
                return

            if not os.access(install_path, os.W_OK):
                messagebox.showerror("Error", "The install path is not writable.")
                d.destroy()
                return

            url = f"https://github.com/SirPigari/lucia/archive/refs/tags/Release{self.version}.zip"
            output_file = os.path.join(install_path, f"lucia_Release{self.version}.zip")

            try:
                print(f"Downloading {url}...")
                response = requests.get(url, stream=True)
                response.raise_for_status()

                with open(output_file, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)

                print(f"Downloaded successfully to {output_file}")
                download_bar.step(step)
                d.update_idletasks()
                assets_dir = os.path.join(install_path, f"lucia-Release{self.version}", "env\\assets")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Error downloading the release: {e}")
                d.destroy()
                write_log(f"ERROR: {str(e)}")
                log_exception()
                return

            try:
                with zipfile.ZipFile(output_file, 'r') as zip_ref:
                    zip_ref.extractall(install_path)
                print("Extraction completed.")
                download_bar.step(step)
                d.update_idletasks()
            except zipfile.BadZipFile as e:
                messagebox.showerror("Error", f"Error extracting the release: {e}")
                d.destroy()
                write_log(f"ERROR: {str(e)}")
                log_exception()
                return

            try:
                os.remove(output_file)
                print("Removed zip file.")
                download_bar.step(step)
                d.update_idletasks()
            except Exception as e:
                write_log(f"ERROR: {str(e)}")
                log_exception()
                print(f"Error removing zip file: {e}")

            try:
                with open(os.path.join(install_path, f"lucia-Release{self.version}\\env", "config.json"), 'w') as file:
                    config = {
                      "debug": False,
                      "use_lucia_traceback": True,
                      "warnings": True,
                      "print_comments": False,
                      "lucia_file_extensions": [".lucia", ".luc", ".lc", ".l"],
                      "home_dir": os.path.join(install_path, f"lucia-Release{self.version}\\env"),
                      "recursion_limit": 9999,
                      "version": self.version,
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
                    json.dump(config, file, indent=4)
                    print("Added config file.")
                    download_bar.step(step)
                    d.update_idletasks()
            except Exception as e:
                messagebox.showerror("Error", f"Error creating config file: {e}")
                d.destroy()
                write_log(f"ERROR: {str(e)}")
                log_exception()
                return

            if precompile:
                print("Compiling Lucia...")
                lucia_path = os.path.join(install_path, f"lucia-Release{self.version}")
                lucia_path_py = os.path.join(lucia_path, "lucia.py")
                lucia_path_exe = os.path.join(lucia_path, "lucia.exe")
                print(lucia_path_py)

                if not os.path.exists(lucia_path_py):
                    messagebox.showerror("Error", "Lucia source file not found for compilation.")
                    d.destroy()
                    write_log(f"ERROR: {str(e)}")
                    log_exception()
                    return

                os.makedirs(os.path.join(lucia_path, "env\\build"), exist_ok=True)

                try:
                    if not is_python_installed():
                        messagebox.showerror("Error", "Python is not installed.")
                        d.destroy()
                        return
                    if not is_pyinstaller_installed():
                        messagebox.showerror("Error", "PyInstaller is not installed.")
                        d.destroy()
                        return

                    subprocess.run([
                        "pyinstaller",
                        "--onefile", f"--icon={os.path.join(assets_dir, 'installer.ico')}",
                        "--add-data", f"{lucia_path}{os.pathsep}.",
                        "--distpath", lucia_path,  # Set output directory to lucia_path
                        "--workpath", os.path.join(lucia_path, "env\\build"),  # Avoid cluttering main dir
                        "--specpath", os.path.join(lucia_path, "env\\build"),  # Keep spec file in build dir
                        lucia_path_py
                    ], check=True)

                    print(f"Compilation successful. Executable saved to {lucia_path_exe}")
                    download_bar.step(step)
                    d.update_idletasks()

                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Error", f"Compilation failed: {e}")
                    d.destroy()
                    write_log(f"ERROR: {str(e)}")
                    log_exception()
                    return
                except Exception as e:
                    messagebox.showerror("Error", f"Error compiling Lucia: {e}")
                    d.destroy()
                    write_log(f"ERROR: {str(e)}")
                    log_exception()
                    return
            if download_libraries:
                url = f"https://github.com/SirPigari/lucia/releases/download/Release{self.version}/Lib.zip"
                path = os.path.join(install_path, f"lucia-Release{self.version}", "env\\Lib")
                print(f"Downloading {url}...")

                response = requests.get(url)
                response.raise_for_status()
                download_bar.step(step)
                d.update_idletasks()

                with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
                    temp_dir = os.path.join(install_path, "temp_lib")
                    os.makedirs(temp_dir, exist_ok=True)

                    zip_ref.extractall(temp_dir)

                    extracted_files = os.listdir(temp_dir)
                    download_bar.step(step)
                    d.update_idletasks()

                    if extracted_files and extracted_files[0] == 'Lib' and os.path.isdir(os.path.join(temp_dir, 'Lib')):
                        lib_dir = os.path.join(temp_dir, 'Lib')
                        for root, dirs, files in os.walk(lib_dir):
                            for file in files:
                                temp_file = os.path.join(root, file)
                                target_file = os.path.join(path, os.path.relpath(temp_file, lib_dir))

                                os.makedirs(os.path.dirname(target_file), exist_ok=True)

                                if os.path.exists(target_file):
                                    os.remove(target_file)

                                shutil.move(temp_file, target_file)
                    else:
                        for root, dirs, files in os.walk(temp_dir):
                            for file in files:
                                temp_file = os.path.join(root, file)
                                target_file = os.path.join(path, os.path.relpath(temp_file, temp_dir))

                                os.makedirs(os.path.dirname(target_file), exist_ok=True)

                                if os.path.exists(target_file):
                                    os.remove(target_file)

                                shutil.move(temp_file, target_file)
                    download_bar.step(step)
                    d.update_idletasks()
                    shutil.rmtree(temp_dir)
                    download_bar.step(step)
                    d.update_idletasks()

                download_bar.step(step)
                d.update_idletasks()
                print(f"Downloaded libraries successfully to {path}")
            if add_to_path:
                print("Adding 'lucia' to PATH...")
                lucia_path = os.path.join(install_path, f"lucia-Release{self.version}")
                lucia_path_ = os.path.join(lucia_path, "lucia.exe")
                if not os.path.exists(lucia_path_):
                    lucia_path_ = os.path.join(lucia_path, "lucia.py")

                if not os.path.exists(lucia_path):
                    messagebox.showerror("Error", "Lucia installation not found.")
                    d.destroy()
                    return
                try:
                    pythoncom.CoInitialize()
                    current_path = os.environ.get("PATH", "")

                    desktop = winshell.desktop()
                    shortcut_path = os.path.join(desktop, f"Lucia-{self.version}.lnk")

                    shell = Dispatch('WScript.Shell')
                    shortcut = shell.CreateShortcut(shortcut_path)
                    shortcut.TargetPath = lucia_path_
                    shortcut.WorkingDirectory = os.path.dirname(lucia_path_)
                    shortcut.Save()

                    print(f"Shortcut 'Lucia-{self.version}' created successfully on the desktop.")

                    if lucia_path not in current_path:
                        new_path = f"{lucia_path};{current_path}"
                        print(new_path)
                        subprocess.run(f'setx PATH "{new_path}"', shell=True, check=True)
                        print(os.environ.get("PATH"))
                        print(f"Added {lucia_path} to PATH.")
                        messagebox.showinfo("Success", f"{lucia_path} has been added to PATH.")
                    else:
                        messagebox.showinfo("Info", f"{lucia_path} is already in PATH.")
                except Exception as e:
                    print(f"Error modifying PATH: {e}")
                    messagebox.showerror("Error", f"Failed to add {lucia_path} to PATH.\n{str(e)}")
                    download_bar.step(step)
                    d.update_idletasks()
                    write_log(f"ERROR: {str(e)}")
                    log_exception()
                print("Lucia added to PATH successfully.")
                download_bar.step(step)
                d.update_idletasks()

            d.destroy()
            print("Installation completed.")
            messagebox.showinfo("Success", f"Lucia APL {self.version} has been installed at {install_path}.")
            self.root.quit()

        threading.Thread(target=install_process, daemon=True).start()

    def on_closing(self):
        if messagebox.askyesno(f"Lucia Installer - {self.version}", "Are you sure you want to quit?", icon='warning'):
            self.root.quit()

if __name__ == "__main__":
    if not is_python_installed():
        install_python()
    else:
        print("Python is already installed.")

    if not is_pyinstaller_installed():
        install_pyinstaller()
    else:
        print("PyInstaller is already installed.")
    print(os.environ.get("PATH", ""))
    os.chdir(os.path.dirname(__file__))

    if (len(sys.argv) > 1) and (sys.argv[1] == "--no-admin"):
        Installer(version)
        sys.exit(0)
    if not is_admin():
        run_as_admin()
        sys.exit(0)
    else:
        os.chdir(os.path.dirname(__file__))
        Installer(version)