from PyTexturePacker import Packer
import sys
from pathlib import Path
import json


def pack_tex(folder):
    packer = Packer.create(max_width=4096, max_height=4096,
                           enable_rotated=False, atlas_format='json')
    packer.pack(str(folder), str(folder), "")


def update_uvd(uvd_file, group_file):
    with open(uvd_file, encoding='UTF-8') as f:
        data = json.loads(f.read())
    if Path.exists(group_file):
        print(group_file)
        group = group_file.stem
        print('group found')
        with open(group_file, encoding='UTF-8') as f:
            plist = json.loads(f.read())
        group_id = None
        for item in data['Groups']:
            print(data['Groups'][item]["Name"])
            if group == data['Groups'][item]["Name"]:
                print("good")
                group_id = item
                break
        for item in data['Groups'][group_id]['Items']:
            item_data = data['Groups'][group_id]['Items'][item]
            p_data = plist['frames'][f"{item_data['Name']}.png"]
            item_data["X Position in File"] = p_data['frame']['x']
            item_data["Y Position in File"] = p_data['frame']['y']
            item_data['Item Size X'] = p_data['frame']['w']
            item_data['Item Size Y'] = p_data['frame']['h']
            item_data['Tex Size W'] = plist['meta']['size']['w']
            item_data['Tex Size H'] = plist['meta']['size']['h']
    with open(f'{uvd_file}', 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=2)


def main():
    input_folders = sys.argv[1:]
    file_count = 0
    if len(input_folders) == 0:
        input("No files inputted. Drag the sprite folder(s) onto the script to repack.\nPress ENTER to continue...")
        return
    for folder in input_folders:
        folder = Path(folder)
        if folder.is_dir():
            pack_tex(folder)
            uvd_file = str(folder.parents[0]).removesuffix(
                "".join(folder.parents[0].suffixes)) + ".uvd.json"
            update_uvd(uvd_file, folder.with_suffix(".json"))
        file_count += 1

    print(f'{file_count} file(s) packed.')


if __name__ == '__main__':
    main()
