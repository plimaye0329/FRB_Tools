## FRB-UBER : (**U**ltra **B**roadBand **E**ffelsberg **R**eceiver plotter)
The Ultra BroadBand receiver (UBB) installed on the Effelsberg 100-m Radio Telescope operates in the frequency range of 1.3 - 6 GHz.
The data is recorded by the Effelsberg Direct Digitization (EDD) System in standard PSRFITS Format. 

Singularity to shell before using the scripts : ``` pulsar@paf0: /fpra/bursts/01/sbethapudi/psrppd.sif ```
This singularity can be accessed from either pulsar@paf0 or dogmatix0 servers

This is a python script to make FRB or pulsar/magnetar single pulse dynamic spectrum plots across 1.3 - 6GHz Ultra BroadBand (UBB) receiver installed on the 
Effelsberg 100-m Radio Telescope. 
```
usage: FRB-UBER.py [-h] file_band1 file_band2 file_band3 file_band4 file_band5 burst_mjd dm bins output_prefix combined_output_filename_prefix n_samples final_output_png

Process UBBBurster data.

positional arguments:
  file_band1            Path to the file for band 1
  file_band2            Path to the file for band 2
  file_band3            Path to the file for band 3
  file_band4            Path to the file for band 4
  file_band5            Path to the file for band 5
  burst_mjd             Burst MJD
  dm                    Dispersion Measure (DM)
  bins                  Number of bins
  output_prefix         Output prefix for intermediate files
  combined_output_filename_prefix
                        Prefix for combined output files
  n_samples             Number of samples around the pulse for slicing spectrum (preferred range : 100-400 depending on your pulse structure and width)
  final_output_png      Filename for the final output PNG

optional arguments:
  -h, --help            show this help message and exit
```
The above script can be runned over a loop to process multiple single pulse plots using a ```commands.txt``` file 
The <common_path> flag in this txt file refers to the common branch of all the psrfits data files. The loop is runned using the script
```run_commands.py``` on this txt file:
```
usage: run_commands.py [-h] commands_file common_path

Execute a list of commands from a file with placeholders.

positional arguments:
  commands_file  Path to the file containing commands.
  common_path    Common path to replace in commands.


optional arguments:
  -h, --help     show this help message and exit
```
An example usage of running this loop is as follows:
```
$ python3 run_commands.py commands.txt /beegfsEDD/EDD_pipeline_data/production/pipeline_data

```
An example UBB plot of a magnetar (XTE J1810-197):
![marlon1](https://github.com/user-attachments/assets/fe252849-5412-4e78-b5ee-58ccefa20b36)
