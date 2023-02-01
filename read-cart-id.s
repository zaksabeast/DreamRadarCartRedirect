read_cart_id:
  stmdb sp!, { r2, lr }
  ldr r2, [cart_id]
  str r2, [r0, #0x0]
  mov r0, #0
  ldmia sp!, { r2, pc }

  cart_id:
    .ascii GAME_ID
