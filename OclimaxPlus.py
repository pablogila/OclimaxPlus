import os
import subprocess

# Get the current working directory
folder_path = os.getcwd()

# Iterate over the .phonon files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.phonon'):
        # Extract the base name of the file without the extension
        base_name = os.path.splitext(filename)[0]
        
        # Construct the PowerShell commands
        convert_command = f".\\oclimax_convert.exe -c {filename} -o {base_name}"
        run_command = f".\\oclimax_run.exe {base_name}.oclimax {base_name}.params"
        
        # Execute the first PowerShell command
        process = subprocess.Popen(['powershell', '-Command', convert_command])
        process.communicate()  # Wait for the process to finish
        
        # Execute the second PowerShell command
        process = subprocess.Popen(['powershell', '-Command', run_command])
        process.communicate()  # Wait for the process to finish
