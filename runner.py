import os
import subprocess

directory_path = '/commandline runners'

py_files = [file for file in os.listdir(directory_path) if file.endswith('.py')]
for file in py_files:
    file_path = os.path.join(directory_path, file)
    try:
        subprocess.run(['python', file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {file}: {e}")

