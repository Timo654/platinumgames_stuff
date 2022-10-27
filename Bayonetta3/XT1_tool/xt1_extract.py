import sys
import os
from lib.xt1_lib import read_file

def main():
    input_files = sys.argv[1:]
    if len(input_files) == 0:
        input("To use the tool, drag XT1 file(s) or folder(s) containing XT1 files onto the script.\nPress ENTER to continue...")
        input()
        sys.exit()

    file_count = 0
    for file in input_files:
        if os.path.isdir(file):
            for item in os.listdir(file):
                if item.endswith(".xt1"):
                    read_file(os.path.join(file, item))
        elif file.endswith(".xt1"):
            read_file(file)
        file_count += 1
    print(f'{file_count} file(s) converted.')
if __name__ == "__main__":
    main()
