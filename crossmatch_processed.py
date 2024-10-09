#!/usr/bin/env python3

import pandas as pd
import argparse
import os

# Function to filter output to keep only rows with '_01_01.png' in the image file path
def filter_output(input_file, output_file):
    try:
        # Load the data from the input file
        df = pd.read_csv(input_file, delim_whitespace=True, header=None)

        # Identify the column containing the image file paths (9th column is index 8)
        image_file_column = 8  # Updated to 8 for the 9th column (0-indexed)

        # Convert the image file column to string (to avoid non-string errors)
        df[image_file_column] = df[image_file_column].astype(str)

        # Filter to keep rows where the image file ends with '_01_01.png'
        filtered_df = df[df[image_file_column].str.endswith('_01_01.png', na=False)]

        # Save the filtered result to the output file
        filtered_df.to_csv(output_file, sep='\t', index=False, header=False)
        print(f"Filtered output saved to: {output_file}")
    except Exception as e:
        print(f"Error processing file: {e}")

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Filter crossmatcher output by keeping rows with '_01_01.png' in the image file name.")

    parser.add_argument('input_file', type=str, help="Path to the input crossmatcher output file.")
    parser.add_argument('output_file', type=str, help="Path to save the filtered output file.")

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: The file '{args.input_file}' does not exist.")
        return

    # Run the filtering function
    filter_output(args.input_file, args.output_file)

if __name__ == "__main__":
    main()

