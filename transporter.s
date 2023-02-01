.3ds
.open "transporter.bin", "transporter_patched.bin", 0x100000

fs_handle equ 0x311f80
FSUSER_OpenFileDirectly equ 0x1df448
FSFILE_ReadFile equ 0x15930c
FSFILE_WriteFile equ 0x159390
FSFILE_Close equ 0x159364

.org 0x21a7e0
read_save:
  b read_save_from_sd

.org 0x21aa0c
.include "read-cart-id.s"

.org 0x21ab50
write_save:
  stmdb sp!, { r2, r3, lr }
  eor r2, r2, r3              ; swap r2 and r3
  eor r3, r2, r3
  eor r2, r2, r3
  bl write_save_to_sd
  ldmia sp!, { r2, r3, pc }

.org 0x28dd00
.include "sd-save-utils.s"

.close
