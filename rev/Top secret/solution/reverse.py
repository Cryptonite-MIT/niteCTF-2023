from PIL import Image

def binaryToChar(binary):
    decimal = int(binary, 2)
    return chr(decimal)

def reverseBitsExtraction(input_image, output_string):
    image = Image.open(input_image)
    width, height = image.size

    extracted_bits = ""

    for i in range(height):
        binary_byte = ""
        for j in range(8):
            pixel = image.getpixel((j+i%8, i))
            # Extract the LSB of the blue channel
            bit = pixel[i%3] & 1
            binary_byte += str(bit)

        extracted_bits += binary_byte

    with open(output_string, "w") as output_file:
        for i in range(0, len(extracted_bits), 8):
            binary_char = extracted_bits[i:i+8]
            char = binaryToChar(binary_char)
            output_file.write(char)

if __name__ == "__main__":
    input_image = "output.png"  # Use the image with embedded bits
    output_string = "reversed_output.txt"

    reverseBitsExtraction(input_image, output_string)

    print("Bits extracted and reversed successfully!")
