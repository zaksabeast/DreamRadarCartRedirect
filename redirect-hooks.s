checkIfCartIsInserted:                                ; patch to redirect to checkIfSDSaveFileExists - located at 0x137da4
  b checkIfSDSaveFileExists

readTWLSaveData:                                      ; patch to redirect to readSDSaveFile - located at 0x13dac8
  b readSDSaveFile

readCartId:                                           ; patch to set cart Id for app as IRDO (white 2 ID) - located at 0x13dcf4
  b LAB_0013de00                                      ; skip checks - located at 0x13dd28
  mov result,#0x49                                    ; ascii I - located at 0x13de00
  mov result,#0x52                                    ; ascii R - located at 0x13de08
  mov result,#0x44                                    ; ascii D - located at 0x13de10
  mov result,#0x4f                                    ; ascii O - located at 0x13de18

writeTWLSaveData:                                     ; patch to redirect to readSDSaveFile - located at 0x188788
  b writeSDSaveFile
