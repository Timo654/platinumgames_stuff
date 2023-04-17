import json
from binary_reader import BinaryReader, Endian
import argparse
ENDIANNESS = 'BIG'


def read_file(filename):
    with open(filename, 'rb') as file:
        eff = BinaryReader(file.read())
    if ENDIANNESS == 'BIG':
        eff.set_endian(Endian.BIG)
    data = dict()
    data['Magic'] = eff.read_str(4)
    data['Data count'] = eff.read_uint32()
    data['DataPointer1'] = eff.read_uint32()
    data['DataPointer2'] = eff.read_uint32()
    data['DataPointer3'] = eff.read_uint32()
    data['Unk1'] = eff.read_uint32()
    data['Unk2Count'] = eff.read_uint32()
    data['Empty'] = eff.read_uint32()

    eff.seek(data['DataPointer2'])
    items_list = list()
    for i in range(data['Data count']):
        current_item = dict()
        current_item['Index'] = i
        current_item['Data'] = list()
        for o in range(data['Unk2Count']):
            item = dict()
            item['Empty'] = eff.read_uint32()
            item['Name'] = eff.read_str(4)
            if ENDIANNESS == 'BIG':
                item['Name'] = item['Name'][::-1]
            item['Size'] = eff.read_uint32()
            item['DataPointer'] = eff.read_uint32()
            current_item['Data'].append(item)
        items_list.append(current_item)
    data['Data2'] = items_list

    eff.seek(data['DataPointer1'])
    data_pointers = list()
    for i in range(data['Data count']):
        data_pointers.append(eff.read_uint32())
    for i in range(len(data_pointers)):
        item = dict()
        item['Index'] = i
        item['Pointer'] = data_pointers[i]
        item['Datas'] = list()
        eff.seek(item['Pointer'])
        print(len(data['Data2'][i]['Data']))
        for e in range(len(data['Data2'][i]['Data'])):
            item = data['Data2'][i]['Data'][e]
            if item['Size'] != 0:
                item['Data'] = dict()
                if item['Name'] == 'PART':
                    item['Data']['Unk1'] = eff.read_uint16()
                    item['Data']['Unk2'] = eff.read_uint16()
                    item['Data']['Unk3'] = eff.read_uint32()
                    item['Data']['Unk4'] = eff.read_uint32()
                    item['Data']['Unk5'] = eff.read_uint16()
                    item['Data']['Unk6'] = eff.read_uint16()
                    item['Data']['Unk7'] = eff.read_uint32()
                    item['Data']['Unk8'] = eff.read_uint8()
                    item['Data']['Unk9'] = eff.read_uint8()
                    item['Data']['Unk10'] = eff.read_uint8()
                    item['Data']['Unk11'] = eff.read_uint8()
                    item['Data']['Unk12'] = eff.read_uint8()
                    item['Data']['Unk13'] = eff.read_uint8()
                    item['Data']['Unk14'] = eff.read_uint8()
                    item['Data']['Unk15'] = eff.read_uint8()
                    item['Data']['Unk16'] = eff.read_uint32()
                    item['Data']['Unk17'] = eff.read_uint32()
                    item['Data']['Padding'] = list()
                    for a in range(7):
                        item['Data']['Padding'].append(eff.read_uint32())
                elif item['Name'] == 'MOVE':
                    item['Data']['Unk1'] = eff.read_uint32()
                    item['Data']['Floats1'] = list()
                    for a in range(57):
                        item['Data']['Floats1'].append(eff.read_float())
                    item['Data']['Unk2'] = eff.read_uint16()
                    item['Data']['Unk3'] = eff.read_uint16()
                    item['Data']['Floats2'] = list()
                    for a in range(23):
                        item['Data']['Floats2'].append(eff.read_float())
                    item['Data']['Unk4'] = eff.read_uint16()
                    item['Data']['Unk5'] = eff.read_uint16()
                    item['Data']['Unk6'] = eff.read_float()
                    item['Data']['Unk7'] = eff.read_uint8()
                    item['Data']['Unk8'] = eff.read_uint8()
                    item['Data']['Unk9'] = eff.read_uint8()
                    item['Data']['Unk10'] = eff.read_uint8()
                    item['Data']['Floats3'] = list()
                    for a in range(11):
                        item['Data']['Floats3'].append(eff.read_float())
                elif item['Name'] == "EMIF":
                    item['Data']['Unk0'] = eff.read_uint16()
                    item['Data']['Unk1'] = eff.read_uint16()
                    item['Data']['Unk2'] = eff.read_uint32()
                    item['Data']['Unk3'] = eff.read_uint16()
                    item['Data']['Unk4'] = eff.read_uint16()
                    item['Data']['Unk5'] = eff.read_uint8()
                    item['Data']['Unk6'] = eff.read_uint8()
                    item['Data']['Unk7'] = eff.read_uint8()
                    item['Data']['Unk8'] = eff.read_uint8()
                    item['Data']['Padding'] = list()
                    for a in range(8):
                        item['Data']['Padding'].append(eff.read_uint32())
                elif item['Name'] == 'TEX ':
                    item['Data']['Unk0'] = eff.read_float()
                    item['Data']['Unk1'] = eff.read_uint16()
                    item['Data']['Unk2'] = eff.read_uint16()
                    item['Data']['Unk3'] = eff.read_uint32()
                    item['Data']['Unk4'] = eff.read_float()
                    item['Data']['Unk5'] = eff.read_float()
                    item['Data']['Unk6'] = eff.read_float()
                    item['Data']['Unk7'] = eff.read_float()

                    item['Data']['Unk8'] = eff.read_uint16()
                    item['Data']['Unk9'] = eff.read_uint8()
                    item['Data']['Unk9b'] = eff.read_uint8()

                    item['Data']['Unk10'] = eff.read_uint32()

                    item['Data']['Unk11a'] = eff.read_uint8()
                    item['Data']['Unk11b'] = eff.read_uint8()
                    item['Data']['Unk11c'] = eff.read_uint8()
                    item['Data']['Unk11d'] = eff.read_uint8()

                    item['Data']['Unk12'] = eff.read_float()
                    item['Data']['Unk13'] = eff.read_uint16()
                    item['Data']['Unk13a'] = eff.read_uint8()
                    item['Data']['Unk13b'] = eff.read_uint8()
                    item['Data']['Unk14'] = eff.read_uint32()
                    item['Data']['Unk15'] = eff.read_uint32()
                    item['Data']['Unk16'] = eff.read_uint32()
                    item['Data']['Unk17'] = eff.read_uint32()
                    item['Data']['Unk18'] = eff.read_uint32()
                    item['Data']['Unk19'] = eff.read_uint32()
                    item['Data']['Unk20'] = eff.read_uint32()
                    item['Data']['Unk21'] = eff.read_uint32()
                    item['Data']['Unk22'] = eff.read_uint32()

                    item['Data']['Unk23'] = eff.read_float()
                    item['Data']['Unk24'] = eff.read_float()
                    item['Data']['Unk25'] = eff.read_float()

                    item['Data']['Unk26'] = eff.read_uint32()
                    item['Data']['Unk27'] = eff.read_uint32()
                    item['Data']['Unk28'] = eff.read_uint32()
                    item['Data']['Unk29'] = eff.read_uint32()
                    item['Data']['Padding'] = list()
                    for a in range(16):
                        item['Data']['Padding'].append(eff.read_uint32())
                elif item['Name'] == 'PSSA':
                    item['Data']['Unk1'] = eff.read_uint32()
                    item['Data']['Floats'] = list()
                    for a in range(23):
                        item['Data']['Floats'].append(eff.read_float())
                elif item['Name'] == 'FWK ':
                    item['Data']['Unk1'] = eff.read_uint16()
                    item['Data']['Unk2'] = eff.read_uint16()
                    item['Data']['Unk3'] = eff.read_uint16()
                    item['Data']['Unk4'] = eff.read_uint16()
                    item['Data']['Unk5'] = eff.read_uint16()
                    item['Data']['Unk5b'] = eff.read_uint16()
                    item['Data']['Unk6'] = eff.read_uint16()
                    item['Data']['Unk6b'] = eff.read_uint16()
                    item['Data']['Unk7'] = eff.read_uint8()
                    item['Data']['Unk8'] = eff.read_uint8()
                    item['Data']['Unk9'] = eff.read_uint8()
                    item['Data']['Unk10'] = eff.read_uint8()
                    item['Data']['Padding'] = list()
                    for a in range(3):
                        item['Data']['Padding'].append(eff.read_uint32())
                elif item['Name'] == 'FVWK':
                    item['Data']['Unk1'] = eff.read_float()
                    item['Data']['Unk2'] = eff.read_float()
                    item['Data']['Unk3'] = eff.read_float()
                    item['Data']['Unk4'] = eff.read_float()
                    item['Data']['Unk5'] = eff.read_float()
                    item['Data']['Unk6'] = eff.read_float()
                    item['Data']['Unk7'] = eff.read_float()
                    item['Data']['Unk8'] = eff.read_float()
                    item['Data']['Unk9'] = eff.read_float()
                    item['Data']['Unk10'] = eff.read_float()
                    item['Data']['Unk11'] = eff.read_float()
                    item['Data']['Unk12'] = eff.read_float()
                    item['Data']['Unk13'] = eff.read_float()
                    item['Data']['Unk14'] = eff.read_float()
                    item['Data']['Unk15'] = eff.read_float()
                    item['Data']['Unk16'] = eff.read_float()
                    item['Data']['Unk17'] = eff.read_float()
                    item['Data']['Unk18'] = eff.read_float()
                    item['Data']['Unk19'] = eff.read_float()
                    item['Data']['Unk20'] = eff.read_float()
                elif item['Name'] == 'EMMV':
                    item['Data']['Unk1'] = eff.read_uint32()
                    item['Data']['Floats1'] = list()
                    for a in range(81):
                        item['Data']['Floats1'].append(eff.read_float())
                    item['Data']['Unk2'] = eff.read_uint16()
                    item['Data']['Unk3'] = eff.read_uint16()
                    item['Data']['Floats2'] = list()
                    for a in range(25):
                        item['Data']['Floats2'].append(eff.read_float())
                else:
                    raise ValueError('Unknown name', item['Name'])
    with open(f'{filename}.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input",  help='Input file (.bin.json)',
                        type=str, nargs='+')
    args = parser.parse_args()

    input_files = args.input
    file_count = 0
    for file in input_files:
        read_file(file)
        file_count += 1

    print(f'{file_count} file(s) exported.')


if __name__ == "__main__":
    main()
