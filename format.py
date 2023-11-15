import subprocess
import os


def code_format(path):
    try:
        # Create a list to store target files for code formatting
        target_files = []

        # Traverse the directory tree rooted at path
        for root, dirs, files in os.walk(path):
            for file in files:
                # Check if the file is a Python file and not inside a "venv" directory
                if file.endswith(".py") and root.find("venv") == -1:
                    target_files.append(os.path.join(root, file))

        # Iterate over the target files and apply code formatting using Black
        for file in target_files:
            command = f"black {file}"
            print(command)
            subprocess.run(command, shell=True)

        print("code_format done")
    except Exception as e:
        print(e)


def make_requirements_txt(path):
    try:
        command = f"pip freeze > {os.path.join(path, 'requirements.txt')}"
        subprocess.run(command, shell=True)

        print("requirements.txt done")
    except Exception as e:
        print(e)


code_format(os.path.dirname(__file__))
make_requirements_txt(os.path.dirname(__file__))
