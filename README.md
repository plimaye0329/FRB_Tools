# FRB_Tools
FRB_Tools is a collection of processing and data analysis scripts for working with FRB Observations from the Effelsberg 100-m Radio Telescope.









## TransientX Utilities:

## Search Optimization:
**transx_UBB1.sh** \

This is a bash script implementation which runs the transientx_fil command on psrfits format telescope data. The script is designed to handle data from the Ultra BroadBand Receiver
on Effelsberg but can be easily generalized by editing the bash script. TransientX has a flag named ```-zdot``` which is a zero-DM filter to get rid of strong broad rfi signals. However,
this flag cannot be used above ~4GHz. Therefore, this script only performs search on the first three UBB bands where the ```-zdot``` flag is set ```True```. 

The script can be used in the command line as:
```python
$ ./transx_UBB1.sh
```
After running the command, it will ask if you want to input a DDplan or not based on your search specifications. For targeted searches with known source DM, no DDplan file is needed and
the optimized DM steps for each band can be manually input into a configuration txt file. This file includes multiple columns with path to psrfits data, location to dump candidates, time downsampling (--td),
frequency downsampling (--fd), DM start (--dms), DM step (--ddm), No of DMs (--ndm), snr threshold (--thre), min width (--minw), max_width (--maxw) and rfi masks (-zap) respectively. 

The script reads the config file and takes chunks of three rows corresponding to the data from the three bands and processes them simultaneously using the Unix command ``` xargs ``` and further moves on 
with steps of 3 chunks until all observations are processed.

An example file can be seen in the files section ``` 'transx_UBB1.txt' ```


**replot_UBB1.sh** \
This is a basch script that runs replot_fil command on the psrfits data only in the time windows of transientx_fil detections by reading the cands file. The script is designed to handle data from
the Ultra BroadBand Receiver on Effelsberg but can be easily generalized by editing the bash script. Similar to ``` transx_UBB1.sh ```, this script also runs the zdot filter and hence can be used only
on the first three bands of UBB.

The script can be used in the command line as :
```python
$ ./replot_UBB1.sh
```

It will ask to provide a configuration file, which is a txt file with multiple columns as: : path to psrfits data, path to parse cands file, time downsampling (--td), widthcutoff and dmcutoff respectively. \
``` --widthcutoff``` : This option will remove all candidates which have widths larger than the set value. Generally, this value should be set as the maximum search width\
``` --dmcutoff ``` : This option will remove all candidates identified below a certain dispersion measure. This value should be set carefully depending on the source DM.\

The script reads the config file and takes chunks of three rows corresponding to the data from the three bands and processes them simultaneously using the Unix command ``` xargs ``` and further moves on 
with steps of 3 chunks until all observations are processed.

An example configuration file can be seen in the files section ``` replot_UBB1.txt ```


**Note** : Similar scripts have been made to process the high frequency UBB Data (4-6GHz) covering the band4 and band5 respectively.
The scripts are : ``` transx_UBB2.sh``` & ``` replot_UBB2.sh ``` with the example config files : ``` transx_UBB2.txt``` & ``` replot_UBB2.txt```



## crossmatch.py:
This script reads the output .cands file from replot_fil (TransientX). From visual inspection of replot png images, create a list of png filenames of true bursts. 
The script will crossmatch this list with the filenames in the png filename column of the cands file and write out a new cands file with the rows specific to only
the true bursts. This is especially important when there are too many false candidates in replot_fil. You can later extract the burst MJDs from the new cands file
for plotting the bursts.

Usage:
```
sage: crossmatch.py [-h] -i INPUT -o OUTPUT png_filenames [png_filenames ...]

Crossmatch PNG filenames with input file.

positional arguments:
  png_filenames         List of PNG filenames to crossmatch. Provide one or more filenames separated by spaces.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input filename containing the data to be processed.
  -o OUTPUT, --output OUTPUT
                        Output filename where the matched rows will be written.

Author: Pranav Limaye Date: May 24, 2024 Example usage: python crossmatch.py -i input.cands -o output.txt J0000-00_60439.2012380060_cfbf00000_01_01_replot.png
J0000-00_60439.2020366037_cfbf00000_01_01_replot.png

```

## FRB Observations with the Ultra BroadBand Receiver :
The Ultra BroadBand receiver (UBB) installed on the Effelsberg 100-m Radio Telescope operates in the frequency range of 1.3 - 6 GHz.
The data is recorded by the Effelsberg Direct Digitization (EDD) System in standard PSRFITS Format. 

Singularity to shell before using the scripts : ``` pulsar@paf0: /fpra/bursts/01/sbethapudi/psrppd.sif ```
This singularity can be accessed from either pulsar@paf0 or dogmatix0 servers.

The following scripts have been tailored to process and plot detections from one of the bands of the UBB or alternatively will also work
on data from a single bandwidth receiver:

## UBB_Plotter.py:
Usage:
```
$ python UBB_plotter.py -h

usage: UBB_plotter.py [-h] -f FILENAME -m MJD -D DM -b BINS -O OUTPUT

Run dspsr command with specified parameters.

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Input FITS filename
  -m MJD, --mjd MJD     Burst MJD
  -D DM, --dm DM        Dispersion Measure (DM)
  -b BINS, --bins BINS  Number of phase bins
  -O OUTPUT, --output OUTPUT
                        Output filename
```
The plotter will make a dspsr archive file one second long around the burst MJD. The frequency resolution is the default resolution of the receiver
while the time resolution is dependent on the ```-b``` flag. For eg: ```-b 1024``` for storing 1second window gives a time resolution of 1 millisecond.
The maximum acheiveble time resolution will depend on the native time resolution to which the voltage data was averaged to which can be extracted by
reading the header of the psrfits file.

The script will output a ```.ar``` file. This file can be opened using the psrchive command pazi : ``` $ pazi <filename> ```
If required clean the rfi in this spectrum using the psrchive zap option and save the file with the extension ```.ar.pazi```

## UBB_Python_Plotter.py:
Usage:
```
 $ python UBB_python_plotter.py -h

usage: UBB_python_plotter.py [-h] -f FILENAME -n NCHAN -d DM -o OUTPUT

Generate a burst plot from a PSRCHIVE file.

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Path to the PSRCHIVE file
  -n NCHAN, --nchan NCHAN
                        Number of frequency channels to scrunch to
  -d DM, --dm DM        Dispersion measure to set
  -o OUTPUT, --output OUTPUT
                        Output PNG filename

```
The ```NCHAN``` corresponds to the number of frequency channels in the archive file. This can be checked using:
```
$ vap -c nchan <filename>
```
In order to successfully apply the rfi mask created by pazi, downsample the spectrum in frequency by a factor of 2. For eg: If the original nchan is 512,
put ``` -n 256 ``` in the plotter command. 

The output file will be saved in a png format for visualization. Alternatively, you can 
also edit the script to save a 2-D dynamic spectrum instead.

## Example Output Plot:
A single pulse from PSR B0329+54 observed with the P217 7beam L-band receiver on the Effelsberg 100-m Radio Telescope:

![github_plot](https://github.com/user-attachments/assets/0996f585-ced0-48ed-bf48-36ab872aee68)





