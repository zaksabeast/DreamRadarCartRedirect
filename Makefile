.PHONY: transporter_black transporter_white transporter_black2 transporter_white2 radar_black2 radar_white2 jpn_radar_black2 jpn_radar_white2 clean

all: transporter_black transporter_white transporter_black2 transporter_white2 radar_black2 radar_white2 jpn_radar_black2 jpn_radar_white2

transporter_black:
	@armips transporter.s -strequ SD_SAVE_PATH "/roms/nds/saves/black.sav" -strequ GAME_ID "IRBO"
	@mkdir -p out/transporter
	@flips -c transporter.bin transporter_patched.bin out/transporter/black.ips
	@rm transporter_patched.bin

transporter_white:
	@armips transporter.s -strequ SD_SAVE_PATH "/roms/nds/saves/white.sav" -strequ GAME_ID "IRAO"
	@mkdir -p out/transporter
	@flips -c transporter.bin transporter_patched.bin out/transporter/white.ips
	@rm transporter_patched.bin

transporter_black2:
	@armips transporter.s -strequ SD_SAVE_PATH "/roms/nds/saves/black2.sav" -strequ GAME_ID "IREO"
	@mkdir -p out/transporter
	@flips -c transporter.bin transporter_patched.bin out/transporter/black2.ips
	@rm transporter_patched.bin

transporter_white2:
	@armips transporter.s -strequ SD_SAVE_PATH "/roms/nds/saves/white2.sav" -strequ GAME_ID "IRDO"
	@mkdir -p out/transporter
	@flips -c transporter.bin transporter_patched.bin out/transporter/white2.ips
	@rm transporter_patched.bin

radar_black2:
	@armips radar.s -strequ SD_SAVE_PATH "/roms/nds/saves/black2.sav" -strequ GAME_ID "IREO"
	@mkdir -p out/radar
	@flips -c radar.bin radar_patched.bin out/radar/black2.ips
	@rm radar_patched.bin

radar_white2:
	@armips radar.s -strequ SD_SAVE_PATH "/roms/nds/saves/white2.sav" -strequ GAME_ID "IRDO"
	@mkdir -p out/radar
	@flips -c radar.bin radar_patched.bin out/radar/white2.ips
	@rm radar_patched.bin

jpn_radar_black2:
	@armips jpn_radar.s -strequ SD_SAVE_PATH "/roms/nds/saves/black2.sav" -strequ GAME_ID "IREO"
	@mkdir -p out/jpn_radar
	@flips -c jpn_radar.bin jpn_radar_patched.bin out/jpn_radar/black2.ips
	@rm jpn_radar_patched.bin

jpn_radar_white2:
	@armips jpn_radar.s -strequ SD_SAVE_PATH "/roms/nds/saves/white2.sav" -strequ GAME_ID "IRDO"
	@mkdir -p out/jpn_radar
	@flips -c jpn_radar.bin jpn_radar_patched.bin out/jpn_radar/white2.ips
	@rm jpn_radar_patched.bin

clean:
	@rm -rf *_patched.bin out
