from math import ceil, log

s = "0101110110110100011100011000100111011100110011" #binary coded ciphertext


LENS = len(s) #length of s
print(LENS)
MAXP = ceil(log(LENS)/log(2)) #max power of 2 needed for error checking based on len of s
print(MAXP)

print(" Error checking..")

flipbit = -1 #stores index of the potentially erroneous bit

for p in range(MAXP):
    skip = 2**p
    start = skip - 1
    ones = 0
    for i in range(start, LENS, 2*skip):
        ones += s[i:i+skip].count("1")
    if ones % 2 == 1:
        flipbit = max(flipbit, 0) + skip

if flipbit != -1:
    msg = "Wrong bit at {0}".format(flipbit)
    print(msg)
    s = s[:flipbit-1] + ('1' if s[flipbit-1] == '0' else '0') + s[flipbit:]
    print(s)
else:
    print(" No errors found")

print("Extract data bits")
t = ""
for i, c in enumerate(s):
    if i+1 not in [1, 2, 4, 8, 16, 32]:
        t += c
print("Chop in bytes and convert to chars")
sol = "".join(chr(int(t[i:i+8], 2)) for i in range(0, len(t), 8))
print(sol)
