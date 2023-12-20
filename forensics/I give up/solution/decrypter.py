from scapy.all import *
from itertools import cycle
import os

def xor_binary_strings(binary_str1, binary_str2):
    xor_iterator = cycle(binary_str2)
    result = ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(binary_str1, xor_iterator))
    return result

def binary_string_to_file(binary_str, output_path):
    byte_data = bytes(int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8))
    with open(output_path, 'wb') as file:
        file.write(byte_data)

def extract_images_from_pcap(pcap_file, output_folder, xor_key):
    packets = rdpcap(pcap_file)
    os.makedirs(output_folder, exist_ok=True)

    if Raw in packets[40] and ICMP in packets[40]:
        raw_data = packets[40][Raw].load
        binary_str1 = ''.join(format(byte, '08b') for byte in raw_data)
        result = xor_binary_strings(binary_str1, xor_key)
        output_path = os.path.join(output_folder, f'stegimage.jpg')
        binary_string_to_file(result, output_path)

pcap_file = 'file.pcapng'
xor_key = ''.join(format(ord(char), '08b') for char in "nite{n3v3r_g0nn4_g1ve_u_+he_fl4g!}")
output_folder = 'reformed_images'
extract_images_from_pcap(pcap_file, output_folder, xor_key)
