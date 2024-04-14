# Raz/Kraze SPI Flash Dump Repacker
# https://github.com/ginbot86/ColorLCDVape-RE

import os

def reassemble_flash_dump(input_dir):
    # Initialize a bytearray with 1 MiB size filled with 0xFF
    assembled_data = bytearray([0xFF] * 1048576)

    # Get list of split files
    split_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    # Iterate over split files and insert their contents into the assembled_data at the correct offsets
    for split_file in split_files:
        hex_offset = get_hex_offset(split_file)
        if hex_offset is not None:
            with open(os.path.join(input_dir, split_file), 'rb') as f:
                print(f"Reading file {split_file}...")
                data = f.read()
                # Insert data into assembled_data at the correct offset
                print(f"Inserting data at offset 0x{hex_offset:x}, length 0x{len(data):x}")
                assembled_data[hex_offset:hex_offset + len(data)] = data
        else:
            print(f"Skipping nonconforming file: {split_file}")

    # Write assembled binary data to a file
    output_filename = os.path.join(input_dir, os.path.basename(input_dir) + "_assembled.bin")
    with open(output_filename, 'wb') as output_file:
        output_file.write(assembled_data)

    print(f"Flash dump reassembled successfully. Output file: {output_filename}")

def get_hex_offset(filename):
    try:
        return int(filename.split('_')[1], 16)
    except (IndexError, ValueError):
        return None  # Return None for filenames that don't match the expected format

if __name__ == "__main__":
    input_dir = input("Enter the directory containing split files: ")
    reassemble_flash_dump(input_dir)
