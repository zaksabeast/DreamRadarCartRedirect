# Dream Radar Cart Redirect

This patch now supports Pokemon Transporter!

Dream Radar is a game which allows getting level 5 legendary Pokemon in dream balls with hidden abilities, and sending them to a Black 2 or White 2 NDS cartridge. Pokemon Transporter allows transferring Pokemon from previous games to newer games.

This patch redirects saving from an NDS cartridge to a file on the SD card. Using this patch allows dream radar and transporter to use saves from [TWiLightMenu](https://github.com/DS-Homebrew/TWiLightMenu) and [nds-bootstrap](https://github.com/ahezard/nds-bootstrap).

## Usage

This requires having [Luma3DS](https://github.com/AuroraWright/Luma3DS) on your 3DS.

1. Download and unzip the zip file from the latest releases
   - The zip will have two folders in it: `radar` and `transporter`
   - Each folder will have patches for each supported game
2. Copy the ips patch you want to your sd card
   - Pokemon Transporter: `/luma/titles/00040000000C9C00/code.ips`
   - Japanese Pokemon Dream Radar: `/luma/titles/0004000000073200/code.ips`
   - All Regions Pokemon Dream Radar: `/luma/titles/00040000000AE100/code.ips`
3. Ensure you have a save file at `/roms/nds/saves/white2.sav`, `/roms/nds/saves/black2.sav`, `/roms/nds/saves/black.sav`, or `/roms/nds/saves/white.sav`
   - If you're using [TWiLightMenu](https://github.com/DS-Homebrew/TWiLightMenu), this means having a game at `/roms/nds/white2.nds`, `/roms/nds/black2.nds`, `/roms/nds/black.nds`, or `/roms/nds/white.nds`
   - Note: Black and White are only supported by Transporter
4. Ensure that game patching is enabled
   - You can enable it in the Luma3DS configuration menu by holding the Select button before starting the console.

## Building the patches for custom save paths

If you want a different game Id or save path, run these commands (replace `SD_SAVE_PATH` and `GAME_ID`):

```
armips transporter.s -strequ SD_SAVE_PATH "/roms/nds/saves/black.sav" -strequ GAME_ID "IRBO"
flips -c code.bin code_patched.bin code.ips
```
