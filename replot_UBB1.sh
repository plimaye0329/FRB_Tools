#!/bin/bash

#Function to run replot_fil on the candidate files from transientX:

run_replot(){
	fits_file=$1
	cand_file=$2
	td=$3
	width_cutoff=$4
	dmcutoff=$5

	echo "running replot_fil for file: $fits_file"

	replot_fil --td $3 --zdot --candfile $2 --scloffs --kadane 8 4 7 --widthcutoff $4 --dmcutoff $5 --clean --coherent --zero_off --wts -f $1 -v --psrfits
}

export -f run_replot

echo "Enter path to the configuration file "
read config_file

# Split the configuration file into chunks of 5 lines each
split -l 3 "$config_file" chunk_

# Process each chunk sequentially
for chunk in chunk_*
do
        # Run transientx_fil without ddplan option
        cat "$chunk" | xargs -n 5 -P 5 bash -c 'run_replot "$@"' _
    # Clean up the chunk file after processing
    rm "$chunk"
done

