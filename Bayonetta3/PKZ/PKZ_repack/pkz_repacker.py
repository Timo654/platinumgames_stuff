import os
import sys
import math
from struct import unpack, pack
import subprocess
import shutil
from time import sleep


def getstr(f):
    ret = b""
    char = f.read(1)
    while char != b"\x00":
        ret += char
        char = f.read(1)
    if f.tell() % 8:  # normally don't align but only strings here are
        f.seek(8 - (f.tell() % 8), 1)
    return ret


print(
    "--- Bayonetta 3 PKZ REPACKER ---",
    "\nOriginally made by Cabalex, edited for Bayonetta 3 by Timo654"
)

if not os.path.exists("./ooz.exe"):
    input("Missing ooz.exe, which is required for OodleKraken compression...\nPress enter to exit.")
    sys.exit()

if not os.path.exists("./oo2core_7_win64.dll"):
    input("Missing oo2core_7_win64.dll, which is required for OodleKraken compression...\nPress enter to exit.")
    sys.exit()

if not os.path.isdir("replacement/"):
    os.mkdir('replacement')

replacementFiles = [os.path.join(dp[12:], f) for dp, dn, filenames in os.walk(
    "replacement/") for f in filenames]
if len(replacementFiles) == 0:
    print("No use repacking a file without any files to repack with! Insert any files you wanna replace in the replacement/ folder.")
    print("To extract files, use the Bayonetta 3 PKZ extractor.")
    exit()

if len(sys.argv) == 1:
    print(
        "--- HELP ---"
        "Insert your files that are to be replaced in the .PKZ in the replacement/ folder, e.g. .DAT/.DTT, .BIN, etc.",
        "\nThen, run the program with 'zstd-repacker.py <filename>.pkz' to repack 'em."
    )
    exit()

filename = sys.argv[1]
f = open(filename, 'rb')
print("[!] Reading PKZ...")
tmpFiles = []
magic, unk, size, numFiles, offset_file_descriptors, fileNameTableLength = unpack(
    '2IQ2IQ', f.read(32))

for i in range(numFiles):
    unpacked = unpack('2I3Q', f.read(32))
    tmpFiles.append({
        'nameOffset': unpacked[0],
        'compressionOffset': unpacked[1],
        'size': unpacked[2],
        'offset': unpacked[3],
        'compressedSize': unpacked[4],
        'kind': 'extracted'
    })
fileNames = list()
fileCompressions = list()
for i in range(numFiles):
    f.seek(tmpFiles[i]["nameOffset"] + offset_file_descriptors + numFiles*0x20)
    name = getstr(f).decode("UTF-8")
    f.seek(tmpFiles[i]["compressionOffset"] +
           offset_file_descriptors + numFiles*0x20)
    compression = getstr(f).decode("UTF-8")
    fileNames.append(name)
    fileCompressions.append(compression)


files = {}
offset = tmpFiles[0]['offset']
for i, fname in enumerate(fileNames):
    files[fname] = tmpFiles[i]
    compression = fileCompressions[i]
    files[fname]['newOffset'] = offset
    if os.path.normpath(fname) in replacementFiles:
        files[fname]['kind'] = "custom"
        files[fname]['size'] = os.stat(f"replacement/{fname}").st_size
        # Probably not the most optimized but eh
        if compression == "OodleKraken":
            print(f"[+] Found {fname} - Repacking with OodleKraken...")
            item_path = os.path.join("compressed", os.path.dirname(fname))
            # make output folder if it doesn't exist
            if not os.path.exists(item_path):
                os.makedirs(item_path)
            subprocess.run(
                f'ooz.exe -z --kraken "replacement/{fname}" "compressed/{fname}"')
            with open(f"compressed/{fname}", 'rb') as rawf:
                files[fname]['fp'] = rawf.read()[8:]
        elif compression == "None":
            print(f"[+] Found {fname} - Repacking with no compression...")
            with open(f"replacement/{fname}", 'rb') as rawf:
                files[fname]['fp'] = rawf.read()
        else:
            raise ValueError("Unknown compression", compression)

        files[fname]['compressedSize'] = len(files[fname]['fp'])
    # Padded to 64 byte increments
    offset += math.ceil(files[fname]['compressedSize']/64)*64


print("[!] Repacking everything...")
# Repack nameTable
nameTableOffsets = []
compressionOffsets = dict()
nameTableStr = b""
for compression in set(fileCompressions):
    compressionOffsets[compression] = len(nameTableStr)
    nameTableStr += compression.encode('utf-8')
    nameTableStr += b''.join([b'\x00'] * (8 - (len(nameTableStr) % 8)))
for fname in fileNames:
    nameTableOffsets.append(len(nameTableStr))
    nameTableStr += fname.encode('utf-8')
    nameTableStr += b''.join([b'\x00'] * (8 - (len(nameTableStr) % 8)))

# Repack
newf = open(filename.replace(".pkz", "new.pkz"), 'wb')
newf.write(pack('2IQ2IQ', magic, unk, 32 + len(nameTableStr) + sum([math.ceil(
    x['compressedSize']/64)*64 for x in files.values()]), numFiles, 32, len(nameTableStr)))

for i, fname in enumerate(fileNames):
    newf.write(pack('<2I3Q', nameTableOffsets[i], compressionOffsets[fileCompressions[i]],
               files[fname]['size'], files[fname]['newOffset'], files[fname]['compressedSize']))
newf.write(nameTableStr)

if newf.tell() < math.ceil(newf.tell()/64)*64:
    newf.write(
        b''.join([b'\x00'] * (math.ceil(newf.tell()/64)*64 - newf.tell())))

# Write files and padding
for fname in fileNames:
    if files[fname]['kind'] == 'custom':
        newf.write(files[fname]['fp'])
    else:
        f.seek(files[fname]['offset'])
        newf.write(f.read(files[fname]['compressedSize']))
    if newf.tell() < math.ceil(newf.tell()/64)*64:
        newf.write(
            b''.join([b'\x00'] * (math.ceil(newf.tell()/64)*64 - newf.tell())))


f.close()
newf.close()
if os.path.exists("compressed"):
    shutil.rmtree("compressed")
print(
    f"--- Finished, {len([x for x in files.values() if x['kind'] == 'custom'])} files replaced ({len(fileNames)} files in PKZ) ---")
sleep(2)
