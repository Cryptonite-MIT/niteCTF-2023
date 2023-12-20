import sys

def hex_to_binary(hex_string):
    try:
        binary_data = bytes.fromhex(hex_string)
        return binary_data
    except ValueError as e:
        print(f"Error: {e}")
        return None

if len(sys.argv) != 2:
    print("Usage: python3 bin.py input_file.txt")
    sys.exit(1)

input_file_path = sys.argv[1]

try:
    with open(input_file_path, 'r') as file:
        hex_string = file.read().strip()
        binary_data = hex_to_binary(hex_string)

    if binary_data:
        output_file_path = "output.bin"
        with open(output_file_path, "wb") as output_file:
            output_file.write(binary_data)

except FileNotFoundError:
    print(f"Error: File '{input_file_path}' not found.")
