import json
from binary_reader import BinaryReader, Endian
import argparse

ENDIANNESS = 'LITTLE'

def rebuild(input_file):
    print(f'Rebuilding {input_file}...')
    with open(input_file, encoding='UTF-8') as f:
        data = json.loads(f.read())
    # header
    head = BinaryReader()
    if ENDIANNESS == 'BIG':
        head.set_endian(Endian.BIG)
    head.write_str_fixed('EFF', size=4)
    head.write_uint32(len(data['Data2']))  # item count
    header_pointer_pos = head.pos()
    head.write_uint32(0) # first data pointer
    head.write_uint32(0)  # second data pointer
    head.write_uint32(0) # third data pointer
    head.write_uint32(data['Unk1'])
    head.write_uint32(len(data['Data2'][0]['Data']))
    head.write_uint32(0) # Padding?
    text = BinaryReader()
    data_br = BinaryReader()
    if ENDIANNESS == 'BIG':
        text.set_endian(Endian.BIG)
        data_br.set_endian(Endian.BIG)

    data_start_pos = list()
    for i in range(len(data['Data2'])):
        data_start_pos.append(data_br.size())
        for e in range(len(data['Data2'][i]['Data'])):
            item = data['Data2'][i]['Data'][e]
            text.write_uint32(0) # padding
            if ENDIANNESS == 'BIG':
                text.write_str_fixed(item['Name'][::-1], size=4)
            else:
                text.write_str_fixed(item['Name'], size=4)
            text.write_uint32(item['Size'])
            if item['Size'] == 0:
                text.write_uint32(0) # no data, no pointer
            else:
                text.write_uint32(data_br.size() - data_start_pos[i]) # pointer to data
                if item['Name'] == 'PART':
                    data_br.write_uint16(item['Data']['Unk1'])
                    data_br.write_uint16(item['Data']['Unk2'])
                    data_br.write_uint32(item['Data']['Unk3'])
                    data_br.write_uint32(item['Data']['Unk4'])
                    data_br.write_uint16(item['Data']['Unk5'])
                    data_br.write_uint16(item['Data']['Unk6'])
                    data_br.write_uint32(item['Data']['Unk7'])
                    data_br.write_uint8(item['Data']['Unk8'])
                    data_br.write_uint8(item['Data']['Unk9'])
                    data_br.write_uint8(item['Data']['Unk10'])
                    data_br.write_uint8(item['Data']['Unk11'])
                    data_br.write_uint8(item['Data']['Unk12'])
                    data_br.write_uint8(item['Data']['Unk13'])
                    data_br.write_uint8(item['Data']['Unk14'])
                    data_br.write_uint8(item['Data']['Unk15'])
                    data_br.write_uint32(item['Data']['Unk16'])
                    data_br.write_uint32(item['Data']['Unk17'])
                    for a in range(7):
                        data_br.write_uint32(0) # padding
                elif item['Name'] == 'MOVE':
                    data_br.write_uint32(item['Data']['Unk1'])
                    for float1 in item['Data']['Floats1']:
                        data_br.write_float(float1)
                    data_br.write_uint16(item['Data']['Unk2'])    
                    data_br.write_uint16(item['Data']['Unk3'])    
                    for float2 in item['Data']['Floats2']:
                        data_br.write_float(float2)
                    data_br.write_uint16(item['Data']['Unk4'])
                    data_br.write_uint16(item['Data']['Unk5'])
                    data_br.write_float(item['Data']['Unk6'])
                    data_br.write_uint8(item['Data']['Unk7'])
                    data_br.write_uint8(item['Data']['Unk8'])
                    data_br.write_uint8(item['Data']['Unk9'] )
                    data_br.write_uint8(item['Data']['Unk10'])
                    for float3 in item['Data']['Floats3']:
                        data_br.write_float(float3)
                elif item['Name'] == 'EMIF':
                    data_br.write_uint16(item['Data']['Unk0'])
                    data_br.write_uint16(item['Data']['Unk1'])
                    data_br.write_uint32(item['Data']['Unk2'])
                    data_br.write_uint16(item['Data']['Unk3'])
                    data_br.write_uint16(item['Data']['Unk4'])
                    data_br.write_uint8(item['Data']['Unk5'])
                    data_br.write_uint8(item['Data']['Unk6'])
                    data_br.write_uint8(item['Data']['Unk7'])
                    data_br.write_uint8(item['Data']['Unk8'])
                    data_br.pad(32)
                elif item['Name'] == 'TEX ':
                    data_br.write_float(item['Data']['Unk0'])
                    data_br.write_uint16(item['Data']['Unk1'])
                    data_br.write_uint16(item['Data']['Unk2'])

                    data_br.write_uint32(item['Data']['Unk3'])

                    data_br.write_float(item['Data']['Unk4'])
                    data_br.write_float(item['Data']['Unk5'])
                    data_br.write_float(item['Data']['Unk6'])
                    data_br.write_float(item['Data']['Unk7'])

                    data_br.write_uint16(item['Data']['Unk8'])
                    data_br.write_uint8(item['Data']['Unk9'])
                    data_br.write_uint8(item['Data']['Unk9b'])

                    data_br.write_uint32(item['Data']['Unk10'])

                    data_br.write_uint8(item['Data']['Unk11a'])
                    data_br.write_uint8(item['Data']['Unk11b'])
                    data_br.write_uint8(item['Data']['Unk11c'])
                    data_br.write_uint8(item['Data']['Unk11d'])

                    data_br.write_float(item['Data']['Unk12'])
                    data_br.write_uint16(item['Data']['Unk13'])

                    data_br.write_uint8(item['Data']['Unk13a'])
                    data_br.write_uint8(item['Data']['Unk13b'])
                    data_br.write_uint32(item['Data']['Unk14'])
                    data_br.write_uint32(item['Data']['Unk15'])
                    data_br.write_uint32(item['Data']['Unk16'])
                    data_br.write_uint32(item['Data']['Unk17'])
                    data_br.write_uint32(item['Data']['Unk18'])
                    data_br.write_uint32(item['Data']['Unk19'])
                    data_br.write_uint32(item['Data']['Unk20'])
                    data_br.write_uint32(item['Data']['Unk21'])
                    data_br.write_uint32(item['Data']['Unk22'])

                    data_br.write_float(item['Data']['Unk23'])
                    data_br.write_float(item['Data']['Unk24'])
                    data_br.write_float(item['Data']['Unk25'])
                    
                    data_br.write_uint32(item['Data']['Unk26'])
                    data_br.write_uint32(item['Data']['Unk27'])
                    data_br.write_uint32(item['Data']['Unk28'])
                    data_br.write_uint32(item['Data']['Unk29'])
                    data_br.pad(64)
                elif item['Name'] == 'PSSA':
                    data_br.write_uint32(item['Data']['Unk1'])
                    for float in item['Data']['Floats']:
                        data_br.write_float(float)
                elif item['Name'] == 'FWK ':
                    data_br.write_uint16(item['Data']['Unk1'])
                    data_br.write_uint16(item['Data']['Unk2'])
                    data_br.write_uint16(item['Data']['Unk3'])
                    data_br.write_uint16(item['Data']['Unk4'])
                    data_br.write_uint16(item['Data']['Unk5'])
                    data_br.write_uint16(item['Data']['Unk5b'])
                    data_br.write_uint16(item['Data']['Unk6'])
                    data_br.write_uint16(item['Data']['Unk6b'])
                    data_br.write_uint8(item['Data']['Unk7'])
                    data_br.write_uint8(item['Data']['Unk8'])
                    data_br.write_uint8(item['Data']['Unk9'])
                    data_br.write_uint8(item['Data']['Unk10'])
                    data_br.pad(12)
                elif item['Name'] == 'FVWK':
                    data_br.write_float(item['Data']['Unk1'])
                    data_br.write_float(item['Data']['Unk2'])
                    data_br.write_float(item['Data']['Unk3'])
                    data_br.write_float(item['Data']['Unk4'])
                    data_br.write_float(item['Data']['Unk5'])
                    data_br.write_float(item['Data']['Unk6'])
                    data_br.write_float(item['Data']['Unk7'])
                    data_br.write_float(item['Data']['Unk8'])
                    data_br.write_float(item['Data']['Unk9'])
                    data_br.write_float(item['Data']['Unk10'])
                    data_br.write_float(item['Data']['Unk11'])
                    data_br.write_float(item['Data']['Unk12'])
                    data_br.write_float(item['Data']['Unk13'])
                    data_br.write_float(item['Data']['Unk14'])
                    data_br.write_float(item['Data']['Unk15'])
                    data_br.write_float(item['Data']['Unk16'])
                    data_br.write_float(item['Data']['Unk17'])
                    data_br.write_float(item['Data']['Unk18'])
                    data_br.write_float(item['Data']['Unk19'])
                    data_br.write_float(item['Data']['Unk20'])
                elif item['Name'] == 'EMMV':
                    data_br.write_uint32(item['Data']['Unk1'] )
                    for float1 in item['Data']['Floats1']:
                        data_br.write_float(float1)
                    data_br.write_uint16(item['Data']['Unk2'])
                    data_br.write_uint16(item['Data']['Unk3'])
                    for float2 in item['Data']['Floats2']:
                        data_br.write_float(float2)
                else:
                    raise ValueError('Unknown name', item['Name'])

    pointer_start_pos = head.pos()
    head.pad(len(data_start_pos * 4))
    head.align(16)
    header_size = head.size()
    head.seek(pointer_start_pos)
    for start_pos in data_start_pos:
        head.write_uint32(start_pos + text.size() + header_size)
    head.seek(header_pointer_pos)
    head.write_uint32(pointer_start_pos)
    head.write_uint32(head.size())
    head.write_uint32(head.size() + text.size())    
    text.extend(data_br.buffer())
    text.seek(data_br.size(), 1)
    head.extend(text.buffer())
    head.seek(text.size(), 1)

    with open(f'{input_file}.dat', 'wb') as f:
        f.write(head.buffer())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input",  help='Input file (.bin.json)',
                        type=str, nargs='+')
    args = parser.parse_args()

    input_files = args.input
    file_count = 0
    for file in input_files:

        rebuild(file)
        file_count += 1

    print(f'{file_count} file(s) rebuilt.')


if __name__ == "__main__":
    main()
