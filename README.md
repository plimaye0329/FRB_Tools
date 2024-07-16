# FRB_Tools
FRB_Tools is a collection of processing and data analysis scripts for working with FRB Observations from the Effelsberg 100-m Radio Telescope:

## FRB Observations from the Ultra BroadBand Receiver :
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
![github_plot](https://github.com/user-attachments/assets/0996f585-ced0-48ed-bf48-36ab872aee68)


