# XT1 Tool
Requires Python 3.

## Installation: 
Install binary-reader: `pip install binary-reader`

## How to use:
Drag any XT1 files onto xt1_extract.py to convert them to PNG/DDS and xt1_repack.py to reconvert them to XT1. You can drag multiple files, or folders containing the files.
Any PNG/DDS files must have a JSON file next to them containing metadata about the file.

Some formats may be less tested than others, I recommend making sure the texture actually looks proper before trying out in-game, by just reconverting it back to verify.
You can edit the JSON to change the format for the texture (for DDS, the actual file has to also match this new format).

List of currently supported formats can be found [here](lib/xt1_lib.py#L10).

## Known issues:

* ASTC_6x6 swizzling breaks at 2048x2048. 


Thanks to [cabalex](https://github.com/cabalex) for the [Astral Chain Blender plugin](https://github.com/cabalex/AstralChain2Blender), which I butchered for this.

