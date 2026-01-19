import os
import subprocess
import warnings
import numpy as np
import fitsio as fio
import matplotlib.pyplot as plt
from skimage.measure import block_reduce
import argparse
import psrchive


# ==========================================================
# CLASS FOR MULTI-BAND BURSTER PROCESSING
# ==========================================================

class UBBBurster:
    def __init__(self, band_files, burst_mjd, dm):
        self.band_files = band_files  # list of 7 files
        self.burst_mjd = burst_mjd
        self.dm = dm

        # Center frequencies for 7 bands
        self.center_freqs = [
            1101.5625,
            1851.5625,
            2601.5625,
            3351.5625,
            4101.5625,
            4851.5625,
            5601.5625
        ]

        # Read FITS headers and extract tmjd for each band
        self.tmjds = []
        for f in band_files:
            hdr = fio.read_header(f, ext=0)
            self.tmjds.append(self._calculate_tmjd(hdr))

        # Calculate TOAs for all 7 bands
        self.toas = []
        for tmjd, freq in zip(self.tmjds, self.center_freqs):
            self.toas.append(self._calculate_toa(tmjd, burst_mjd, freq, dm))

        # Convert TOA → cepoch
        self.cepochs = [tmjd + toa/86400 for tmjd, toa in zip(self.tmjds, self.toas)]

        print("===== TOA VALUES FOR 7 BANDS =====")
        for i, toa in enumerate(self.toas):
            print(f"Band {i+1}: TOA = {toa:.6f} sec")


    # -------------------------------------------------------
    def _calculate_tmjd(self, hdr):
        imjd = hdr["STT_IMJD"]
        smjd = hdr["STT_SMJD"]
        soffs = hdr["STT_OFFS"]
        return imjd + (smjd + soffs) / 86400.0


    # -------------------------------------------------------
    def _calculate_toa(self, tmjd, burst_mjd, freq, dm):
        delay_seconds = (
            4.1487416e6 * ((1.0/freq**2) - (1.0/5601.5625**2))
        ) / 1000.0 * dm
        return ((burst_mjd + delay_seconds/86400) - tmjd)*86400 - 0.5


    # -------------------------------------------------------
    def dspsr_process_all(self, dm, bins, output_prefix):
        commands = []

        for i, (toa, cepoch, f) in enumerate(zip(self.toas, self.cepochs, self.band_files)):
            commands.append([
                "dspsr",
                "-S", str(toa),
                "-T", "1.0",
                "-c", "1.0",
                "--scloffs",
                "-D", str(dm),
                "-cepoch", str(cepoch),
                "-b", str(bins),
                "-O", f"{output_prefix}_{i+1}",
                f
            ])

        results = []
        for cmd in commands:
            result = subprocess.run(cmd, capture_output=True, text=True)
            results.append(result)
            if result.returncode != 0:
                warnings.warn(f"Command failed: {' '.join(cmd)}\nError: {result.stderr}")

        return results


# ==========================================================
# PSRCHIVE LOADING UTILITIES
# ==========================================================

def load_psrchive(fname, nchans):
    archive = psrchive.Archive_load(fname)
    archive.fscrunch_to_nchan(nchans)
    archive.pscrunch()
    archive.remove_baseline()
    archive.dedisperse()

    weights = archive.get_weights().squeeze()
    data = np.ma.masked_array(archive.get_data().squeeze())
    data[weights == 0] = np.ma.masked

    f_channels = np.array([
        archive.get_first_Integration().get_centre_frequency(i)
        for i in range(archive.get_nchan())
    ])

    t_res = archive.get_first_Integration().get_duration() / archive.get_nbin()

    # Flip if needed
    if archive.get_bandwidth() < 0:
        data = np.flipud(data)
        f_channels = f_channels[::-1]

    return data, f_channels, t_res


# ==========================================================
# WATERFALL PROCESSING FUNCTIONS
# ==========================================================

def extract_sliced_spectrum(waterfall, n_samples=200):
    time_series = np.nanmean(waterfall, axis=0)
    peak_index = np.argmax(time_series)
    start = max(0, peak_index - n_samples)
    end = min(waterfall.shape[1], peak_index + n_samples)
    return waterfall[:, start:end]


def process_waterfall(wf, t_res, block_size=(1,1)):
    reduced = block_reduce(wf, block_size=block_size, func=np.mean)
    mean = np.nanmean(reduced, axis=1, keepdims=True)
    std = np.nanstd(reduced, axis=1, keepdims=True)
    std[std == 0] = 1
    reduced = (reduced - mean)/std
    return reduced, t_res * block_size[1]


def combine_waterfalls(waterfalls, f_lists):
    wf = np.concatenate(waterfalls, axis=0)
    freqs = np.concatenate(f_lists)
    return wf, freqs


# ==========================================================
# PLOTTING OBSERVATION OUTPUT
# ==========================================================

def main(
    file_band1, file_band2, file_band3, file_band4,
    file_band5, file_band6, file_band7,
    burst_mjd, dm, bins, output_prefix, n_samples, final_png
):

    band_files = [
        file_band1, file_band2, file_band3, file_band4,
        file_band5, file_band6, file_band7
    ]

    burster = UBBBurster(band_files, burst_mjd, dm)
    burster.dspsr_process_all(dm, bins, output_prefix)

    # Load all 7 waterfalls
    nchans_list = [640,640,640,640,640,640,640]
    waterfalls = []
    f_channels_list = []
    t_res_list = []

    for i in range(7):
        wf, freqs, t_res = load_psrchive(f"{output_prefix}_{i+1}.ar", nchans_list[i])
        waterfalls.append(wf)
        f_channels_list.append(freqs)
        t_res_list.append(t_res)

    # Reduce all waterfalls
    waterfalls_reduced = []
    for wf, t_res in zip(waterfalls, t_res_list):
        reduced, _ = process_waterfall(wf, t_res)
        waterfalls_reduced.append(reduced)

    # Combine all 7 (NO GAPS ANYMORE)
    full_waterfall, full_freqs = combine_waterfalls(waterfalls_reduced, f_channels_list)

    # Collapse to time_series
    time_series = np.nanmean(full_waterfall, axis=0)
    start = max(0, np.argmax(time_series) - n_samples)
    end = min(full_waterfall.shape[1], np.argmax(time_series) + n_samples)

    centered_wf = full_waterfall[:, start:end]
    t_res = t_res_list[0]
    time_axis = np.arange(centered_wf.shape[1]) * t_res
    time_axis -= time_axis[len(time_axis)//2]

    # PLOT
    fig, (ax1, ax2) = plt.subplots(
        2,1,sharex=True,figsize=(9,7),
        gridspec_kw={"height_ratios":[1,3]}
    )

    ax1.plot(time_axis, time_series[start:end], color="black")
    ax1.set_ylabel("Intensity")
    ax1.grid(True)

    im = ax2.imshow(
        centered_wf,
        aspect='auto', cmap='plasma', origin='lower',
        extent=[time_axis.min(), time_axis.max(),
                full_freqs.min(), full_freqs.max()],
        vmin=np.nanpercentile(centered_wf,5),
        vmax=np.nanpercentile(centered_wf,95)
    )

    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Frequency (MHz)")

    plt.tight_layout()
    plt.savefig(final_png, dpi=150)
    plt.close()

    # Cleanup .ar files
    for i in range(7):
        fname = f"{output_prefix}_{i+1}.ar"
        if os.path.exists(fname):
            os.remove(fname)
            print(f"Removed {fname}")

    print("Processing Complete!")


# ==========================================================
# COMMAND LINE INTERFACE
# ==========================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process UBBBurster 7-band data.")

    parser.add_argument("file_band1")
    parser.add_argument("file_band2")
    parser.add_argument("file_band3")
    parser.add_argument("file_band4")
    parser.add_argument("file_band5")
    parser.add_argument("file_band6")
    parser.add_argument("file_band7")

    parser.add_argument("burst_mjd", type=float)
    parser.add_argument("dm", type=float)
    parser.add_argument("bins", type=int)
    parser.add_argument("output_prefix", type=str)
    parser.add_argument("n_samples", type=int)
    parser.add_argument("final_output_png", type=str)

    args = parser.parse_args()

    main(
        args.file_band1, args.file_band2, args.file_band3, args.file_band4,
        args.file_band5, args.file_band6, args.file_band7,
        args.burst_mjd, args.dm, args.bins, args.output_prefix,
        args.n_samples, args.final_output_png
    )
