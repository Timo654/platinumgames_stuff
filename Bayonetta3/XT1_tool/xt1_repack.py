import os
import sys
from lib.xt1_lib import rebuild
def main():
    input_files = sys.argv[1:]
    file_count = 0
    if len(input_files) == 0:
        input("To use the tool, drag PNG/DDS file(s) or folder(s) containing XT1 files onto the script.\nPress ENTER to continue...")
        sys.exit()
    for file in input_files:
        if file.endswith((".png", ".dds")):
            rebuild(file)
        if os.path.isdir(file):
            for item in os.listdir(file):
                if item.endswith((".png", ".dds")):
                    rebuild(os.path.join(file,item))
        file_count += 1

    print(f'{file_count} file(s) converted.')
if __name__ == "__main__":
    main()