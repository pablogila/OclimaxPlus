"""
OclimaxPlus. Simulate neutron scattering with OCLIMAX for lots of files.
Copyright (C) 2023  Pablo Gila-Herranz
If you find this code useful, a citation would be awesome :D
Gila-Herranz, Pablo. “OclimaxPlus”, 2023. https://github.com/pablogila/OclimaxPlus

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import os
import subprocess
import shutil
import time



def version():
    return "vOP.2023.05.10.1300"



jobs_file = 'OclimaxPlus_JOBS.txt'



# This function will read the input file and execute the batch jobs
def jobs(job_file):
    try:
        is_file_empty = True
        with open(job_file, 'r') as f:
            lines = f.readlines()
        for line in lines[0:]:
            line = line.split(',')
            line = [x.strip() for x in line]
            if line[0].startswith('#') or line[0] == '':
                continue
            if len(line) == 2:
                is_file_empty = False
                print("")
                print("\n Starting new job: " + line[0] + ", " + line[1])
                print("")
                main(line[0], line[1])
            else:
                print("")
                print(" ERROR:  Unknown job. Check this line:")
                print(line)
                print(" Skipping to the next job...")
                print("")
                continue
        if is_file_empty:
            print("")
            print(" WARNING:  '" + job_file + "' batch job file was found,")
            print(" but it is empty. Please fill it and try again.")
            print("")
            exit()
    except FileNotFoundError:
        with open(job_file, 'w') as f:
            f.write("# ----------------------------------------------------------------------------------------------\n")
            f.write("# OclimaxPlus batch job file\n")
            f.write("# Copyright (C) 2023  Pablo Gila-Herranz\n")
            f.write("# If you find this code useful, a citation would be awesome :D\n")
            f.write("# Gila-Herranz, Pablo. “OclimaxPlus”, 2023. https://github.com/pablogila/OclimaxPlus\n")
            f.write("# This is free software, and you are welcome to redistribute it under GNU General Public License\n")
            f.write("#\n")
            f.write("# Write here all the OclimaxPlus jobs that you want to execute, following this format:\n")
            f.write("# data_directory, phonon_files\n")
            f.write("# Note that the data_directory should be inside a folder called 'data'\n")
            f.write("#\n")
            f.write("# Example:\n")
            f.write("# data_pbe-d3, cc-2_PhonDOS.phonon\n")
            f.write("# ----------------------------------------------------------------------------------------------\n")
        print("")
        print(" First time running OclimaxPlus, huh?")
        print(" The batch job file was not found, so an empty one called")
        print(" '" + job_file + "' was created with examples")
        print("")
        exit()



def main(data_directory='data_pbe-d3', phonon_files='cc-2_PhonDOS.phonon'):

    # Get the folder names
    working_path = os.getcwd()
    data = 'data'
    out = 'out'
    output_directory = 'OUT_oclimax_' + data_directory
    temp_directory = 'TEMP_oclimax_' + data_directory
    input_folder = os.path.join(working_path, data, data_directory)
    output_folder = os.path.join(working_path, out, output_directory)
    temp_folder = os.path.join(working_path, out, temp_directory)

    time_start_main = time.time()

    #############################################################
    #  Rename and copy the *.phonon files to the current folder
    #############################################################

    print("\n Renaming and copying the *.phonon files to the current folder...\n")

    # Iterate over the subfolders in the input folder
    for folder_name in os.listdir(input_folder):
        folder_path = os.path.join(input_folder, folder_name)

        # Check if the item in the folder_path is a directory
        if os.path.isdir(folder_path):
            file_path = os.path.join(folder_path, phonon_files)
            output_file_name = folder_name + '.phonon'
            output_file_path = os.path.join(working_path, output_file_name)

            # Copy the file to the output folder with the new name
            shutil.copy(file_path, output_file_path)

    #############################################################
    #  Execute the OCLIMAX commands for all *.phonon files
    #############################################################

    print(" Executing OCLIMAX for all *.phonon files...\n")

    # Iterate over the .phonon files in the folder
    for filename in os.listdir(working_path):
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

    #############################################################
    #  Move the *.phonon and *.csv files to the output folder
    #############################################################

    # Create the output folders if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # Get the list of files in the current directory
    files = os.listdir(working_path)

    # Move files with extensions ".phonon" and ".csv" to the output folder
    for file in files:
        if file.endswith((".phonon", ".oclimax", ".params")):
            file_old = os.path.join(working_path, file)
            temp_path = os.path.join(temp_folder, file)
            shutil.move(file_old, temp_path)
        if file.endswith(".csv"):
            file_old = os.path.join(working_path, file)
            output_path = os.path.join(output_folder, file)
            shutil.move(file_old, output_path)

    print("")
    print(" Job finished in", round(time.time() - time_start_main, 1), "seconds")
    print("")



if (not os.path.isfile('oclimax.bat')) or (not os.path.isfile('oclimax_convert.exe')) or (not os.path.isfile('oclimax_run.exe')) or (not os.path.isfile('oclimax_plot.exe')):
    if os.path.isfile('oclimax.win') and os.path.isfile('oclimax_convert.exe') and os.path.isfile('oclimax_run.exe') and os.path.isfile('oclimax_plot.exe'):
        print("\n ERROR:  'oclimax.win' was found, but you must rename it as 'oclimax.bat'\n")
    else:
        print("\n ERROR:  OCLIMAX files not found. Required files are:")
        print(" oclimax.bat (renamed from oclimax.win), oclimax_convert.exe, oclimax_run.exe, oclimax_plot.exe")
        print(" Download from: https://sites.google.com/site/ornliceman/download\n")
    exit()



time_start = time.time()


jobs(jobs_file)


print("")
print(" All jobs finished in", round(time.time() - time_start, 1), "seconds\n")
print("")

