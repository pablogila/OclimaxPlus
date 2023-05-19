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
    return "vOP.2023.05.19.1330"



jobs_file = 'OclimaxPlus_JOBS.txt'



# This function will read the input file and execute the batch jobs
def jobs(job_file):
    current_directory = os.getcwd()
    job_file_path = os.path.join(current_directory, job_file)
    if os.path.isfile(job_file_path):
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
                print(" ------------------------------------------------------------")
                print(" Starting new job: " + line[0] + ", " + line[1])
                print(" ------------------------------------------------------------")
                print("")
                main(line[0], line[1])
            else:
                is_file_empty = False
                error_job_unknown(line)
                continue
        if is_file_empty:
            error_jobfile_empty(job_file)
            exit()
    else:
        error_jobfile_missing(job_file)
        exit()


def error_job_unknown(line):
    print("")
    print(" ------------------------------------------------------------")
    print(" ERROR:  Unknown job. Check this line:")
    print(' ' + str(line))
    print(" Skipping to the next job...")
    print(" ------------------------------------------------------------")
    print("")


def error_jobfile_empty(job_file):
    print("")
    print(" ------------------------------------------------------------")
    print(" WARNING:  '" + job_file + "' batch job file was found,")
    print(" but it is empty. Please fill it and try again.")
    print(" ------------------------------------------------------------")
    print("\n")


def error_oclimax_missing():
    print("")
    print(" ------------------------------------------------------------")
    print(" ERROR:  OCLIMAX files not found. Required files are:")
    print(" oclimax.bat (renamed from oclimax.win), oclimax_convert.exe, oclimax_run.exe, oclimax_plot.exe")
    print(" Download from: https://sites.google.com/site/ornliceman/download")
    print(" ------------------------------------------------------------")
    print("")


def error_oclimax_rename():
    print("")
    print(" ------------------------------------------------------------")
    print(" ERROR:  'oclimax.win' was found, but you must rename it as 'oclimax.bat'")
    print(" ------------------------------------------------------------")
    print("")


def error_folder_missing(folder):
    print("")
    print(" ------------------------------------------------------------")
    print(" ERROR:  '" + folder + "' folder is missing.")
    print(" Skipping to the next job...")
    print(" ------------------------------------------------------------")
    print("")


def error_files_missing(files):
    print("")
    print(" ------------------------------------------------------------")
    print(" WARNING:  missing file/s:")
    for file in files:
        print(" " + file)
    print(" ------------------------------------------------------------")
    print("")


def warning_moving_unfinished(unfinished_directory):
    print("")
    print(" ------------------------------------------------------------")
    print(" WARNING:  Moving old files to '" + unfinished_directory + "' folder")
    print(" ------------------------------------------------------------")
    print("")


def error_jobfile_missing(job_file):
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
    print(" ------------------------------------------------------------")
    print(" First time running OclimaxPlus, huh?")
    print(" The batch job file was not found, so an empty one called")
    print(" '" + job_file + "' was created with examples")
    print(" ------------------------------------------------------------")
    print("\n")


def main(data_directory='data_pbe-d3', phonon_files='cc-2_PhonDOS.phonon'):

    # Get the folder names
    working_path = os.getcwd()
    data = 'data'
    out = 'out'
    output_directory = 'OUT_oclimax_' + data_directory
    temp_directory = 'TEMP_oclimax_' + data_directory
    unfinished_directory = 'UNFINISHED_FILES'
    input_folder = os.path.join(working_path, data, data_directory)
    output_folder = os.path.join(working_path, out, output_directory)
    temp_folder = os.path.join(working_path, out, temp_directory)
    error_log = 'oclimax_ERRORS_' + data_directory + '.txt'
    error_file = os.path.join(working_path, out, error_log)

    unfinished_folder = os.path.join(working_path, unfinished_directory)

    time_start_main = time.time()


    # Clean the working directory from unfinished files
    files_start = os.listdir(working_path)
    warning_unfinished = False
    for file in files_start:
        if file.endswith((".phonon", ".oclimax", ".params", ".csv")):
            warning_unfinished = True
            if not os.path.exists(unfinished_folder):
                os.makedirs(unfinished_folder)
            unfinished_old = os.path.join(working_path, file)
            unfinished_path = os.path.join(unfinished_folder, file)
            shutil.move(unfinished_old, unfinished_path)
    if warning_unfinished:
        warning_moving_unfinished(unfinished_directory)


    if not os.path.isdir(input_folder):
        error_folder_missing(data_directory)
        return

    #############################################################
    #  Rename and copy the *.phonon files to the current folder
    #############################################################

    print("\n Renaming and copying the *.phonon files to the current folder...\n")

    # Iterate over the subfolders in the input folder
    files_missing = []
    for folder_name in os.listdir(input_folder):
        folder_path = os.path.join(input_folder, folder_name)
        # Check if the item in the folder_path is a directory
        if os.path.isdir(folder_path):
            file_path = os.path.join(folder_path, phonon_files)
            output_file_name = folder_name + '.phonon'
            output_file_path = os.path.join(working_path, output_file_name)

            if not os.path.isfile(file_path):
                error_file = os.path.join(folder_name, phonon_files)
                files_missing.append(error_file)
                continue

            # Copy the file to the output folder with the new name
            shutil.copy(file_path, output_file_path)
    if len(files_missing) > 0:
        #errorlog(error_file, files_missing)
        error_files_missing(files_missing)

    #############################################################
    #  Execute the OCLIMAX commands for all *.phonon files
    #############################################################

    print("\n Executing OCLIMAX for all *.phonon files...\n\n")

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
    print(" ------------------------------------------------------------")
    print(" Job finished in", round(time.time() - time_start_main, 1), "seconds")
    print(" ------------------------------------------------------------")
    print("")



#########################
#   Start OclimaxPlus
#########################



print("\n")
print(" --------------------------------------------------------------------------")
print(" Welcome to OclimaxPlus version " + version())
print(" This is free software, and you are welcome to")
print(" redistribute it under GNU General Public License.")
print(" You should have already configured the '" + jobs_file + "'")
print(" batch file, else check the documentation.")
print(" --------------------------------------------------------------------------")
print(" If you find this code useful, a citation would be awesome :D")
print(" Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/OclimaxPlus")
print(" --------------------------------------------------------------------------")
print("")



if (not os.path.isfile('oclimax.bat')) or (not os.path.isfile('oclimax_convert.exe')) or (not os.path.isfile('oclimax_run.exe')) or (not os.path.isfile('oclimax_plot.exe')):
    if os.path.isfile('oclimax.win') and os.path.isfile('oclimax_convert.exe') and os.path.isfile('oclimax_run.exe') and os.path.isfile('oclimax_plot.exe'):
        error_oclimax_rename()
    else:
        error_oclimax_missing()
    exit()



time_start = time.time()


jobs(jobs_file)


print("")
print(" ------------------------------------------------------------")
print(" All jobs finished in", round(time.time() - time_start, 1), "seconds")
print(" ------------------------------------------------------------")
print("\n")

