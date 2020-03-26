#!/usr/bin/env python3

import argparse
import collections
import operator
import sys

from typing import Dict

# Various constants for dealing with IPS files
PATCH_BYTEORDER = 'big'
PATCH_HEADER = b'PATCH'
PATCH_EOF = b'EOF'

# Both pokear and salmon use the same code offset; from the cxis with ctrtool
CODE_OFFSET = 0x100000
CODE_BYTEORDER = 'little'

# Offset from the start of card_id function to where we skip from
CARD_ID_SKIP_OFFSET = 0x34
# Offset from the start of the card_id frunciton to where we fake the id
CARD_ID_FAKE_OFFSET = 0x10c

# Offsets from the end of the binary at which to install the SD functions
# These values are based on the pre-built poke radar patch
SD_FUNCTION_OFFSET = 0x310
OPEN_FUNCTION_OFFSET = 0x3c8

class Config(collections.namedtuple('AbstractConfig', (
    'code_size', 'check_card', 'card_id', 'read_save', 'write_save',
    'fs_handle', 'fs_open', 'fs_read', 'fs_write', 'fs_close'))):
  """Configuration for the Pokemon binary.

  Attributes:
    code_size: The size of the code .text section; obtained from cxi with
      ctrtool.
    check_card: The address of the function that checks if a card is inserted,
      or none if the binary doesn't explicitly check for a card;
      indirectly calls FSUSER_CardSlotIsInserted.
    card_id: The address of the function that gets the card id;
      indirectly calls FSUSER_GetLegacyRomHeader2.
    read_save: The address of the function that reads the save data;
      see TWLSaveTool SPIReadSaveData.
    write_save: The address of the function that writes the save data;
      see TWLSaveTool SPIWriteSaveData.
    fs_handle: The address of the handle to the fs:USER process.
    fs_open: The address of FSUSER_OpenFileDirectly.
    fs_read: The address of FSFILE_Read.
    fs_write: The address of FSFILE_Write.
    fs_close: The address of FSFILE_Close.
  """

# Config for Dream Radar
POKEAR_CONFIG = Config(
  code_size  = 0x0bebb4,
  # limit    = 0x0bf000
  check_card = 0x137da4,
  card_id    = 0x13dcf4,
  read_save  = 0x13dac8,
  write_save = 0x188788,
  fs_handle  = 0x1dba80,
  fs_open    = 0x124ea8,
  fs_read    = 0x139058,
  fs_write   = 0x1390dc,
  fs_close   = 0x1390b0,
)

CONFIGS = collections.OrderedDict(
  pokear=POKEAR_CONFIG,
)


def PadASMString(string: bytes) -> bytes:
  padding_size = 4 - len(string) % 4
  return string + b'\0' * padding_size


def ASM_Branch(link: bool, addr: int, label: int) -> bytes:
  pc = addr + 8
  return b''.join((
    (label - pc >> 2).to_bytes(3, byteorder=CODE_BYTEORDER, signed=True),
    b'\xeb' if link else b'\xea',  # `blal` if link else `bal`
  ))


def ASM_FakeCardId(card_id: str) -> bytes:
  id_bytes = card_id.encode('ascii')
  assert len(id_bytes) == 4
  return b''.join((
    id_bytes[0:1] + b'\x00\xa0\xe3',  # mov  r0, <id_bytes[0]>
    b'\x00'       + b'\x00\xc6\xe5',  # strb r0, [r6,#0]
    id_bytes[1:2] + b'\x00\xa0\xe3',  # mov  r0, <id_bytes[1]>
    b'\x01'       + b'\x00\xc6\xe5',  # strb r0, [r6,#1]
    id_bytes[2:3] + b'\x00\xa0\xe3',  # mov  r0, <id_bytes[2]>
    b'\x02'       + b'\x00\xc6\xe5',  # strb r0, [r6,#2]
    id_bytes[3:4] + b'\x00\xa0\xe3',  # mov  r0, <id_bytes[3]>
    b'\x03'       + b'\x00\xc6\xe5',  # strb r0, [r6,#3]
  ))


def ASM_ReadSDSaveFile(config: Config, addr: int, open_addr: int) -> bytes:
  return b''.join((
    b'\x3f\x40\x2d\xe9',  # stmdb sp!, { r0-r5, lr }
    b'\x03\x50\xa0\xe1',  # mov   r5, r3          ; set buffer pointer to r5
    b'\x02\x40\xa0\xe1',  # mov   r4, r2          ; set read size to r4
    b'\x00\x30\xa0\xe3',  # mov   r3, #0x0        ; set offsetHigh as 0 to r3
    b'\x01\x20\xa0\xe1',  # mov   r2, r1          ; set offsetLow to r2
    b'\x0d\x10\xa0\xe1',  # mov   r1, sp          ; set r1 to sp to store file handle
    ASM_Branch(True, addr + 24, open_addr),       # bl OpenSDSaveFile
    b'\x01\x00\xa0\xe1',  # mov   r0, r1          ; set r0 to file handle
    b'\x30\x00\x2d\xe9',  # stmdb sp!, { r4,r5 }  ; push variables
    b'\x0c\x10\x8d\xe2',  # add   r1, sp, #0xc    ; set r1 to throwaway location for bytes read
    ASM_Branch(True, addr + 40, config.fs_read),  # bl FSFILE_Read
    b'\x30\x00\xbd\xe8',  # ldmia sp!, { r4,r5 }  ; pop variables
    b'\x0d\x00\xa0\xe1',  # mov   r0, sp          ; set r0 to file handle
    ASM_Branch(True, addr + 52, config.fs_close), # bl FSFILE_Close
    b'\x3f\x80\xbd\xe8',  # ldmia sp!, { r0-r5, pc }
    b'\x00\x00\x00\x00',  # nop
  ))


def ASM_WriteSDSaveFile(config: Config, addr: int, open_addr: int) -> bytes:
  return b''.join((
    b'\x7f\x40\x2d\xe9',  # stmdb sp!, { r0-r6, lr }
    b'\x00\x60\xa0\xe3',  # mov   r6, #0x0        ; set flags 0 to r6
    b'\x02\x50\xa0\xe1',  # mov   r5, r2          ; set write size to r5
    b'\x03\x40\xa0\xe1',  # mov   r4, r3          ; set buffer pointer to r4
    b'\x00\x30\xa0\xe3',  # mov   r3, #0x0        ; set offsetHigh as 0 to r3
    b'\x01\x20\xa0\xe1',  # mov   r2, r1          ; set offsetLow to r2
    b'\x0d\x10\xa0\xe1',  # mov   r1, sp          ; set r1 to sp to store file handle
    ASM_Branch(True, addr + 28, open_addr),       # bl OpenSDSaveFile
    b'\x01\x00\xa0\xe1',  # mov   r0, r1          ; set r0 to file handle
    b'\xf0\x00\x2d\xe9',  # stmdb sp!, { r4-r7 }  ; push variables
    b'\x0c\x10\x8d\xe2',  # add   r1, sp, #0xc    ; set r1 to throwaway location for bytes written
    ASM_Branch(True, addr + 44, config.fs_write), # bl FSFILE_Write
    b'\xf0\x00\xbd\xe8',  # ldmia sp!, { r4-r7 }  ; pop variables
    b'\x0d\x00\xa0\xe1',  # mov   r0, sp          ; set r0 to file handle
    ASM_Branch(True, addr + 56, config.fs_close), # bl FSFILE_Close
    b'\x7f\x80\xbd\xe8',  # ldmia sp!, { r0-r6, pc }
    b'\x00\x00\x00\x00',  # nop
  ))


def ASM_CheckSDSaveFile(config: Config, addr: int, open_addr: int) -> bytes:
  return b''.join((
    b"\x06\x40\x2d\xe9",  # stmdb sp!, { r1, r2, lr }
    b"\x01\x00\x2d\xe9",  # stmdb sp!, { r0 }       ; push extra stack location for file handle
    b"\x0d\x10\xa0\xe1",  # mov   r1, sp            ; set r1 to sp to store file handle
    ASM_Branch(True, addr + 12, open_addr),         # bl OpenSDSaveFile
    b"\xa0\x2f\xb0\xe1",  # movs  r2, r0, lsr #0x1f ; get the most significant bit of the result
    b"\x01\x20\x22\xe2",  # eor   r2, r2, #0x1      ; flip the bit so true if success
    b"\x0d\x00\xa0\xe1",  # mov   r0, sp            ; set r0 to file handle
    ASM_Branch(True, addr + 28, config.fs_close),   # bl FSFILE_Close
    b"\x01\x00\xbd\xe8",  # ldmia sp!, { r0 }       ; pop extra stack location
    b"\x02\x00\xa0\xe1",  # mov   r0, r2            ; set r0 to result
    b"\x06\x80\xbd\xe8",  # ldmia sp!, { r1, r2, pc }
    b'\x00\x00\x00\x00',  # nop
  ))


def ASM_OpenSDSaveFile(config: Config, addr: int, save_path: str) -> bytes:
  path_bytes = save_path.encode('ascii')
  size = len(path_bytes) + 1
  assert 0 < size < 0x100
  return b''.join((
    b'\xfc\x4f\x2d\xe9',  # stmdb sp!, { r2-r11, lr }
    b'\x34\x00\xbf\xe5',  # ldr   r0, [pc, #0x34]! ; set r0 to fsHandle
    b'\x00\x20\xa0\xe3',  # mov   r2, #0x0         ; always set to 0
    b'\x09\x30\xa0\xe3',  # mov   r3, #0x9         ; set archiveId to ARCHIVE_SDMC
    b'\x01\x40\xa0\xe3',  # mov   r4, #0x1         ; set archivePath.type to PATH_EMPTY
    b'\x28\x50\x8f\xe2',  # adr   r5, emptyString  ; set archivePath.data to emptyString
    b'\x01\x60\xa0\xe3',  # mov   r6, #0x1         ; set archivePath.size to 1 (null terminator)
    b'\x03\x70\xa0\xe3',  # mov   r7, #0x3         ; set filePath.type to PATH_ASCII
    b'\x20\x80\x8f\xe2',  # adr   r8, savePath     ; set filePath.data to savePath
    size.to_bytes(1, byteorder=CODE_BYTEORDER) +
        b'\x90\xa0\xe3',  # mov   r9, <size>       ; set filePath.size to the size of savePath
    b'\x03\xa0\xa0\xe3',  # mov   r10, #0x3        ; set openFlags to OPEN_READ|OPEN_WRITE
    b'\x00\xb0\xa0\xe3',  # mov   r11, #0x0        ; set attributes to 0
    b'\xf0\x0f\x2d\xe9',  # stmdb sp!, { r4-r11 }  ; push variables
    ASM_Branch(True, addr + 52, config.fs_open),   # bl FSUSER_OpenFileDirectly
    b'\xf0\x0f\xbd\xe8',  # ldmia sp!, { r4-r11 }  ; pop variables
    b'\xfc\x8f\xbd\xe8',  # ldmia sp!, { r2-r11, pc }

    # fsHandle: .word <config.fs_handle>
    config.fs_handle.to_bytes(4, byteorder=CODE_BYTEORDER),

    # emptyString: .string ""
    PadASMString(b''),

    # savePath: .string <path_bytes>
    PadASMString(path_bytes),
  ))


def CreatePatchRecords(config: Config, card_id: str, save_path: str) -> Dict[int, bytes]:
  records = {}
  sd_asm = b''
  sd_addr = CODE_OFFSET + config.code_size + SD_FUNCTION_OFFSET

  # Add OpenSDSaveFile function
  open_addr = CODE_OFFSET + config.code_size + OPEN_FUNCTION_OFFSET
  records[open_addr] = ASM_OpenSDSaveFile(config, open_addr, save_path)

  # Redirect save read
  read_addr = sd_addr + len(sd_asm)
  sd_asm += ASM_ReadSDSaveFile(config, read_addr, open_addr)
  records[config.read_save] = ASM_Branch(False, config.read_save, read_addr)

  # Redirect save write
  write_addr = sd_addr + len(sd_asm)
  sd_asm += ASM_WriteSDSaveFile(config, write_addr, open_addr)
  records[config.write_save] = ASM_Branch(False, config.write_save, write_addr)

  # Redirect card check if needed
  if config.check_card is not None:
    check_addr = sd_addr + len(sd_asm)
    sd_asm += ASM_CheckSDSaveFile(config, check_addr, open_addr)
    records[config.check_card] = ASM_Branch(False, config.check_card, check_addr)
  
  # Add SD Functions
  records[sd_addr] = sd_asm
  
  # Patch the function that reads the card id
  skip_addr = config.card_id + CARD_ID_SKIP_OFFSET
  fake_addr = config.card_id + CARD_ID_FAKE_OFFSET
  records[skip_addr] = ASM_Branch(False, skip_addr, fake_addr)
  records[fake_addr] = ASM_FakeCardId(card_id)

  return records


def CreatePatch(config: Config, card_id: str, save_path: str) -> bytes:
  patch = [PATCH_HEADER]
  for offset, data in sorted(
      CreatePatchRecords(config, card_id, save_path).items(),
      key=operator.itemgetter(0)):
    patch.append((offset - CODE_OFFSET).to_bytes(3, byteorder=PATCH_BYTEORDER))
    patch.append(len(data).to_bytes(2, byteorder=PATCH_BYTEORDER))
    patch.append(data)
  patch.append(PATCH_EOF)
  return b''.join(patch)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      description='Create an IPS patch to redirect card access to a file on SD')
  parser.add_argument(
      'config', choices=CONFIGS.keys(), help='which binary configuration to use')
  parser.add_argument('card_id', help='the 4 character id of the card')
  parser.add_argument('save_path', help='the path to the save file on the SD card')
  args = parser.parse_args()
  sys.stdout.buffer.write(CreatePatch(CONFIGS[args.config], args.card_id, args.save_path))

