# OclimaxPlus
OclimaxPlus is a Python program to automatize batch calculations of neutron scattering _S(Q,E)_ simulations of *.phonon files via the _OCLIMAX_ software, performing the following consecutive console commands for each phonon file:  
`oclimax_convert.exe -c filename.phonon -o filename`  
`oclimax_run.exe filename.oclimax filename.params`  


## Requirements

OclimaxPlus runs in [Python 3.X](https://www.python.org/downloads/) with **Pandas** installed, and has to be executed with the [OCLIMAX software](https://sites.google.com/site/ornliceman/download) installed in the same folder; in particular, the following files are required:  
**oclimax_convert.exe**, **oclimax_run.exe**, **oclimax.bat** (renamed from oclimax.win), **oclimax_plot.exe**.  


## Installing

First download the source code, as you prefer:  
* From your **web browser**  
On GitHub, clic on 'Code', 'Download ZIP', and extract.  
* Using **git**  
`git clone https://github.com/pablogila/OclimaxPlus.git`  

Once downloaded, open the **OclimaxPlus** folder and copy inside the required OCLIMAX scripts, mentioned in the previous section. Then create a new folder called **data**, where the input folder(s) should be placed; inside each of your input folder(s), there should be several nested subfolders containing your phonon files. After execution, the program will extract the outputs in an **out** folder, following the naming of the subfolders. The folder structure should look as follows:  

```.
CrystalReader
│
├── OclimaxPlus.py
├── ... OCLIMAX scripts ...
│
├── data
│   ├── data_directory_1
│   │    ├── 000-000-000-000
│   │    │   └── data_file.phonon
│   │    ├── 270-000-000-000
│   │    │   └── ...
│   │    ├── pnam-270-180-000-000_test
│   │    ├── random_subfolder-180-270-000-090
│   │    └── ...
│   ├── data_directory_2
│   └── ...
│   
└── out
    ├── OUT_oclimax_data_directory_1
    │   ├── 000-000-000-000.csv
    │   ├── 270-000-000-000.csv
    │   └── ...
    ├── TEMP_oclimax_data_directory_1
    │   └── ... Temporary files ...
    ├── OUT_oclimax_data_directory_2
    └── ...
 ```


## Execution

Run in **Windows Powershell**:  
`python OclimaxPlus.py`  

The first time running the program it will create an empty batch job file, called **OclimaxPlus_JOBS.txt**. The jobs to perform should be introduced in this file; then, run the program again. The structure of the jobs shoud be:  
`data_directory, phonon_files`  

An example of a batch job for a folder called **pbe-d3**, with a **cc-2_PhonDOS.phonon** file inside each of the subfolders, would be:  
`pbe-d3, cc-2_PhonDOS.phonon`  

Notice that before execution, if any *.csv, *.phonon, *.params or *.oclimax file is found in the working directory, it will be moved to a 'UNFINISHED_FILES' folder.  


## Suggestions and Citation

Please feel free to contact me if you have any questions or suggestions.  
If you find these scripts useful, a citation would be awesome :D  
*Pablo Gila-Herranz, “OclimaxPlus”, 2023. https://github.com/pablogila/OclimaxPlus*  


## References

* [Simulation of INS Spectra Using OCLIMAX](https://doi.org/10.1021/acs.jctc.8b01250)
* [OCLIMAX download webpage and user manual](https://sites.google.com/site/ornliceman/download)
* [CrystalReader on GitHub](https://github.com/pablogila/CrystalReader)