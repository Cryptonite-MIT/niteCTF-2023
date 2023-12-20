from PIL import Image

def rgb_to_hex(r, g, b):
    return "{:02x}{:02x}{:02x}".format(r, g, b)

def extract_and_write_rgb(image_path, output_file):
    img = Image.open(image_path)
    width, height = img.size

    with open(output_file, 'w') as file:
        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                hex_color = rgb_to_hex(r, g, b)
                file.write(f"{hex_color}")

    print(f"RGB values written to {output_file}")

input_image_path = 'img.png'
output_file_path = 'output.txt'
extract_and_write_rgb(input_image_path, output_file_path)
