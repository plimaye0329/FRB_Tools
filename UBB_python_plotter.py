import sys
import psrchive
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import block_reduce
import argparse

def load_psrchive(fname, nchan, dm):
    """Load data from a PSRCHIVE file.
    
    Parameters
    ----------
    fname : str
        Archive (.ar) to load.
    nchan : int
        Number of frequency channels to scrunch to.
    dm : float
        Dispersion measure to set.

    Returns
    -------
    waterfall : array_like
        Burst dynamic spectrum.
    f_channels : array_like
        Center frequencies, in MHz.
    t_res : float
        Sampling time, in s.
    """
    archive = psrchive.Archive_load(fname)
    archive.fscrunch_to_nchan(nchan)
    archive.pscrunch()
    archive.remove_baseline()
    archive.set_dispersion_measure(dm)
    archive.dedisperse()
    weights = archive.get_weights().squeeze()
    waterfall = np.ma.masked_array(archive.get_data().squeeze())
    waterfall[weights == 0] = np.ma.masked
    f_channels = np.array([
        archive.get_first_Integration().get_centre_frequency(i) \
        for i in range(archive.get_nchan())])
    t_res = archive.get_first_Integration().get_duration() \
        / archive.get_nbin()

    if archive.get_bandwidth() < 0:
        waterfall = np.flipud(waterfall)
        f_channels = f_channels[::-1]

    return waterfall, f_channels, t_res

def main():
    parser = argparse.ArgumentParser(description='Generate a burst plot from a PSRCHIVE file.')
    parser.add_argument('-f', '--filename', type=str, required=True, help='Path to the PSRCHIVE file')
    parser.add_argument('-n', '--nchan', type=int, required=True, help='Number of frequency channels to scrunch to')
    parser.add_argument('-d', '--dm', type=float, required=True, help='Dispersion measure to set')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output PNG filename')
    
    args = parser.parse_args()

    waterfall, f_channels, t_res = load_psrchive(args.filename, args.nchan, args.dm)

    block_size = (1, 1)
    waterfall_reduced = block_reduce(waterfall, block_size=block_size, func=np.mean)
    mean_per_row = np.mean(waterfall_reduced, axis=1, keepdims=True)
    std_per_row = np.std(waterfall_reduced, axis=1, keepdims=True)
    std_per_row[std_per_row == 0] = 1  # Avoid division by zero

    waterfall_reduced = (waterfall_reduced - mean_per_row) / std_per_row

    t_res_reduced = t_res * block_size[1]
    f_channels_reduced = f_channels[::block_size[0]]

    time_series = np.mean(waterfall_reduced[0:], axis=0)
    time_series = (time_series - np.median(time_series)) / np.std(time_series)

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(9, 7), gridspec_kw={'height_ratios': [1, 3]})

    time = np.arange(waterfall_reduced.shape[1]) * t_res_reduced
    ax1.plot(time, time_series, color='black')
    ax1.set_ylabel('S/N')
    ax1.grid(True)

    im = ax2.imshow(waterfall_reduced, aspect='auto', cmap='plasma', origin='lower',
                    extent=[0, waterfall_reduced.shape[1] * t_res_reduced, f_channels_reduced.min(), f_channels_reduced.max()],
                    vmin=np.percentile(waterfall_reduced, 5), vmax=np.percentile(waterfall_reduced, 95))
    ax2.set_xlabel('Time (ms)')
    ax2.set_ylabel('Frequency (MHz)')
    yticks = np.linspace(f_channels_reduced.min(), f_channels_reduced.max(), num=15)
    ax2.set_yticks(yticks)
    ax2.set_yticklabels([f'{tick:.1f}' for tick in yticks])
    plt.title(f'DM = {args.dm} $pc cm^{{-3}}$')

    plt.subplots_adjust(hspace=0.1)
    plt.tight_layout()

    plt.savefig(args.output)
    plt.show()

if __name__ == "__main__":
    main()

