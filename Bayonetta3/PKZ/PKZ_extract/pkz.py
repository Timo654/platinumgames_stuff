# Bayonetta 3 PKZ extractor, based on https://gist.github.com/NWPlayer123/27199c50ae7ee83cb3e3fd06ea4b3d82 by NWPlayer123
# edited to work with Bayo3 by Timo654

from struct import unpack, pack
from os.path import exists, dirname, join
from os import makedirs, remove
import sys
import subprocess
from time import sleep


def read32(f):
    return unpack("<I", f.read(4))[0]


def getstr(f):
    ret = b""
    char = f.read(1)
    while char != b"\x00":
        ret += char
        char = f.read(1)
    if f.tell() % 8:  # normally don't align but only strings here are
        f.seek(8 - (f.tell() % 8), 1)
    return ret

ooz_path = join(dirname(__file__), f'ooz.exe')
if not exists(ooz_path):
    input("Missing ooz.exe...\nPress enter to exit.")
    sys.exit()
if len(sys.argv) == 1:
    input("Drag and drop a PKZ file onto the script to use.\nPress enter to exit.")
    sys.exit()

with open(sys.argv[1], "rb") as f:
    outname = sys.argv[1][:-4]
    assert f.read(4) == b"pkzl"  # magic
    assert read32(f) == 0x20000  # ??? version?
    f.seek(0, 2)
    full_size = f.tell()
    f.seek(8)
    assert read32(f) == full_size  # assert file+8 = filesize
    header = unpack("<5I", f.read(0x14))  # 0x20 header
    entries = [unpack("<2I3Q", f.read(32))
               for i in range(header[1])]  # 4 lwords
    fileinfos = list()
    for i in range(len(entries)):
        f.seek(entries[i][0] + header[2] + header[1]*0x20)
        name = getstr(f).decode("UTF-8")
        f.seek(entries[i][1] + header[2] + header[1]*0x20)
        compression = getstr(f).decode("UTF-8")
        fileinfos.append((name, compression))
    # variable length, aligned to 8-byte boundary, "UTF-8" so py3's happy >.>
    for i in range(header[1]):
        filename = fileinfos[i][0]
        compression = fileinfos[i][1]
        item_path = join(outname, dirname(filename))
        if (compression == "None"):
            print("Uncompressed -", filename)  # pretty print
            if not exists(item_path):  # make output folder if it doesn't exist
                makedirs(item_path)
            with open(join(outname, filename), "wb") as o:
                f.seek(entries[i][3])  # seek to entry_offset
                o.write(f.read(entries[i][4]))  # decompress dec_size
        # compressed
        elif (compression == "OodleKraken"):
            print("Compressed -", filename)  # pretty print
            if not exists(item_path):  # make output folder if it doesn't exist
                makedirs(item_path)
            with open(join(outname, filename + "_enc"), "wb") as o:
                f.seek(entries[i][3])  # seek to entry_offset
                o.write(pack("<Q", entries[i][2]))
                o.write(f.read(entries[i][4]))  # decompress dec_size
            subprocess.run(
                f'{ooz_path} -d "{outname}/{filename}_enc" "{outname}/{filename}"', shell=True)
            remove(join(outname, filename + "_enc"))
        else:
            print("Unknown compression -", compression)
print("Finished!")
sleep(2)
