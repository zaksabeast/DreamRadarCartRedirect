# Dream Radar Cart Redirect

Dream Radar is a game which allows getting level 5 legendary Pokemon in dream balls with hidden abilities, and sending them to a Black 2 or White 2 NDS cartridge.

This patch redirects saving from an NDS cartridge to a file on the SD card.  Using this patch allows dream radar to use saves from [TWiLightMenu](https://github.com/DS-Homebrew/TWiLightMenu) and [nds-bootstrap](https://github.com/ahezard/nds-bootstrap).

## Usage

This requires having [Luma3DS](https://github.com/AuroraWright/Luma3DS) on your 3DS.

1. Download and unzip the zip file from the latest releases
   - This will have two ips patches in it - `black2.ips` and `white2.ips`
2. Copy the patch you want to `/luma/titles/00040000000AE100/code.ips`
3. Ensure you have a save file at `/roms/nds/saves/white2.sav` or `/roms/nds/saves/black2.sav`
   - If you're using [TWiLightMenu](https://github.com/DS-Homebrew/TWiLightMenu), this means having a game at `/roms/nds/white2.nds` or `/roms/nds/black2.nds`

## Converting from White 2 to Black 2

1. Update the save file location at `saveLocation`
2. Update `readCartId` to store a Black 2 Id, such as IREO
3. Build the patches

## Updating the save location

1. Update the save file location at `saveLocation`
2. Update the save file location string size in `openSDSaveFile`
3. Build the patches

## Building

Hand assemble the patches to build them.
