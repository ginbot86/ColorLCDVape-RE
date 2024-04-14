# Raz/Kraze SPI Flash Dump Splitter/Unpacker
# https://github.com/ginbot86/ColorLCDVape-RE

import os
import csv

def read_image_info(csv_file):
    image_info = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            index = int(row['Index'])
            offset = int(row['OffsetHex'], 16)  # Convert hex string to integer
            length = int(row['LengthHex'], 16)  # Convert hex string to integer
            img_x = int(row['ImgX'])
            img_y = int(row['ImgY'])
            category = row['Category']
            sequence = int(row['Sequence'])
            image_info.append((index, offset, length, img_x, img_y, category, sequence))
    return image_info

def split_flash_dump(flash_dump_path, image_info):
    # Validate Flash dump size
    if os.path.getsize(flash_dump_path) != 0x100000:  # 1 MiB
        print("Error: Invalid Flash dump size.")
        return

    # Create output directory based on input filename
    filename = os.path.splitext(os.path.basename(flash_dump_path))[0]
    output_folder = filename
    os.makedirs(output_folder, exist_ok=True)

    # Read and split Flash dump
    with open(flash_dump_path, 'rb') as f:
        for index, offset, length, img_x, img_y, category, sequence in image_info:
            f.seek(offset)
            image_data = f.read(length)
            filename = f"{index}_{offset:x}_{img_x}x{img_y}_{category}-{sequence}.bin"  # Format filename
            image_path = os.path.join(output_folder, filename)
            with open(image_path, 'wb') as img_file:
                img_file.write(image_data)

    print("Flash dump split successfully.")

if __name__ == "__main__":
    csv_file = "split_map.csv"
    flash_dump_path = input("Enter the path to the Flash dump file: ")
    image_info = read_image_info(csv_file)
    split_flash_dump(flash_dump_path, image_info)
