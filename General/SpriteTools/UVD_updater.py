import sys
from pathlib import Path
from SPRITE_packer import update_uvd
import time
def main():
    input_files = sys.argv[1:]
    file_count = 0
    if len(input_files) == 0:
        input("No input files. Drag the repacked sprite's json(s) onto the script to update uvd.json.\nPress ENTER to continue...")
        return
    try:
        for file in input_files:
            file = Path(file)
            if str(file).endswith(".json"):
                uvd_file = str(file.parents[0]).removesuffix("".join(file.parents[0].suffixes)) + ".uvd.json"
                update_uvd(uvd_file, file)
            file_count += 1
    except Exception as e:
        print("oh no", e)
    print(f'{file_count} file(s) packed.')
    time.sleep(2)

if __name__ == '__main__':
    main()
