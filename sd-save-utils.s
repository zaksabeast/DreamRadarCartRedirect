readSDSaveFile:
  stmdb sp!, { r0-r5, lr }
  mov r5, r3                                           ; set buffer pointer to r5
  mov r4, r2                                           ; set read size to r4
  mov r3, #0x0                                         ; set offsetHigh as 0 to r3
  mov r2, r1                                           ; set offsetLow to r2
  mov r1, sp                                           ; set r1 to sp to store the file handle
  bl openSDSaveFile
  mov r0, r1                                           ; set r0 to file handle pointer
  stmdb sp!, { r4,r5 }                                 ; push variables
  add r1, sp, #0xc                                     ; set r1 to throwaway location for bytes read
  bl FSFILE_Read                                       ; FSFILE_Read is located at 0x139058
  ldmia sp!, { r4,r5 }                                 ; pop variables
  mov r0, sp                                           ; set r0 to file handle
  bl FSFILE_Close                                      ; FSFILE_Close is located at 0x1390b0
  ldmia sp!, { r0-r5, pc }

writeSDSaveFile:
  stmdb sp!, { r0-r6, lr }
  mov r6, #0x0                                         ; set flags as 0 to r6
  mov r5, r2                                           ; set write size to r5
  mov r4, r3                                           ; set buffer pointer to r4
  mov r3, #0x0                                         ; set offsetHigh as 0 to r3
  mov r2, r1                                           ; set offsetLow to r2
  mov r1, sp                                           ; set r1 to sp to store the file handle
  bl openSDSaveFile
  mov r0, r1                                           ; set r0 to file handle
  stmdb sp!, { r4-r7 }                                 ; push variables
  add r1, sp, #0xc                                     ; set r1 to throwaway location for bytes written
  bl FSFILE_Write
  ldmia sp!, { r4-r7 }                                 ; pop variables
  mov r0, sp                                           ; set r0 to file handle
  bl FSFILE_Close                                      ; FSFILE_Close is located at 0x1390b0
  ldmia sp!, { r0-r6, pc }

checkIfSDSaveFileExists:
  stmdb sp!, { r1, r2, lr }
  stmdb sp!, { r0 }                                    ; push extra stack location to store file handle
  mov r1, sp                                           ; set r1 to sp to store the file handle
  bl openSDSaveFile                                    ; store openSDSaveFile result in r0
  movs r2, r0, lsr #0x1f                               ; get the most significant bit of the result - 0 if success, 1 if error
  eor r2, r2, #0x1                                     ; flip the bit so true if success, false if error
  mov r0, sp                                           ; FIX
  bl FSFILE_Close                                      ; FSFILE_Close is located at 0x1390b0
  ldmia sp!, { r0 }                                    ; pop extra stack location
  mov r0, r2                                           ; set r0 to result
  ldmia sp!, { r1, r2, pc }

openSDSaveFile:
  stmdb sp!, { r2-r11, lr }
  ldr r0, [pc, #0x34]!                                 ; set r0 to fsHandle
  mov r2, #0x0                                         ; always set to 0
  mov r3, #0x9                                         ; set archiveId as ARCHIVE_SDMC
  mov r4, #0x1                                         ; set archivePath.type to PATH_EMPTY
  adr r5, emptyString                                  ; set archivePath.data to empty string location
  mov r6, #0x1                                         ; set archivePath.size to 1 (null terminator)
  mov r7, #0x3                                         ; set filePath.type to PATH_ASCII
  adr r8, saveLocation                                 ; set filePath.data to save string location
  mov r9, #0x1b                                        ; set filePath.size to the size of the save location string
  mov r10, #0x3                                        ; set openFlags to OPEN_READ|OPEN_WRITE
  mov r11, #0x0                                        ; set attributes to 0
  stmdb sp!, { r4-r11 }                                ; push variables
  bl FSUSER_OpenFileDirectly
  ldmia sp!, { r4-r11 }                                ; pop variables
  ldmia sp!, { r2-r11, pc }

fsHandle:
  .word 0x1dba80

emptyString:
  .string ""

saveLocation:
  .string "/roms/nds/saves/white2.sav"