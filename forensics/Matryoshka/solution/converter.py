import base64

def main():
    with open("matryoshka.txt", "r") as file:
        base64_text = file.readline().strip()
    decoded_base64 = base64.b64decode(base64_text).decode('utf-8')
    hex_text = decoded_base64.replace(" ", "")
    decoded_hex = bytes.fromhex(hex_text).decode('utf-8')
    decoded_ascii = ''.join(chr(int(char)) for char in decoded_hex.split())
    with open("hexstream.txt", "w") as output_file:
        output_file.write(decoded_ascii)

if __name__ == "__main__":
    main()
