import os
import argparse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def main(file_band1, file_band2, file_band3, file_band4, file_band5, mjd_file, dm, bins, output_prefix, combined_output_filename_prefix, pdf_output_filename, n_samples=200):
    # Read the burst MJD values from the file
    with open(mjd_file, 'r') as f:
        burst_mjd_values = [float(line.strip()) for line in f.readlines()]

    png_files = []

    for idx, burst_mjd in enumerate(burst_mjd_values):
        # Create a unique output prefix for each MJD
        unique_output_prefix = f"{output_prefix}_mjd_{idx+1}"
        final_output_png = f"{unique_output_prefix}.png"

        # Run the UBBBurster script with the current burst MJD
        os.system(f"python3 FRB-UBER.py {file_band1} {file_band2} {file_band3} {file_band4} {file_band5} {burst_mjd} {dm} {bins} {unique_output_prefix} {combined_output_filename_prefix} {final_output_png} --n_samples {n_samples}")

        # Collect the generated PNG files
        png_files.append(final_output_png)

    # Create a PDF with a 3x3 layout
    with PdfPages(pdf_output_filename) as pdf:
        for i in range(0, len(png_files), 9):  # 9 images per page
            fig, axes = plt.subplots(3, 3, figsize=(13, 13))
            for j, ax in enumerate(axes.flat):
                if i + j < len(png_files):
                    img = plt.imread(png_files[i + j])
                    ax.imshow(img)
                    ax.axis('off')
                else:
                    ax.axis('off')
            plt.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

    print(f"Saved output PDF to {pdf_output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run UBBBurster script with multiple MJD values and compile results into a PDF.")
    parser.add_argument("file_band1", type=str, help="Path to the file for band 1")
    parser.add_argument("file_band2", type=str, help="Path to the file for band 2")
    parser.add_argument("file_band3", type=str, help="Path to the file for band 3")
    parser.add_argument("file_band4", type=str, help="Path to the file for band 4")
    parser.add_argument("file_band5", type=str, help="Path to the file for band 5")
    parser.add_argument("mjd_file", type=str, help="Path to the text file containing burst MJD values")
    parser.add_argument("dm", type=float, help="Dispersion Measure (DM)")
    parser.add_argument("bins", type=int, help="Number of bins")
    parser.add_argument("output_prefix", type=str, help="Output prefix for intermediate files")
    parser.add_argument("combined_output_filename_prefix", type=str, help="Prefix for combined output files")
    parser.add_argument("pdf_output_filename", type=str, help="Filename for the output PDF")
    parser.add_argument("--n_samples", type=int, default=200, help="Number of samples around the pulse for slicing spectrum")

    args = parser.parse_args()

    main(args.file_band1, args.file_band2, args.file_band3, args.file_band4, args.file_band5, args.mjd_file, args.dm, args.bins, args.output_prefix, args.combined_output_filename_prefix, args.pdf_output_filename, args.n_samples)

