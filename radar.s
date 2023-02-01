.3ds
.open "radar.bin", "radar_patched.bin", 0x100000

fs_handle equ 0x1dba80
FSUSER_OpenFileDirectly equ 0x124ea8
FSFILE_ReadFile equ 0x139058
FSFILE_WriteFile equ 0x1390dc
FSFILE_Close equ 0x1390b0

.org 0x137da4
check_if_cart_is_inserted:
  b check_if_save_exists

.org 0x13dac8
read_save:
  b read_save_from_sd

.org 0x13dcf4
.include "read-cart-id.s"

.org 0x188788
write_save:
  b write_save_to_sd

.org 0x1beec4
.include "sd-save-utils.s"

.align 4
check_if_save_exists:
  stmdb sp!, { r1, r2, lr }
  stmdb sp!, { r0 }           ; push extra stack location to store file handle
  mov r1, sp                  ; set r1 to sp to store the file handle
  bl open_sd_save             ; store openSDSaveFile result in r0
  movs r2, r0, lsr #0x1f      ; get the most significant bit of the result - 0 if success, 1 if error
  eor r2, r2, #0x1            ; flip the bit so true if success, false if error
  mov r0, sp
  bl FSFILE_Close             ; FSFILE_Close is located at 0x1390b0
  ldmia sp!, { r0 }           ; pop extra stack location
  mov r0, r2                  ; set r0 to result
  ldmia sp!, { r1, r2, pc }

.close
