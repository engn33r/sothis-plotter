import matplotlib.pyplot as plt
import json
import argparse
import csv

def parse_args():
    parser = argparse.ArgumentParser(description="sothis plotting tool: visualize blockchain data the easy way")
    parser.add_argument("-i", "--input_file",
                        help="JSON input file", required=True)
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Print parsed x and y values")
    parser.add_argument("-r", "--bytes_right", default=0, type=int,
                        help="Number of bytes to ignore on the right of the storage slot")
    parser.add_argument("-l", "--bytes_left", default=0, type=int,
                        help="Number of bytes to ignore on the left of the storage slot")
    parser.add_argument("-c", "--csv", default=0, type=str,
                        help="CSV output file")
    return parser.parse_args()

def debug(debug_mode: bool, print_msg: str):
    if(debug_mode):
        print(print_msg)

def plot_data(json_file: str, debug_mode: bool, bytes_right: int, bytes_left: int, csv_file: str):
    with open(json_file) as json_data:
        raw_data = json.load(json_data)

    blocknumbers = []
    y_values = []

    # Extract the data from the JSON file
    for datapoint in raw_data["state_changes"]:
        # x-axis shows block number
        x = int(datapoint["block_number"], 16)
        debug(debug_mode, "x: " + str(x))
        blocknumbers.append(x)


        # first extract the proper number of bytes from the storage slot value
        hex_value_without_0x = datapoint["value"][2:] # remove "0x" preceding the value
        left_cutoff = bytes_left*2
        right_cutoff = bytes_right*-2
        if(right_cutoff):
            hex_value_cut_to_size = hex_value_without_0x[left_cutoff:right_cutoff] # multiply by 2 to convert bytes value to hex, 1 byte = 2 hex chars
        else: # if right is zero, ignore right splice cut-off and get value until the end
            hex_value_cut_to_size = hex_value_without_0x[left_cutoff:] # multiply by 2 to convert bytes value to hex, 1 byte = 2 hex chars
        # y-axis shows storage slot value
        y = int(hex_value_cut_to_size, 16)
        debug(debug_mode, "y: " + str(y))
        y_values.append(y)

    # Output CSV if requested
    if (csv_file):
        with open(csv_file, 'w', newline='') as localfile:
            outputfile = csv.writer(localfile, delimiter=',')
            for i in range(len(blocknumbers)):
                print(blocknumbers[i])
                print(y_values[i])
                outputfile.writerow([blocknumbers[i], y_values[i]])

    # Plot the data
    lines = plt.plot(blocknumbers, y_values)
    plt.xlabel('Block Number')
    plt.ylabel('Storage Slot Value')
    plt.setp(lines, color='r')
    plt.show()

if __name__ == "__main__":

    # Parse input arguments
    args = parse_args()
    plot_data(args.input_file, args.debug, args.bytes_right, args.bytes_left, args.csv)
