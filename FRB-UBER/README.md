![ls1](https://github.com/user-attachments/assets/dd3c119f-bc6b-4295-bd3a-b5cd98afd416)## FRB-UBER : (**U**ltra **B**roadBand **E**ffelsberg **R**eceiver plotter)
The Ultra BroadBand receiver (UBB) installed on the Effelsberg 100-m Radio Telescope operates in the frequency range of 1.3 - 6 GHz.
The data is recorded by the Effelsberg Direct Digitization (EDD) System in standard PSRFITS Format. 

Singularity to shell before using the scripts : ``` pulsar@paf0: /fpra/bursts/01/sbethapudi/psrppd.sif ```
This singularity can be accessed from either pulsar@paf0 or dogmatix0 servers

This is a python script to make FRB or pulsar/magnetar single pulse dynamic spectrum plots across 1.3 - 6GHz Ultra BroadBand (UBB) receiver installed on the 
Effelsberg 100-m Radio Telescope. 
```
usage: FRB-UBER.py [-h] [--n_samples N_SAMPLES] file_band1 file_band2 file_band3 file_band4 file_band5 burst_mjd dm bins output_prefix combined_output_filename_prefix final_output_png

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
  final_output_png      Filename for the final output PNG

optional arguments:
  -h, --help            show this help message and exit
  --n_samples N_SAMPLES
                        Number of samples around the pulse for slicing spectrum
```

# Batch Processing:
The above script can be runned over a loop to process multiple single pulse plots using ```run-UBER.py``` script.
The usage of this script is as follows:
(Note: The FRB-UBER.py script has to be on the same path to run this script)

```
usage: UBB_Batch.py [-h] [--n_samples N_SAMPLES] file_band1 file_band2 file_band3 file_band4 file_band5 mjd_file dm bins output_prefix combined_output_filename_prefix pdf_output_filename

Run UBER.py script with multiple MJD values and compile results into a PDF.

positional arguments:
  file_band1            Path to the file for band 1
  file_band2            Path to the file for band 2
  file_band3            Path to the file for band 3
  file_band4            Path to the file for band 4
  file_band5            Path to the file for band 5
  mjd_file              Path to the text file containing burst MJD values
  dm                    Dispersion Measure (DM)
  bins                  Number of bins
  output_prefix         Output prefix for intermediate files
  combined_output_filename_prefix
                        Prefix for combined output files
  pdf_output_filename   Filename for the output PDF

optional arguments:
  -h, --help            show this help message and exit
  --n_samples N_SAMPLES
                        Number of samples around the pulse for slicing spectrum

```
This script takes a mjd.txt file as input which should have a 1-D array of burst mjds for which you want to make waterfaller plots.
The script will create a pdf file with a 3 X 3 plot layout as well as save the individual plots in seperate .png files.

Note: The parameter ```--n_samples``` decides how many time samples to consider around the burst center. For a single component burst,
this can be set to 100 but for a multi-component burst, set this to 200


# Example:
Making a single burst plot: 
```
python3 FRB-UBER.py /beegfsEDD/EDD_pipeline_data/production/pipeline_data/search1/34-24/FRB20240114A_20240509-04:05:15.fits /beegfsEDD/EDD_pipeline_data/production/pipeline_data/search2/34-24/FRB20240114A_20240509-04:05:15.fits /beegfsEDD/EDD_pipeline_data/production/pipeline_data/search3/34-24/FRB20240114A_20240509-04:05:15.fits /beegfsEDD/EDD_pipeline_data/production/pipeline_data/search4/34-24/FRB20240114A_20240509-04:05:15.fits /beegfsEDD/EDD_pipeline_data/production/pipeline_data/search5/34-24/FRB20240114A_20240509-04:05:15.fits 60439.172625  529.56 8192 r147 r147 r147 --n_samples 150
```

Making burst collage using MJD List:
```
python3 UBB_Batch.py --n_samples 50 /beegfsEDD/EDD_pipeline_data/production/pipeline_data/search1/34-24/FRB20240114A_20240509-04:05:15.fits /beegfsEDD/EDD_pipeline_data/production/pipeline_data/search2/34-24/FRB20240114A_20240509-04:05:15.fits /beegfsEDD/EDD_pipeline_data/production/pipeline_data/search3/34-24/FRB20240114A_20240509-04:05:15.fits /beegfsEDD/EDD_pipeline_data/production/pipeline_data/search4/34-24/FRB20240114A_20240509-04:05:15.fits /beegfsEDD/EDD_pipeline_data/production/pipeline_data/search5/34-24/FRB20240114A_20240509-04:05:15.fits mjd_list.txt 529.56 1024 r147 r147 r147
```

# Example Plots:
1) Single Pulse of B0355+54:
 

![b0355_mjd_8](https://github.com/user-attachments/assets/caff9dba-7548-40bc-a0cc-5da18301dbd7)
