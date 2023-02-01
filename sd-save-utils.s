read_save_from_sd:
  stmdb sp!, { r0-r5, lr }
  mov r5, r3                       ; set buffer pointer to r5
  mov r4, r2                       ; set read size to r4
  mov r3, #0x0                     ; set offsetHigh as 0 to r3
  mov r2, r1                       ; set offsetLow to r2
  mov r1, sp                       ; set r1 to sp to store the file handle
  bl open_sd_save
  mov r0, r1                       ; set r0 to file handle pointer
  stmdb sp!, { r4, r5 }            ; push variables
  mov r1, sp                       ; set r1 to throwaway location for bytes read
  bl FSFILE_ReadFile               ; FSFILE_Read is located at 0x139058
  ldmia sp!, { r4, r5 }            ; pop variables
  mov r0, sp                       ; set r0 to file handle
  bl FSFILE_Close                  ; FSFILE_Close is located at 0x1390b0
  ldmia sp!, { r0-r5, pc }

write_save_to_sd:
  stmdb sp!, { r0-r6, lr }
  mov r6, #0x0                     ; set flags as 0 to r6
  mov r5, r2                       ; set write size to r5
  mov r4, r3                       ; set buffer pointer to r4
  mov r3, #0x0                     ; set offsetHigh as 0 to r3
  mov r2, r1                       ; set offsetLow to r2
  mov r1, sp                       ; set r1 to sp to store the file handle
  bl open_sd_save
  mov r0, r1                       ; set r0 to file handle
  stmdb sp!, { r4-r6 }             ; push variables
  mov r1, sp                       ; set r1 to throwaway location for bytes written
  bl FSFILE_WriteFile
  ldmia sp!, { r4-r6 }             ; pop variables
  mov r0, sp                       ; set r0 to file handle
  bl FSFILE_Close                  ; FSFILE_Close is located at 0x1390b0
  ldmia sp!, { r0-r6, pc }

open_sd_save:
  stmdb sp!, { r2-r11, lr }
  ldr r0, [fs_handle_ptr]          ; set r0 to fsHandle
  mov r2, #0x0                     ; always set to 0
  mov r3, #0x9                     ; set archiveId as ARCHIVE_SDMC
  mov r4, #0x1                     ; set archivePath.type to PATH_EMPTY
  adr r5, empty_string             ; set archivePath.data to empty string location
  mov r6, #0x1                     ; set archivePath.size to 1 (null terminator)
  mov r7, #0x3                     ; set filePath.type to PATH_ASCII
  adr r8, save_path                ; set filePath.data to save string location
  mov r9, #strlen(SD_SAVE_PATH)+1  ; set filePath.size to the size of the save location string
  mov r10, #0x3                    ; set openFlags to OPEN_READ|OPEN_WRITE
  mov r11, #0x0                    ; set attributes to 0
  stmdb sp!, { r4-r11 }            ; push variables
  bl FSUSER_OpenFileDirectly
  ldmia sp!, { r4-r11 }            ; pop variables
  ldmia sp!, { r2-r11, pc }

fs_handle_ptr:
  .word fs_handle

empty_string:
  .word 0x0

save_path:
  .asciiz SD_SAVE_PATH
