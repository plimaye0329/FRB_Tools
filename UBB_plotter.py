import os
import subprocess
import warnings

import numpy as np
import fitsio as fio
import matplotlib.pyplot as plt
import matplotlib.gridspec as mgs
from skimage.measure import block_reduce
import argparse

class UBBPlotter:
    def __init__(self, filename, burst_mjd):
        self.fname = filename
        self.burst_mjd = burst_mjd
        self.primary = fio.read_header(self.fname, ext=0)
        imjd = self.primary['STT_IMJD']
        smjd = self.primary['STT_SMJD']
        soffs = self.primary['STT_OFFS']
        self.tmjd = imjd + (smjd / 86_400.) + (soffs / 86_400.)
        self.toa = (self.burst_mjd - self.tmjd) * 86400 
        print(self.toa)

    def run_dspsr_command(self, dm, bins, output_filename):
        # Construct the dspsr command
        command1 = [
            'dspsr',
            '-S', str(self.toa),
            '-T', '0.6',
            '-c', '0.6',
            '--scloffs',
            '-D', str(dm),
            '-O', output_filename,
            self.fname
        ]

        # Run the dspsr command
        result1 = subprocess.run(command1, capture_output=True, text=True)

        # Check if the command was successful
        if result1.returncode == 0:
            print("dspsr command executed successfully:")
            print(result1.stdout)
        else:
            print("dspsr command failed with error:")
            print(result1.stderr)
            return  # Exit the function if the dspsr command fails


            output_ar_file
        


def main():
    parser = argparse.ArgumentParser(description="Run dspsr command with specified parameters.")
    parser.add_argument('-f', '--filename', type=str, required=True, help='Input FITS filename')
    parser.add_argument('-m', '--mjd', type=float, required=True, help='Burst MJD')
    parser.add_argument('-D', '--dm', type=float, required=True, help='Dispersion Measure (DM)')
    parser.add_argument('-b', '--bins', type=int, required=True, help='Number of phase bins')
    parser.add_argument('-O', '--output', type=str, required=True, help='Output filename')

    args = parser.parse_args()

    plotter = UBBPlotter(args.filename, args.mjd)
    plotter.run_dspsr_command(args.dm, args.bins, args.output)

if __name__ == "__main__":
    main()
