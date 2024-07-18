#!/bin/bash


# Function to run transientx_fil with dms, ddm, ndm parameters
run_transientx() {
    fits_file=$1
    output_dir=$2
    td=$3
    fd=$4
    dms=$5
    ddm=$6
    ndm=$7
    thre=$8
    minw=$9
    maxw=${10}
    zap1=${11}
    zap2=${12}
    zap3=${13}
    zap4=${14}

    echo "Running transientx_fil for file: $fits_file"

    # Create the output directory if it doesn't exist
    mkdir -p "$output_dir"

    # Run the transientx_fil command with dms, ddm, ndm
    transientx_fil -v -t 4 --td "$td" --fd "$fd" --dms "$dms" --ddm "$ddm" --ndm "$ndm" --thre "$thre" --minw "$minw" --maxw "$maxw" -r 1 -z "$zap1" "$zap2" zap "$zap3" "$zap4" zdot kadaneF 8 4 --fill mean --scloffs --zero_off --wts --psrfits -f "$fits_file" -o "$output_dir"
}

# Function to run transientx_fil with ddplan option
run_transientx_ddplan() {
    fits_file=$1
    output_dir=$2
    td=$3
    fd=$4
    ddplan=$5
    thre=$6
    minw=$7
    maxw=$8
    zap1=$9
    zap2=${10}
    zap3=${11}
    zap4=${12}

    echo "Running transientx_fil with ddplan for file: $fits_file"

    # Create the output directory if it doesn't exist
    mkdir -p "$output_dir"

    # Run the transientx_fil command with ddplan
    transientx_fil -v -t 4 --td "$td" --fd "$fd" --ddplan "$ddplan" --thre "$thre" --minw "$minw" --maxw "$maxw" -r 1 -z "$zap1" "$zap2" zap "$zap3" "$zap4" zdot --fill mean --scloffs --psrfits -f "$fits_file" -o "$output_dir"
}

# Export the functions so xargs can use them
export -f run_transientx
export -f run_transientx_ddplan

# Prompt the user to choose between running with or without ddplan
echo "Do you want to use the --ddplan option? (yes/no)"
read use_ddplan

# Prompt the user to specify the configuration file
echo "Enter the path to the configuration file:"
read config_file

# Split the configuration file into chunks of 5 lines each
split -l 3 "$config_file" chunk_

# Process each chunk sequentially
for chunk in chunk_*
do
    if [ "$use_ddplan" = "yes" ]; then
        # Run transientx_fil with ddplan option
        cat "$chunk" | xargs -n 12 -P 5 bash -c 'run_transientx_ddplan "$@"' _
    else
        # Run transientx_fil without ddplan option
        cat "$chunk" | xargs -n 14 -P 5 bash -c 'run_transientx "$@"' _
    fi
    # Clean up the chunk file after processing
    rm "$chunk"
done

