import json
from binary_reader import BinaryReader, Endian
import sys



def rebuild(input_file):
    with open(input_file, encoding='UTF-8') as f:
        data = json.loads(f.read())
    # header
    head = BinaryReader()
    group_br = BinaryReader()
    if data["Endianness"] == 'big':
        group_br.set_endian(Endian.BIG)
        head.set_endian(Endian.BIG)

    head.write_uint32(len(data['Groups']))  # endian check
    item_count = 0
    for group in data['Groups']:
        item_count += len(data['Groups'][group]['Items'])
    head.write_uint32(item_count)
    head.write_uint32(0x10)  # Item Pointer
    head.write_uint32(0x10 + 96 * item_count) # group pointer


    for group in data['Group order']:
        group_br.write_str_fixed(data['Groups'][str(group)]['Name'],size=32)
        group_br.write_uint32(int(group))

    for item in data['Item order']:
            item_data = data['Groups'][str(item[0])]['Items'][str(item[1])]
            head.write_str_fixed(item_data['Name'], size=64)
            head.write_uint32(item[1])
            head.write_uint32(item[0])
            head.write_float(item_data["X Position in File"])
            head.write_float(item_data["Y Position in File"])
            head.write_float(item_data["Item Size X"])
            head.write_float(item_data["Item Size Y"])
            head.write_float(1 / item_data["Tex Size W"])
            head.write_float(1 / item_data["Tex Size H"])

    print(f'Rebuilding {input_file}...')

    head.extend(group_br.buffer())
    with open(f'{input_file}.uvd', 'wb') as f:
        f.write(head.buffer())

def read_file(filename, endianness="little"):
    with open(filename, 'rb') as file:
        uvd = BinaryReader(file.read())
    if endianness == 'big':
        uvd.set_endian(Endian.BIG)
    data = dict()
    data["Endianness"] = endianness
    data['Group count'] = uvd.read_uint32()
    data['Item count'] = uvd.read_uint32()
    data['Groups'] = dict()
    data['Group order'] = list()
    data['Item order'] = list()
    item_pointer = uvd.read_uint32()
    group_pointer = uvd.read_uint32()
    uvd.seek(group_pointer)
    for i in range(data['Group count']):
        group = dict()
        group['Name'] = uvd.read_str(32)
        group['Items'] = dict()
        group_id = uvd.read_uint32()
        data['Groups'][group_id] = group
        data['Group order'].append(group_id)
    
    uvd.seek(item_pointer)
    for i in range(data['Item count']):
        item = dict()
        item['Name'] = uvd.read_str(64)
        item_id = uvd.read_uint32()
        group_id = uvd.read_uint32()
        item['X Position in File'] = uvd.read_float()
        item['Y Position in File'] = uvd.read_float()
        item['Item Size X'] = uvd.read_float()
        item['Item Size Y'] = uvd.read_float()
        item['Tex Size W'] =  1 / uvd.read_float()
        item['Tex Size H'] = 1 / uvd.read_float()
        data['Groups'][group_id]['Items'][item_id] = item
        data['Item order'].append((group_id, item_id))

    with open(f'{filename}.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=2)

def main():
    input_files = sys.argv[1:]
    file_count = 0
    for file in input_files:
        if file.endswith(".json"):
            rebuild(file)
        else:
            read_file(file)
        file_count += 1

    print(f'{file_count} file(s) converted.')


if __name__ == "__main__":
    main()
