from binary_reader import BinaryReader, Whence, Endian
import os
from pathlib import Path
import json
import sys

def write_gtx_info(wtb, data):
    wtb.write_uint32(data['Dimension'])
    wtb.write_uint32(data['Width'])
    wtb.write_uint32(data['Height'])
    wtb.write_uint32(data['Depth'])
    wtb.write_uint32(data['NumMipmaps'])
    wtb.write_uint32(data['Format'])
    wtb.write_uint32(data['AA Mode'])
    wtb.write_uint32(data['Usage'])
    wtb.write_uint32(data['Data length'])
    wtb.write_uint32(data['Data pointer'])
    wtb.write_uint32(data['Mipmaps data length'])
    wtb.write_uint32(data['Mipmaps pointer'])
    wtb.write_uint32(data['Tile mode'])
    wtb.write_uint32(data['Swizzle value'])
    wtb.write_uint32(data['Alignment'])
    wtb.write_uint32(data['Pitch'])
    wtb.write_uint32(data['MipmapOffsets']) # list of 13
    wtb.write_uint32(data['First mipmap'])
    wtb.write_uint32(data['NumMipmaps2'])
    wtb.write_uint32(data['First Slice'])
    wtb.write_uint32(data['NumSlices'])
    wtb.write_uint8(data['Component']) # list of 4
    wtb.write_uint32(data['Texture Registers']) # list of 5

def write_gtx_header(wtb, data):
    # header
    wtb.write_str('Gfx2')
    wtb.write_uint32(0x20) # header size
    wtb.write_uint32(7) # major ver number
    wtb.write_uint32(1) # minor ver number
    wtb.write_uint32(2) # gpu version
    wtb.write_uint32(0) # align mode
    wtb.write_uint32(0) # reserved
    wtb.write_uint32(0) # reserved
    # block header
    wtb.write_str('BLK{')
    wtb.write_uint32(0x20) # block header size
    wtb.write_uint32(1) # major ver number
    wtb.write_uint32(0) # minor ver number
    wtb.write_uint32(0x0B) # GX2 surface block type
    wtb.write_uint32(0x9C) # always 0x9C, if block type is 0x0B
    wtb.write_uint32(0) # unique identifier for block
    wtb.write_uint32(0) # incrementing index
    # block
    wtb.write_uint32(data['Dimension'])
    wtb.write_uint32(data['Width'])
    wtb.write_uint32(data['Height'])
    wtb.write_uint32(data['Depth'])
    wtb.write_uint32(data['NumMipmaps'])
    wtb.write_uint32(data['Format'])
    wtb.write_uint32(data['AA Mode'])
    wtb.write_uint32(data['Usage'])
    wtb.write_uint32(data['Data length'])
    wtb.write_uint32(data['Data pointer'])
    wtb.write_uint32(data['Mipmaps data length'])
    wtb.write_uint32(data['Mipmaps pointer'])
    wtb.write_uint32(data['Tile mode'])
    wtb.write_uint32(data['Swizzle value'])
    wtb.write_uint32(data['Alignment'])
    wtb.write_uint32(data['Pitch'])
    wtb.write_uint32(data['MipmapOffsets']) # list of 13
    wtb.write_uint32(data['First mipmap'])
    wtb.write_uint32(data['NumMipmaps2'])
    wtb.write_uint32(data['First Slice'])
    wtb.write_uint32(data['NumSlices'])
    wtb.write_uint8(data['Component']) # list of 4
    wtb.write_uint32(data['Texture Registers']) # list of 5
    # block header 2
    wtb.write_str('BLK{')
    wtb.write_uint32(0x20) # size
    wtb.write_uint32(1) # major ver number
    wtb.write_uint32(0) # minor ver number
    wtb.write_uint32(0x0C) # swizzled image data block type
    wtb.write_uint32(data['Data length']) # size of the following data
    wtb.write_uint32(0) # unique identifier for block
    wtb.write_uint32(0) # incrementing index
    
def read_gtx_data(wtb):
    data = dict()
    data['Dimension'] = wtb.read_uint32()
    data['Width'] = wtb.read_uint32()
    data['Height'] = wtb.read_uint32()
    data['Depth'] = wtb.read_uint32()
    data['NumMipmaps'] = wtb.read_uint32()
    data['Format'] = wtb.read_uint32()
    data['AA Mode'] = wtb.read_uint32()
    data['Usage'] = wtb.read_uint32()
    data['Data length'] = wtb.read_uint32()
    data['Data pointer'] = wtb.read_uint32()
    data['Mipmaps data length'] = wtb.read_uint32()
    data['Mipmaps pointer'] = wtb.read_uint32()
    data['Tile mode'] = wtb.read_uint32()
    data['Swizzle value'] = wtb.read_uint32()
    data['Alignment'] = wtb.read_uint32()
    data['Pitch'] = wtb.read_uint32()
    data['MipmapOffsets'] = wtb.read_uint32(count=13) # list of 13
    data['First mipmap'] = wtb.read_uint32()
    data['NumMipmaps2'] = wtb.read_uint32()
    data['First Slice'] = wtb.read_uint32()
    data['NumSlices'] = wtb.read_uint32()
    data['Component'] = wtb.read_uint8(count=4) # list of 4
    data['Texture Registers'] = wtb.read_uint32(count=5) # list of 5
    return data
def extract_file(wtb, extract_folder, filename, start_pos, end_pointer, gtx_data, is_AC=False):
    try:
        Path(extract_folder).mkdir(parents=True, exist_ok=True)
    except(FileExistsError):
        print(
            f'File {extract_folder}/{filename} already exists, unable to create.')
    if is_AC and gtx_data != None:
        astc = BinaryReader()
        astc.extend(gtx_data)
        astc.extend(wtb.buffer()[start_pos:end_pointer])
        with open(f'{extract_folder}/{filename}', 'wb') as f:
            f.write(astc.buffer())
    elif gtx_data != None:
        gtx = BinaryReader()
        gtx.set_endian(Endian.BIG)
        write_gtx_header(gtx, gtx_data)
        gtx.extend(wtb.buffer()[start_pos:start_pos + gtx_data['Data length']])
        gtx.seek(0, Whence.END)
        # block header
        gtx.write_str('BLK{')
        gtx.write_uint32(0x20) # block header size
        gtx.write_uint32(1) # major ver number
        gtx.write_uint32(0) # minor ver number
        gtx.write_uint32(1) # end of file block type
        gtx.write_uint32(0) # block size
        gtx.write_uint32(0) # unique identifier for block
        gtx.write_uint32(0) # incrementing index
        with open(f'{extract_folder}/{filename}', 'wb') as f:
            f.write(gtx.buffer())
    else:
        with open(f'{extract_folder}/{filename}', 'wb') as f:
            f.write(wtb.buffer()[start_pos:end_pointer])

# all this code could use some cleanup tbf
def write_rsrc(br, input_file, game):
    try:
        file = open(f'{input_file}', 'rb')
    except:
        print(f'Cannot find {input_file}.')
    ext = BinaryReader(file.read(), True)
    file.close()
    if game == "Bayonetta2WiiU":
        ext.seek(0x40)
        gtx_data = read_gtx_data(ext)
        br.extend(ext.buffer()[0xFC:ext.size()-0x20])
        br.seek(0, whence = Whence.END)
        br.write_uint64(0)
        br.align(0x2000)
    elif game == "AstralChain":
        gtx_data = ext.buffer()[0x0:0x38]
        br.extend(ext.buffer()[0x38:ext.size()])
        br.seek(0, whence = Whence.END)
        br.align(0x1000)
    else:
        gtx_data = None
        br.extend(ext.buffer())
        br.seek(0, whence = Whence.END)
        br.align(0x1000)
    return ext.size(), gtx_data

def calculate_ptr(prev_ptr_pos, prev_entries):
    pointer = prev_ptr_pos + (prev_entries * 4)
    if pointer % 0x20 != 0:
        pointer += 0x20 - (pointer % 0x20)
    return pointer
def pack(pi, po):
    with open(os.path.join(pi,'wtb_data.json'), encoding='UTF-8') as f:
        wtb_data = json.loads(f.read())
    wtb = BinaryReader()
    if wtb_data['Endian'] == 'big':
        wtb.set_endian(Endian.BIG)
    else:
        wtb.set_endian(Endian.LITTLE)
    if wtb_data['Bayonetta 2']:
        header_entries = 9
    else:
        header_entries = 8

    tex_offset_ptr = calculate_ptr(0, header_entries)
    tex_size_ptr = calculate_ptr(tex_offset_ptr, len(wtb_data['Textures']))
    tex_flags_ptr = calculate_ptr(tex_size_ptr, len(wtb_data['Textures']))
    if wtb_data['Is hash']:
        tex_hash_ptr = calculate_ptr(tex_flags_ptr, len(wtb_data['Textures']))
    else:
        tex_hash_ptr = 0
    if wtb_data['Is texture_info']:
        tex_info_ptr = calculate_ptr(tex_hash_ptr, len(wtb_data['Textures']))
    else:
        tex_info_ptr = 0
    if wtb_data['Bayonetta 2']:
        if wtb_data['Endian'] == 'big':
            mipmap_offset_ptr = tex_info_ptr + 192 * len(wtb_data['Textures'])
        else:
            mipmap_offset_ptr = 0
    if wtb_data['WTA']:
        if wtb_data['Is texture_info']:
            if wtb_data['Bayonetta 2']:
                padding = calculate_ptr(mipmap_offset_ptr, len(wtb_data['Textures']))
            else:
                padding = calculate_ptr(tex_info_ptr, len(wtb_data['Textures']))
        elif wtb_data['Is hash']:
            padding = calculate_ptr(tex_hash_ptr, len(wtb_data['Textures']))
        else:
            padding = calculate_ptr(tex_flags_ptr, len(wtb_data['Textures']))
        wtb.pad(padding)
    else:
        wtb.pad(0x1000) # not a thing in wta

    if wtb_data['Bayonetta 2'] and wtb_data['Endian'] == 'little': # future me: it is a thing in wta, but only on Switch i guess
        wtb.pad(0x7B0)

    wtb.seek(0)
    wtb.write_uint32(4346967) # magic
    wtb.write_uint32(wtb_data["Field_0x4"])
    wtb.write_uint32(len(wtb_data['Textures']))
    wtb.write_uint32(tex_offset_ptr)
    wtb.write_uint32(tex_size_ptr)
    wtb.write_uint32(tex_flags_ptr)
    wtb.write_uint32(tex_hash_ptr)
    wtb.write_uint32(tex_info_ptr)
    if wtb_data['Bayonetta 2']:
        wtb.write_uint32(mipmap_offset_ptr)

    file_br = BinaryReader()
    #for i in range(len(wtb_data['Textures'])):
    for i in range(len(wtb_data['Textures'])):
        metadata = wtb_data['Textures'][i]
        wtb.seek(tex_offset_ptr + i * 0x4)
        if wtb_data['WTA']:
            wtb.write_uint32(file_br.pos())
        else:
            wtb.write_uint32(file_br.pos() + wtb.size())
        wtb.seek(tex_flags_ptr + i * 0x4)
        wtb.write_uint8(metadata['Flag1'])
        wtb.write_uint8(metadata['Flag2'])
        wtb.write_uint8(metadata['Flag3'])
        wtb.write_uint8(metadata['Flag4'])

        wtb.seek(tex_hash_ptr + i * 0x4)
        wtb.write_uint32(metadata['Texture Hash'])
        if wtb_data['Bayonetta 2']:
            if wtb_data['Endian'] == 'big':
                wtb.seek(tex_info_ptr + i * 192)
                file_size, gtx_data = write_rsrc(file_br, f'{pi}/{wtb_data["Texture names"][i]}.gtx', "Bayonetta2WiiU")
                write_gtx_info(wtb, gtx_data)
            elif wtb_data["Astral Chain"]:
                wtb.seek(tex_info_ptr + i * 56)
                file_size, astc_data = write_rsrc(file_br, f'{pi}/{wtb_data["Texture names"][i]}.xt1', "AstralChain")
                #print(astc_data)
                #print(wtb.pos())
                wtb.write_bytes(bytes(astc_data))
                file_size -= 56
            else:
                file_size, _ = write_rsrc(file_br, f'{pi}/{wtb_data["Texture names"][i]}.bntx', "Bayonetta2Switch")
        else:
            file_size, _ = write_rsrc(file_br, f'{pi}/{wtb_data["Texture names"][i]}.dds', "Other")

        wtb.seek(tex_size_ptr + i * 0x4)
        wtb.write_uint32(file_size)

        if wtb_data['Bayonetta 2']:
            if wtb_data['Endian'] == 'big':
                wtb.seek(mipmap_offset_ptr)
                wtb.write_uint32(metadata['Mipmap offset PTR'])
    
    wtb.seek(0, Whence.END)
    if wtb_data['WTA']:
        output = po.with_suffix('.wtp')
        with open(output, 'wb') as f:
            f.write(file_br.buffer())
    else:
        wtb.extend(file_br.buffer())
    with open(po, 'wb') as f:
        f.write(wtb.buffer())

def unpack(pi, po, game):
    if not po.is_dir():
        po.mkdir(parents=True)
    with open(pi, 'rb') as file:
        wtb = BinaryReader(file.read())  # reading file as little endian
    magic = wtb.read_uint32()
    wtb_data = dict() # metadata
    if magic == 4346967: # WTB
        wtb_data['Endian'] = 'little'
        endian = Endian.LITTLE
    elif magic == 1465139712: # BTW
        wtb_data['Endian'] = 'big'
        endian = Endian.BIG
    else:
        raise ValueError('Invalid magic', magic)
    
    if pi.suffix == '.wta':
        print('wta mode activated')
        wtb_data['WTA'] = True
        wtp_filename = pi.with_suffix('.wtp')
        with open(wtp_filename, 'rb') as wtp_file:
            wtp = BinaryReader(wtp_file.read())  # reading file as little endian
    else:
        wtb_data['WTA'] = False

    wtb.set_endian(endian)
    wtb_data['Field_0x4'] = wtb.read_uint32()
    wtb_data['Texture count'] = wtb.read_uint32()
    texture_offset_ptr = wtb.read_uint32()
    texture_sizes_ptr = wtb.read_uint32()
    texture_flags_ptr = wtb.read_uint32()
    texture_hash_ptr = wtb.read_uint32()
    texture_info_ptr = wtb.read_uint32()
    if texture_info_ptr == 0:
        wtb_data['Is texture_info'] = False
    else:
        wtb_data['Is texture_info'] = True
    if texture_hash_ptr == 0:
        wtb_data['Is hash'] = False
    else:
        wtb_data['Is hash'] = True
    mipmap_offsets_ptr = wtb.read_uint32()
    if game == 'Bayonetta2':
        wtb_data['Bayonetta 2'] = True
    else:
        wtb_data['Bayonetta 2'] = False
    wtb_data['Astral Chain'] = False
    wtb_data['Textures'] = list()

    wtb_data["Texture names"] = list()
    uvd_path = f'{str(pi)[:-4]}.uvd.json'
    if os.path.exists(uvd_path):
        with open(uvd_path, 'r') as f:
            uvd_data = json.load(f)
        [wtb_data["Texture names"].append(uvd_data["Groups"][str(item)]["Name"]) for item in uvd_data["Group order"]]
    else:
        [wtb_data["Texture names"].append(o) for o in range(wtb_data['Texture count'])]
    for i in range(wtb_data['Texture count']):
        wtb.seek(texture_offset_ptr + i * 0x4) # i * 0x4 so itd get current entry
        tex_pointer = wtb.read_uint32()
        wtb.seek(texture_sizes_ptr + i * 0x4)
        tex_size = wtb.read_uint32()
        # saving metadata
        metadata = dict()
        wtb.seek(texture_flags_ptr + i * 0x4)
        metadata['Index'] = i
        metadata['Flag1'] = wtb.read_uint8()
        metadata['Flag2'] = wtb.read_uint8()
        metadata['Flag3'] = wtb.read_uint8()
        metadata['Flag4'] = wtb.read_uint8()
        if wtb_data['Is hash']:
            wtb.seek(texture_hash_ptr + i * 0x4)
            metadata['Texture Hash'] = wtb.read_uint32()
        if wtb_data['Is texture_info']:
            if wtb_data['Bayonetta 2'] and wtb_data['Endian'] == 'big':
                wtb.seek(texture_info_ptr + i * 192)
                print('prepare for pain')
                gtx_data = read_gtx_data(wtb)
            else:
                wtb.seek(texture_info_ptr + i * 56)
                metadata['Texture Info'] = wtb.read_uint32()
                if metadata['Texture Info'] == 3232856:
                    wtb.seek(-4, Whence.CUR)
                    wtb_data['Astral Chain'] = True
                    print("Astral Chain detected")
                    xt1_data = wtb.read_bytes(56)
                    print("read xt1 data")
        if wtb_data['Bayonetta 2']:
            wtb.seek(mipmap_offsets_ptr + i * 0x4)
            metadata['Mipmap offset PTR'] = wtb.read_uint32()
        if wtb_data['WTA']:
            if wtb_data['Bayonetta 2']:
                if wtb_data['Endian'] == 'big':
                    extract_file(wtp, po, f'{wtb_data["Texture names"][i]}.gtx', tex_pointer, tex_pointer + tex_size, gtx_data)
                elif wtb_data["Astral Chain"]:
                    extract_file(wtp, po, f'{wtb_data["Texture names"][i]}.xt1', tex_pointer, tex_pointer + tex_size, xt1_data, True)
                else:
                    extract_file(wtp, po, f'{wtb_data["Texture names"][i]}.bntx', tex_pointer, tex_pointer + tex_size, None)
            else:
                extract_file(wtp, po, f'{wtb_data["Texture names"][i]}.dds', tex_pointer, tex_pointer + tex_size, None)
        else:
            extract_file(wtb, po, f'{wtb_data["Texture names"][i]}.dds', tex_pointer, tex_pointer + tex_size, None)

        wtb_data['Textures'].append(metadata)
    with open(os.path.join(po, 'wtb_data.json'), 'w', encoding='UTF-8') as f:
        json.dump(wtb_data, f, indent=4) 

def main():
    input_files = sys.argv[1:]
    if len(input_files) == 0:
        input("No input files. Drag and drop wta files or extracted wta folders onto the script.")
    for file in input_files:
        pi = Path(file)
        game = 'Bayonetta2' # this is actually also used for bayo3 and astral chain. basically anything but MGRR. i should really  clean it up
        if pi.is_dir():
            print('Repacking...')
            po = pi.parent / f"{pi.name}.wta" # TODO - use correct extension
            pack(pi, po)
            print(f'File saved to {po}')
        else:
            print('Unpacking...')
            po = pi.parent / f"{pi.name}_ex"
            unpack(pi, po, game)
            print(f'File unpacked to {po}')

if __name__ == "__main__":
    main()
