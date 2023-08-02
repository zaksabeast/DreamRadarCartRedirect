# Dream Radar Cart Redirect

This patch now supports Pokémon Transporter!

Dream Radar is a game which allows getting level 5 legendary Pokémon in dream balls with hidden abilities, and sending them to a Black 2 or White 2 NDS cartridge. Pokémon Transporter allows transferring Pokémon from previous games to newer games.

This patch redirects saving from an NDS cartridge to a file on the SD card. Using this patch allows dream radar and transporter to use saves from [TWiLightMenu](https://github.com/DS-Homebrew/TWiLightMenu) and [nds-bootstrap](https://github.com/ahezard/nds-bootstrap).

## Usage

This requires having [Luma3DS](https://github.com/AuroraWright/Luma3DS) on your 3DS.

1. Download and unzip the zip file from the latest releases
   - The zip will have two folders in it: `radar` and `transporter`
   - Each folder will have patches for each supported game
2. Copy the IPS patch you want to your SD card
   - Pokémon Transporter: `/luma/titles/00040000000C9C00/code.ips`
   - Japanese Pokémon Dream Radar: `/luma/titles/0004000000073200/code.ips`
   - All Regions Pokémon Dream Radar: `/luma/titles/00040000000AE100/code.ips`
3. Ensure you have a save file at `/roms/nds/saves/white2.sav`, `/roms/nds/saves/black2.sav`, `/roms/nds/saves/black.sav`, or `/roms/nds/saves/white.sav`
   - If you're using [TWiLightMenu](https://github.com/DS-Homebrew/TWiLightMenu), this means having a game at `/roms/nds/white2.nds`, `/roms/nds/black2.nds`, `/roms/nds/black.nds`, or `/roms/nds/white.nds`
   - Note: Black and White are only supported by Transporter
4. Ensure that game patching is enabled
   - You can enable it in the Luma3DS configuration menu by holding the Select button before starting the console.

## Building the patches for custom save paths

### Requirements

- [ ] The `.code` file of the Dream Radar or Pokémon Transporter application (see [below](#dump) how to dump it)
- [ ] A copy of this repository (or at least of the respective `.s` file of the title you want to modify)
- [ ] A copy of [armips](https://github.com/Kingcom/armips)
- [ ] A copy of [flips (Floating IPS)](https://github.com/Alcaro/Flips)

<details>
   <summary>
   <h3>
      <a name="dump">Dumping the <code>.code</code></a>
   </h3>
   </summary>

#### Requirements

- [ ] The respective title (Dream Radar or Transporter) installed on your 3DS
- [ ] [GodMode9](https://github.com/d0k3/GodMode9) on your 3DS (should be installed if you followed [this guide](https://3ds.hacks.guide/))

<h4>Dumping</h4>

1. Boot into GodMode9 (if you followed the aforementioned guide, hold start while booting)
2. Open the title manager:

   - Navigate to `[Y:] TITLE MANAGER` and press <kbd>A</kbd>
   <br>or<br>
   - Navigate to `[A:] SYSNAND SD` and press <kbd>R + A</kbd> for drive options and select `Open title manager` on the bottom screen by using the D-pad and then press <kbd>A</kbd>
3. Find the entry of the title you want to dump and press <kbd>A</kbd>, it should have the same folder name as above:

   - Pokémon Transporter: `00040000000C9C00`
   - Japanese Pokémon Dream Radar: `0004000000073200`
   - All Regions Pokémon Dream Radar: `00040000000AE100`

4. Select `Open title folder` and press <kbd>A</kbd>
5. Select the `.tmd` file and press <kbd>A</kbd>
6. Select `TMD file options...` and press <kbd>A</kbd>
7. Select `Mount CXI/NDS to drive` and press <kbd>A</kbd>
8. Press <kbd>A</kbd> to enter the mount point
9. Select the `exefs` folder and press <kbd>A</kbd>
10. Select the `.code` file and press <kbd>A</kbd>
11. Select `Copy to 0:/gm9/out` and press <kbd>A</kbd>
12. Press <kbd>A</kbd> to continue

Success! The dumped `.code` is now stored on your SD card at `SD:/gm9/out`. Copy this file over to the repository folder on your computer using your preferred method, e.g. with [FTPD](https://github.com/mtheall/ftpd) or by plugging in your SD into your computer. Remember that on Unix and Unix-like environments files with filenames starting with a `.` are treated as hidden files, so make sure your preferred file browser shows them when trying to transfer the file.
</details>

### Building the patches yourself

<details>
   <summary>
   <h3>
      Dream Radar (All regions)
   </h3>
   </summary>

   1. Rename your obtained `.code` file to `radar.bin`
   2. Open a shell in the folder containing your recently renamed `.bin`and the rest of the above resources. If you are using installed versions of the aforementioned tools, omit the preceding `./`. __Windows users__: replace all the binary names in the following with `.\$NAME.exe`, so `./armips` becomes `.\armips.exe` etc.
   3. Execute the following command, replacing `$GAME_ID` with the ID of your game (check [the table](#version-table)) and `$SAVE_PATH` with the location of your save file on your SD card, so if using TWiLightMenu with a Pokémon Black 2 ROM stored at `/roms/nds/black2.nds`, use `IREO` and `/roms/nds/saves/black2.sav`.

      ```shell
      ./armips radar.s -strequ SD_SAVE_PATH "$SAVE_PATH" -strequ GAME_ID "$GAME_ID"
      ```

   4. Execute

      ```shell
      ./flips -c radar.bin radar_patched.bin code.ips
      ```

   Congratulations! You now have an IPS patch for your save path and game. It is safe to delete the `radar_patched.bin`, since it is specific to the save path and game. Follow the instructions above under [Usage](#usage) to continue, keeping in mind that your save path will differ.
</details>

<details>
   <summary>
   <h3>
      Dream Radar (Japan)
   </h3>
   </summary>

   1. Rename your obtained `.code` file to `radar.bin`
   2. Open a shell in the folder containing your recently renamed `.bin`and the rest of the above resources. If you are using installed versions of the aforementioned tools, omit the preceding `./`. __Windows users__: replace all the binary names in the following with `.\$NAME.exe`, so `./armips` becomes `.\armips.exe` etc.
   3. Execute the following command, replacing `$GAME_ID` with the ID of your game (check [the table](#version-table)) and `$SAVE_PATH` with the location of your save file on your SD card, so if using TWiLightMenu with a Pokémon Black 2 ROM stored at `/roms/nds/black2.nds`, use `IREO` and `/roms/nds/saves/black2.sav`.

      ```shell
      ./armips jpn_radar.s -strequ SD_SAVE_PATH "$SAVE_PATH" -strequ GAME_ID "$GAME_ID"
      ```

   4. Execute

      ```shell
      ./flips -c jpn_radar.bin jpn_radar_patched.bin code.ips
      ```

   Congratulations! You now have an IPS patch for your save path and game. It is safe to delete the `jpn_radar_patched.bin`, since it is specific to the save path and game. Follow the instructions above under [Usage](#usage) to continue, keeping in mind that your save path will differ.
</details>

<details>
   <summary>
   <h3>
      Transporter
   </h3>
   </summary>

   1. Rename your obtained `.code` file to `transporter.bin`
   2. Open a shell in the folder containing your recently renamed `.bin`and the rest of the above resources. If you are using installed versions of the aforementioned tools, omit the preceding `./`. __Windows users__: replace all the binary names in the following with `.\$NAME.exe`, so `./armips` becomes `.\armips.exe` etc.
   3. Execute the following command, replacing `$GAME_ID` with the ID of your game (check [the table](#version-table)) and `$SAVE_PATH` with the location of your save file on your SD card, so if using TWiLightMenu with a Pokémon Black 2 ROM stored at `/roms/nds/black2.nds`, use `IREO` and `/roms/nds/saves/black2.sav`.

      ```shell
      ./armips transporter.s -strequ SD_SAVE_PATH "$SAVE_PATH" -strequ GAME_ID "$GAME_ID"
      ```

   4. Execute

      ```shell
      ./flips -c transporter.bin transporter_patched.bin code.ips
      ```

   Congratulations! You now have an IPS patch for your save path and game. It is safe to delete the `transporter_patched.bin`, since it is specific to the save path and game. Follow the instructions above under [Usage](#usage) to continue, keeping in mind that your save path will differ.
</details>

### Version table

   | Game     | ID    |
   |   ----   |  ---  |
   | Black    | IRBO  |
   | Black 2  | IREO  |
   | White    | IRAO  |
   | White 2  | IRDO  |
