# a messy thing by Timo654, mostly copy pasted together from stuff cabalex had

import json
from binary_reader import BinaryReader
import struct
from .tegrax1swizzle import getImageData, compressImageData, returnFormatTable
import subprocess
import os

formats = {
    # DDS
    0x1: "R4_G4_UNORM",  # FIXME: does not work, here just to prevent crash
    0x25: "R8G8B8A8_UNORM",
    0x42: "BC1_UNORM",
    0x43: "BC2_UNORM",
    0x44: "BC3_UNORM",
    0x45: "BC4_UNORM",
    0x46: "BC1_UNORM_SRGB",
    0x47: "BC2_UNORM_SRGB",
    0x48: "BC3_UNORM_SRGB",
    0x49: "BC4_SNORM",
    0x50: "BC6H_UF16",
    # ASTC (weird texture formats ??)
    0x2D: "ASTC_4x4_UNORM",
    0x38: "ASTC_8x8_UNORM",
    0x3A: "ASTC_12x12_UNORM",
    # ASTC
    0x79: "ASTC_4x4_UNORM",
    0x80: "ASTC_8x8_UNORM",
    0x87: "ASTC_4x4_SRGB",
    0x8E: "ASTC_8x8_SRGB",
    # Unknown NieR switch formats
    0x7D: "ASTC_6x6_UNORM",
    0x8B: "ASTC_6x6_SRGB",
}


class DDSHeader(object):
    # https://docs.microsoft.com/en-us/windows/win32/direct3ddds/dds-header
    class DDSPixelFormat(object):
        def __init__(self, pixelFormat):
            self.size = 32
            self.flags = 4  # contains fourcc
            if pixelFormat["_format"] == "BC6H_UF16" or pixelFormat["_format"] == "R8G8B8A8_UNORM":
                self.fourCC = b'DX10'
            elif pixelFormat["_format"].startswith("BC1"):
                self.fourCC = b'DXT1'
            elif pixelFormat["_format"].startswith("BC2"):
                self.fourCC = b'DXT3'
            else:
                self.fourCC = b'DXT5'
            # BC1 = DXT1, BC2 = DXT3, above is DXT5 i think; BC6H is the only DX10 format
            self.RGBBitCount = 0
            self.RBitMask = 0x00000000
            self.GBitMask = 0x00000000
            self.BBitMask = 0x00000000
            self.ABitMask = 0x00000000

    def __init__(self, texture):
        self.magic = b'DDS\x20'
        self.size = 124
        # Defaults (caps, height, width, pixelformat) + mipmapcount and linearsize
        self.flags = 0x1 + 0x2 + 0x4 + 0x1000 + 0x20000 + 0x80000
        self.height = texture["height"]
        self.width = texture["width"]
        self._format = texture["_format"]
        if self._format == "R8G8B8A8_UNORM":
            self.pitchOrLinearSize = ((self.width + 1) >> 1) * 4
        else:
            # https://docs.microsoft.com/en-us/windows/win32/direct3ddds/dx-graphics-dds-pguide
            self.pitchOrLinearSize = int(
                max(1, ((self.width+3)/4)) * returnFormatTable(self._format)[0])
        self.depth = texture["depth"]
        # texture["mipCount # Setting this to the normal value breaks everything, don't do that
        self.mipmapCount = 1
        self.reserved1 = [0x00000000] * 11
        self.ddspf = self.DDSPixelFormat(texture)
        self.caps = 4198408  # Defaults (DDSCAPS_TEXTURE) + mipmap and complex
        self.caps2 = 0
        self.caps3 = 0
        self.caps4 = 0
        self.reserved2 = 0

    def save(self):
        output = self.magic + struct.pack("20I4s10I", self.size, self.flags, self.height, self.width, self.pitchOrLinearSize, self.depth,
                                          self.mipmapCount, self.reserved1[0], self.reserved1[
                                              1], self.reserved1[2], self.reserved1[3], self.reserved1[4],
                                          self.reserved1[5], self.reserved1[6], self.reserved1[
                                              7], self.reserved1[8], self.reserved1[9], self.reserved1[10],
                                          self.ddspf.size, self.ddspf.flags, self.ddspf.fourCC, self.ddspf.RGBBitCount, self.ddspf.RBitMask, self.ddspf.GBitMask,
                                          self.ddspf.BBitMask, self.ddspf.ABitMask, self.caps, self.caps2, self.caps3, self.caps4, self.reserved2)
        if self._format == "BC6H_UF16":
            output += bytearray(
                b"\x5F\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00")
        elif self._format == "R8G8B8A8_UNORM":
            output += bytearray(
                b"\x1C\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00")
        return output


def rebuild(input_file):
    if os.path.exists(f"{input_file[:-4]}_info.json"):
        with open(f"{input_file[:-4]}_info.json", encoding='UTF-8') as f:
            data = json.loads(f.read())
    else:
        print("JSON metadata file not found, skipping", input_file)
        return False
    if data["_format"].startswith("ASTC"):
        subprocess.run(
            f'./lib/astcenc-avx2.exe -cs "{input_file}" "{input_file[:-4]}-TEMP.astc" {data["_format"].split("_")[1]} -medium',
            shell = True)
        with open(f"{input_file[:-4]}-TEMP.astc", "rb") as f:
            xt1 = BinaryReader(f.read())
        if xt1.read_uint32() != 1554098963:
            print("Invalid XT1 file!")
            return
        header_length = 0x10
        with open(input_file, "rb") as f:
            png = BinaryReader(f.read(), True)

        png.seek(0x10)
        data["width"] = png.read_uint32()
        data["height"] = png.read_uint32()
        data["mipCount"] = 1  # astc encoder can't do mipmaps
    else:
        # DDS
        with open(input_file, "rb") as f:
            xt1 = BinaryReader(f.read())
        xt1.seek(0xC)
        data["height"] = xt1.read_uint32()
        data["width"] = xt1.read_uint32()
        xt1.seek(0x1C)
        data["mipCount"] = xt1.read_uint32()
        xt1.seek(0x54)
        fourCC = xt1.read_str()
        if fourCC == "DX10":
            header_length = 0x94
        else:
            header_length = 0x80
    if data["_format"].startswith("ASTC_6x6") and (data["width"] >= 1024 or data["height"] >= 1024):
        print("Large ASTC 6x6 texture detected, swizzling will probably be broken! Try switching to a different format.")
    # the json stores the type as text for easier understanding for the end user
    data["_formatval"] = dict(zip(formats.values(), formats.keys()))[
        data["_format"]]
    data["imageSize"] = xt1.size() - header_length
    blockHeightLog2 = data["textureLayout"] & 7
    texture = compressImageData(
        data, xt1.buffer()[header_length:], 0, 0, 0, blockHeightLog2, 1)
    head = BinaryReader()
    head.write_uint32(3232856)  # magic
    head.write_uint32(data["unknown"])
    head.write_uint64(data["width"]*data["height"])
    head.write_uint32(56)
    # TODO - should verify if DDS can handle mip counts above 1
    head.write_uint32(data["mipCount"])
    head.write_uint32(data["_typeval"])
    head.write_uint32(data["_formatval"])
    head.write_uint32(data["width"])
    head.write_uint32(data["height"])
    head.write_uint32(data["depth"])
    head.write_uint32(data["unknown4"])
    head.write_uint32(data["textureLayout"])
    head.write_uint32(data["textureLayout2"])

    with open(f"{input_file[:-4]}.xt1", "wb") as f:
        f.write(head.buffer())
        f.write(texture)
    if os.path.exists(f"{input_file[:-4]}-TEMP.astc"):
        os.remove(f"{input_file[:-4]}-TEMP.astc")
    return True


def read_file(filename):
    with open(filename, 'rb') as file:
        xt1 = BinaryReader(file.read())
    data = dict()
    if xt1.read_int32() != 3232856:
        print("Not a valid XT1 file.")
        return False
    data["unknown"] = xt1.read_int32()
    xt1.seek(8, 1)  # image size + header size
    data["headerSize"] = xt1.read_int32()
    data["mipCount"] = xt1.read_int32()
    data["_typeval"] = xt1.read_int32()
    data["_formatval"] = xt1.read_int32()
    data["width"] = xt1.read_int32()
    data["height"] = xt1.read_int32()
    data["depth"] = xt1.read_int32()
    data["unknown4"] = xt1.read_int32()
    data["textureLayout"] = xt1.read_int32()
    data["textureLayout2"] = xt1.read_int32()
    data["arrayCount"] = 1
    surfaceTypes = ["T_1D", "T_2D", "T_3D", "T_Cube", "T_1D_Array",
                    "T_2D_Array", "T_2D_Multisample", "T_2D_Multisample_Array", "T_Cube_Array"]
    #print("formatval:", data["_formatval"])
    data["_format"] = formats[data["_formatval"]]
    if data["_format"].startswith("ASTC_6x6") and (data["width"] >= 1024 or data["height"] >= 1024):
        print("Large ASTC 6x6 texture detected, swizzling might be broken!")
    data["_type"] = surfaceTypes[data["_typeval"]]
    if data["_type"] in ["T_Cube", "T_Cube_Array"]:
        data["ArrayCount"] = 6
    blockHeightLog2 = data["textureLayout"] & 7
    texture = getImageData(data, xt1.buffer()[data["headerSize"]:], 0,
                           0, 0, blockHeightLog2, 1)

    formatInfo = returnFormatTable(data["_format"])
    if data["_format"].startswith("ASTC"):  # Texture is ASTC
        outBuffer = b''.join([
                    b'\x13\xAB\xA1\x5C', formatInfo[1].to_bytes(
                        1, "little"),
                    formatInfo[2].to_bytes(1, "little"), b'\1',
                    data["width"].to_bytes(3, "little"),
                    data["height"].to_bytes(3, "little"), b'\1\0\0',
                    texture,
        ])
        with open(f'{filename}_TEMP.astc', 'wb') as f:
            f.write(outBuffer)
        subprocess.run(
            f'./lib/astcenc-avx2.exe -ds "{filename}_TEMP.astc" "{filename[:-4]}.png"',
            shell = True)
        os.remove(f'{filename}_TEMP.astc')
    else:
        headerDataObject = DDSHeader(data)
        headerData = headerDataObject.save()
        finalTexture = headerData + texture
        with open(f'{filename[:-4]}.dds', 'wb') as f:
            f.write(finalTexture)
    # these values are not really needed for repackng, they can be generated
    del data["width"]
    del data["height"]
    del data["_formatval"]
    del data["headerSize"]
    del data["mipCount"]
    with open(f'{filename[:-4]}_info.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=2)
    return True
