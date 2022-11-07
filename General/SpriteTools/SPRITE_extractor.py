import json
from pathlib import Path
from PIL import Image
import sys


def read_file(filename, folder):
    with open(filename, encoding='UTF-8') as f:
        data = json.loads(f.read())
    for group in data['Groups']:
        img_name = Path(f"{folder}/{data['Groups'][group]['Name']}.png")
        if Path.exists(img_name):
            with Image.open(img_name) as im:
                for sprite in data['Groups'][group]['Items']:
                    sprite_data = data['Groups'][group]['Items'][sprite]
                    temp_img = im.crop((sprite_data['X Position in File'], sprite_data['Y Position in File'], sprite_data[
                        'X Position in File'] + sprite_data['Item Size X'], sprite_data['Y Position in File'] + sprite_data['Item Size Y']))
                    group_out = f"{folder}/{data['Groups'][group]['Name']}"
                    Path(group_out).mkdir(parents=True, exist_ok=True)
                    temp_img.save(f"{group_out}/{sprite_data['Name']}.png")
        else:
            print('no such image, skipping')
            print(img_name)


# takes uvd.json as input
def main():
    input_files = sys.argv[1:]
    file_count = 0
    if len(input_files) == 0:
        input("No input files found. Drag the uvd.json file onto the script to unpack the spritesheet.\nPress ENTER to continue...")
        return
    for file in input_files:
        file = Path(file)
        files = [x for x in Path(file.parents[0]).glob(
            '**/*') if x.is_dir() and f'{str(file.name).removesuffix("".join(file.suffixes))}.wt' in str(x)]
        input_path = files[0]

        read_file(file, input_path)
        file_count += 1

    print(f'{file_count} file(s) exported.')


if __name__ == "__main__":
    main()
