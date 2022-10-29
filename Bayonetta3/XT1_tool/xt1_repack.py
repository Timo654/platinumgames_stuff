import os
import sys
from time import sleep
from lib.xt1_lib import rebuild


def main():
    input_files = sys.argv[1:]
    file_count = 0
    if len(input_files) == 0:
        input("To use the tool, drag PNG/DDS file(s) or folder(s) containing XT1 files onto the script.\nPress ENTER to continue...")
        sys.exit()
    for file in input_files:
        if file.endswith((".png", ".dds")):
            file_count += rebuild(file)
        if os.path.isdir(file):
            for item in os.listdir(file):
                if item.endswith((".png", ".dds")):
                    file_count += rebuild(os.path.join(file, item))
    if file_count == 0:
        print("No valid files found.")
    else:
        print(f'{file_count} file(s) converted.')
    sleep(2)


if __name__ == "__main__":
    main()
