import os
import re

os.chdir("../../")

files = [
    "env/config.json",
    "env/helpers/build.py",
    "env/activate.py",
    "installer/LuciaInstaller.nsi",
    "README.md",
    "env/Docs/language-syntax.md",
    "env/Docs/config-guide.md",
    "lucia.py"
]

# Regex: matches '1.2' or "1.2.3" with either quotes
version_pattern = re.compile(r'["\'](\d+\.\d+(?:\.\d+)?)["\']')

versions_found = set()

for file in files:
    if not os.path.exists(file):
        print(f"File not found: {file}")
        continue
    with open(file, "r") as f:
        content = f.readlines()

    for i, line in enumerate(content):
        if "version" in line.lower():
            match = version_pattern.search(line)
            if match:
                version_str = match.group(1)
                versions_found.add(version_str)
                print(f"Found version in {file} line {i + 1}: '{version_str}'")

print(f"Current version(s) found: {list(versions_found)}")

version = input("Enter the new version number: ")
old_version = input("Enter the old version number: ")

for file in files:
    with open(file, "r") as f:
        content = f.readlines()

    with open(file, "w") as f:
        for i, line in enumerate(content):
            new_line = line.replace(f'"{old_version}"', f'"{version}"')
            new_line = new_line.replace(f"'{old_version}'", f"'{version}'")
            f.write(new_line)
            if new_line != line:
                print(f"Updated {file} line {i + 1}: {line.strip()} -> {new_line.strip()}")
