# SpriteTools
**Sprite Extractor** - extracts sprites from a spritesheet. Requires "pillow". (pip install pillow) and an extracted uvd using UVD Tool.
To use, drag the UVD onto the script. The script will extract all PNG spritesheets in the corresponding wta extract folder (wta has to be extracted and next to uvd.json).

**Sprite Packer** - packs sprites to a spritesheet. Requires "PyTexturePacker" (pip install PyTexturePacker) and an extracted spritesheet using Sprite Extractor.
To use, drag the extracted spritesheet folder onto the script. The script will repack the spritesheet to PNG and update the uvd.json in the dir above.

**UVD Updater** - updates the uvd.json positions based on a spritesheet json file. Requires Sprite Packer.
This is mainly useful if you edit a texture that is identical between all the languages, such as a button prompts mod. Normally, it's not needed as Sprite Packer already updates the positions.
