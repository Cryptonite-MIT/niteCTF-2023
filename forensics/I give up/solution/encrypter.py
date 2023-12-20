from scapy.all import *
from itertools import cycle

def image_to_bits(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    bits_list = [format(byte, '08b') for byte in image_data]
    bits_string = ''.join(bits_list)
    return bits_string

def xor_binary_strings(binary_str1, binary_str2):
    xor_iterator = cycle(binary_str2)
    result = ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(binary_str1, xor_iterator))
    return result

output_filename = 'file.pcapng'
source_ip = '192.168.1.1'
destination_ip = '192.168.1.2'
xored_packets = []

def bitstostring(b):
    return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(b)]*8))
binary_str2 = ''.join(format(ord(char), '08b') for char in "nite{n3v3r_g0nn4_g1ve_u_+he_fl4g!}")

for i in range(1, 191):
    image_path = f'source/{i}.jpg'
    image_bits = image_to_bits(image_path)
    result = xor_binary_strings(image_bits, binary_str2)
    xor_image_data = bytes(int(result[i:i+8], 2) for i in range(0, len(result), 8))
    packet = IP(src=source_ip, dst=destination_ip) / ICMP() / Raw(load=xor_image_data)
    xored_packets.append(packet)

with PcapWriter(output_filename, append=True, sync=True) as pcap_writer:
    for packet in xored_packets:
        pcap_writer.write(packet)
