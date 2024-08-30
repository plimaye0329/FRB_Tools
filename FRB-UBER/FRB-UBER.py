import os
import subprocess
import warnings
import numpy as np
import fitsio as fio
import matplotlib.pyplot as plt
from skimage.measure import block_reduce
import argparse
import psrchive

class UBBBurster:
    def __init__(self, file_band1, file_band2, file_band3, file_band4, file_band5, burst_mjd, dm):
        self.f_band1 = file_band1
        self.f_band2 = file_band2
        self.f_band3 = file_band3
        self.f_band4 = file_band4
        self.f_band5 = file_band5
        self.burst_mjd = burst_mjd
        self.dm = dm

        self.primary1 = fio.read_header(self.f_band1, ext=0)
        self.primary2 = fio.read_header(self.f_band2, ext=0)
        self.primary3 = fio.read_header(self.f_band3, ext=0)
        self.primary4 = fio.read_header(self.f_band4, ext=0)
        self.primary5 = fio.read_header(self.f_band5, ext=0)

        self.tmjd1 = self._calculate_tmjd(self.primary1)
        self.tmjd2 = self._calculate_tmjd(self.primary2)
        self.tmjd3 = self._calculate_tmjd(self.primary3)
        self.tmjd4 = self._calculate_tmjd(self.primary4)
        self.tmjd5 = self._calculate_tmjd(self.primary5)
        #print(self.tmjd1)

        self.freq1 = 1614.84375
        self.freq2 = 2264.84375
        self.freq3 = 3539.0625
        self.freq4 = 4664.0625
        self.freq5 = 5601.5625

        self.toa1 = self._calculate_toa(self.tmjd1, self.burst_mjd, self.freq1, self.dm)
        self.toa2 = self._calculate_toa(self.tmjd2, self.burst_mjd, self.freq2, self.dm)
        self.toa3 = self._calculate_toa(self.tmjd3, self.burst_mjd, self.freq3, self.dm)
        self.toa4 = self._calculate_toa(self.tmjd4, self.burst_mjd, self.freq4, self.dm)
        self.toa5 = self._calculate_toa(self.tmjd5, self.burst_mjd, self.freq5, self.dm)

        self.toa1 = round(self.toa1,6)
        self.toa2 = round(self.toa2,6)
        self.toa3 = round(self.toa3,6)
        self.toa4 = round(self.toa4,6)
        self.toa5 = round(self.toa5,6)

        #self.cepoch1 = self.tmjd1 + self.toa1 / 86400
        self.cepoch1 = self.tmjd1 + self.toa1/86400 #+ (self.tmjd1 - self.tmjd5) # + (self.tmjd1 - self.tmjd5) #self.tmjd1 - (self.tmjd1 - self.tmjd5)
        self.cepoch2 = self.tmjd2 + self.toa2/86400 #+ (self.tmjd2 - self.tmjd5)# + (self.tmjd2 - self.tmjd5)#self.tmjd5 - (self.tmjd2 - self.tmjd5)
        self.cepoch3 = self.tmjd3 + self.toa3/86400 #+ (self.tmjd3 - self.tmjd5)# + (self.tmjd3 - self.tmjd5) #self.tmjd5 - (self.tmjd3 - self.tmjd5)
        self.cepoch4 = self.tmjd4 + self.toa4/86400 #+ (self.tmjd4 - self.tmjd5)# + (self.tmjd4 - self.tmjd5)#self.tmjd5 - (self.tmjd4 - self.tmjd5)
        self.cepoch5 = self.tmjd5 + self.toa5/86400#self.tmjd5 


        self.cepoch1 = round(self.cepoch1, 12)
        self.cepoch2 = round(self.cepoch2, 12)
        self.cepoch3 = round(self.cepoch3, 12)
        self.cepoch4 = round(self.cepoch4, 12)
        self.cepoch5 = round(self.cepoch5, 12)


        print('toa band 1 is', self.toa1)
        print('toa band 2 is', self.toa2)
        print('toa band 3 is', self.toa3)
        print('toa band 4 is', self.toa4)
        print('toa band 5 is', self.toa5)

    def _calculate_tmjd(self, primary_header):
        imjd = primary_header['STT_IMJD']
        smjd = primary_header['STT_SMJD']
        soffs = primary_header['STT_OFFS']
        return imjd + (smjd / 86400.0) + (soffs / 86400.0)

    def _calculate_toa(self, tmjd, burst_mjd, freq, dm):
        delay_seconds = (4.1487416 * 10**6 * ((1 / freq**2) - (1 / 5976.328125**2))) / 1000 * dm
        return ((burst_mjd + delay_seconds/86_400) - tmjd)*86_400 - 0.5

    def dspsr_fullband(self, dm, bins, output_prefix):
        commands = [
            ['dspsr', '-S', str(self.toa1), '-T', '1.0', '-c', '1.0', '--scloffs', '-D', str(dm),'-cepoch',str(self.cepoch1),'-b', str(bins), '-O', f"{output_prefix}_1", self.f_band1],
            ['dspsr', '-S', str(self.toa2), '-T', '1.0', '-c', '1.0', '--scloffs', '-D', str(dm),'-cepoch',str(self.cepoch2),'-b', str(bins), '-O', f"{output_prefix}_2", self.f_band2],
            ['dspsr', '-S', str(self.toa3), '-T', '1.0', '-c', '1.0', '--scloffs', '-D', str(dm),'-cepoch',str(self.cepoch3),'-b', str(bins), '-O', f"{output_prefix}_3", self.f_band3],
            ['dspsr', '-S', str(self.toa4), '-T', '1.0', '-c', '1.0', '--scloffs', '-D', str(dm),'-cepoch',str(self.cepoch4),'-b', str(bins), '-O', f"{output_prefix}_4", self.f_band4],
            ['dspsr', '-S', str(self.toa5), '-T', '1.0', '-c', '1.0', '--scloffs', '-D', str(dm),'-cepoch',str(self.cepoch5),'-b', str(bins), '-O', f"{output_prefix}_5", self.f_band5]
        ]
        results = []
        for cmd in commands:
            result = subprocess.run(cmd, capture_output=True, text=True)
            results.append(result)
            if result.returncode != 0:
                warnings.warn(f"Command failed: {' '.join(cmd)}\nError: {result.stderr}")
        return results

def load_psrchive(fname, nchans):
    archive = psrchive.Archive_load(fname)
    archive.fscrunch_to_nchan(nchans)
    archive.pscrunch()
    archive.remove_baseline()
    archive.dedisperse()
    weights = archive.get_weights().squeeze()
    waterfall = np.ma.masked_array(archive.get_data().squeeze())
    waterfall[weights == 0] = np.ma.masked
    f_channels = np.array([archive.get_first_Integration().get_centre_frequency(i) for i in range(archive.get_nchan())])
    t_res = archive.get_first_Integration().get_duration() / archive.get_nbin()

    if archive.get_bandwidth() < 0:
        waterfall = np.flipud(waterfall)
        f_channels = f_channels[::-1]

    return waterfall, f_channels, t_res

def extract_sliced_spectrum(waterfall, n_samples=200):
    time_series = np.nanmean(waterfall, axis=0)
    peak_index = np.argmax(time_series)
    start_index = max(0, peak_index - n_samples)
    end_index = min(waterfall.shape[1], peak_index + n_samples)
    sliced_spectrum = waterfall[:, start_index:end_index]
    return sliced_spectrum

def insert_nan_band(waterfall1, waterfall2, f_channels1, f_channels2, freq_gap_start, freq_gap_end, freq_gap_bins):
    total_time_bins = waterfall1.shape[1]
    new_frequency_bins = len(f_channels1) + len(f_channels2) + freq_gap_bins
    stitched_waterfall = np.full((new_frequency_bins, total_time_bins), np.nan)
    stitched_waterfall[:len(f_channels1), :] = waterfall1
    stitched_waterfall[len(f_channels1) + freq_gap_bins:, :] = waterfall2
    new_f_channels = np.concatenate([f_channels1, np.linspace(freq_gap_start, freq_gap_end, num=freq_gap_bins, endpoint=False), f_channels2])
    return stitched_waterfall, new_f_channels

def combine_waterfalls(waterfalls, f_channels_list):
    combined_waterfall = waterfalls[0]
    combined_f_channels = f_channels_list[0]

    for i in range(1, len(waterfalls)):
        combined_waterfall = np.concatenate((combined_waterfall, waterfalls[i]), axis=0)
        combined_f_channels = np.concatenate((combined_f_channels, f_channels_list[i]))

    return combined_waterfall, combined_f_channels

def process_waterfall(waterfall, t_res, block_size=(1, 1)):
    waterfall_reduced = block_reduce(waterfall, block_size=block_size, func=np.mean)
    mean_per_row = np.mean(waterfall_reduced, axis=1, keepdims=True)
    std_per_row = np.std(waterfall_reduced, axis=1, keepdims=True)
    std_per_row[std_per_row == 0] = 1
    waterfall_reduced = (waterfall_reduced - mean_per_row) / std_per_row
    return waterfall_reduced, t_res * block_size[1]

def plot_waterfall(waterfall, f_channels, t_res, output_file):
    time = np.arange(waterfall.shape[1]) * t_res

    fig, ax2 = plt.subplots(figsize=(9, 7))
    im = ax2.imshow(waterfall, aspect='auto', cmap='plasma', origin='lower',
                    extent=[time.min(), time.max(), f_channels.min(), f_channels.max()],
                    vmin=np.nanpercentile(waterfall, 5), vmax=np.nanpercentile(waterfall, 95))
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Frequency (MHz)')

    custom_yticks = [1300, 2000, 3000, 4000, 5000, 6000]
    ax2.set_yticks(custom_yticks)
    ax2.set_yticklabels([f'{tick:.1f}' for tick in custom_yticks])

    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()


def main(file_band1, file_band2, file_band3, file_band4, file_band5, burst_mjd, dm, bins, output_prefix, combined_output_filename_prefix, final_output_png, n_samples=200):
    burster = UBBBurster(file_band1, file_band2, file_band3, file_band4, file_band5, burst_mjd, dm)
    burster.dspsr_fullband(dm, bins, output_prefix)

    print("Processing archives...")
    # Load and process the archives
    waterfall1, f_channels1, t_res1 = load_psrchive(f"{output_prefix}_1.ar", 1280)
    waterfall2, f_channels2, t_res2 = load_psrchive(f"{output_prefix}_2.ar", 1280)
    waterfall3, f_channels3, t_res3 = load_psrchive(f"{output_prefix}_3.ar", 2400)
    waterfall4, f_channels4, t_res4 = load_psrchive(f"{output_prefix}_4.ar", 2400)
    waterfall5, f_channels5, t_res5 = load_psrchive(f"{output_prefix}_5.ar", 1600)

    print("Creating dynamic spectra...")
    waterfall_reduced1, t_res_reduced1 = process_waterfall(waterfall1, t_res1)
    waterfall_reduced2, t_res_reduced2 = process_waterfall(waterfall2, t_res2)
    waterfall_reduced3, t_res_reduced3 = process_waterfall(waterfall3, t_res3)
    waterfall_reduced4, t_res_reduced4 = process_waterfall(waterfall4, t_res4)
    waterfall_reduced5, t_res_reduced5 = process_waterfall(waterfall5, t_res5)

    combined_waterfall_1_2, combined_f_channels_1_2 = combine_waterfalls([waterfall_reduced1, waterfall_reduced2], [f_channels1, f_channels2])
    combined_waterfall_3_4_5, combined_f_channels_3_4_5 = combine_waterfalls([waterfall_reduced3, waterfall_reduced4, waterfall_reduced5], [f_channels3, f_channels4, f_channels5])

    freq_gap_start = combined_f_channels_1_2.max()
    freq_gap_end = combined_f_channels_3_4_5.min()
    stitched_waterfall, stitched_f_channels = insert_nan_band(combined_waterfall_1_2, combined_waterfall_3_4_5, combined_f_channels_1_2, combined_f_channels_3_4_5, freq_gap_start, freq_gap_end, freq_gap_bins=400)



    print("Setting RFI FLags to median values...")
    median_value = np.nanmedian(stitched_waterfall)
   # Set multiple frequency ranges to NaN: (These are known rfi channels, edit this according to the rfi environment)
    freq_ranges = [(1450,1600),(1800,1900),(2100,2200),(2450,2500),(3200,3690),(4225,4425),(4625,4675)]

    for freq_range_min, freq_range_max in freq_ranges:
        freq_indices = np.where((stitched_f_channels >= freq_range_min) & (stitched_f_channels <= freq_range_max))[0]
        stitched_waterfall[freq_indices,:] = median_value



   # Calculate the time series and normalize
    time_series = np.nanmean(stitched_waterfall[0:], axis=0)
    noise_floor = int(len(time_series) / 8)
    time_series = (time_series - np.nanmean(time_series[0:noise_floor])) / np.nanstd(time_series[0:noise_floor])

    # Identify the peak and center around it
    peak_index = np.argmax(time_series)
    start_index = max(0, peak_index - n_samples)
    end_index = min(stitched_waterfall.shape[1], peak_index + n_samples)

    # Adjust the waterfall and time axis
    centered_waterfall = stitched_waterfall[:, start_index:end_index]
    time_centered = np.arange(centered_waterfall.shape[1]) * t_res_reduced1
    time_centered -= time_centered[len(time_centered) // 2]  # Center the time axis around zero


    print("Creating Burst Plots...")
    # Plot the results
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(9, 7), gridspec_kw={'height_ratios': [1, 3]})
    ax1.plot(time_centered, time_series[start_index:end_index], color='black')
    ax1.set_ylabel('S/N')
    ax1.grid(True)

    im = ax2.imshow(centered_waterfall, aspect='auto', cmap='plasma', origin='lower',
                    extent=[time_centered.min(), time_centered.max(), stitched_f_channels.min(), stitched_f_channels.max()],
                    vmin=np.nanpercentile(centered_waterfall, 5), vmax=np.nanpercentile(centered_waterfall, 95))
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Frequency (MHz)')

    custom_yticks = [1300, 2000, 3000, 4000, 5000, 6000]
    ax2.set_yticks(custom_yticks)
    ax2.set_yticklabels([f'{tick:.1f}' for tick in custom_yticks])

    plt.subplots_adjust(hspace=0.1)
    plt.tight_layout()
    plt.savefig(final_output_png)
    plt.close()


    # Remove the intermediate .ar files
    for i in range(1, 6):
        ar_file = f"{output_prefix}_{i}.ar"
        if os.path.exists(ar_file):
            os.remove(ar_file)
            print(f"Removed {ar_file}")
    print("Processing Complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process UBBBurster data.")
    parser.add_argument("file_band1", type=str, help="Path to the file for band 1")
    parser.add_argument("file_band2", type=str, help="Path to the file for band 2")
    parser.add_argument("file_band3", type=str, help="Path to the file for band 3")
    parser.add_argument("file_band4", type=str, help="Path to the file for band 4")
    parser.add_argument("file_band5", type=str, help="Path to the file for band 5")
    parser.add_argument("burst_mjd", type=float, help="Burst MJD")
    parser.add_argument("dm", type=float, help="Dispersion Measure (DM)")
    parser.add_argument("bins", type=int, help="Number of bins")
    parser.add_argument("output_prefix", type=str, help="Output prefix for intermediate files")
    parser.add_argument("combined_output_filename_prefix", type=str, help="Prefix for combined output files")
    parser.add_argument("final_output_png", type=str, help="Filename for the final output PNG")
    parser.add_argument("--n_samples", type=int, default=200, help="Number of samples around the pulse for slicing spectrum")

    args = parser.parse_args()

    main(args.file_band1, args.file_band2, args.file_band3, args.file_band4, args.file_band5, args.burst_mjd, args.dm, args.bins, args.output_prefix, args.combined_output_filename_prefix, args.final_output_png, args.n_samples)

