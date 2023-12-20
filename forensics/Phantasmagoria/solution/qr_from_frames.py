from PIL import Image
import os

# Directory containing the PNG files
directory = "gif_frame"

even_files = []
odd_files = []

files = sorted(os.listdir(directory), key=lambda x: int(os.path.splitext(x)[0]))
for filename in files:
    if filename.endswith(".png"):
        file_number = int(os.path.splitext(filename)[0])
        if file_number % 2 == 0:
            even_files.append(os.path.join(directory, filename))
        else:
            odd_files.append(os.path.join(directory, filename))

# Function to create a big image from a list of image files
def create_big_image(image_files, output_filename):
    images = [Image.open(img) for img in image_files]

    image_width, image_height = images[0].size

    big_image = Image.new("RGB", (image_width * 10, image_height * 10))

    for i in range(10):
        for j in range(10):
            index = i * 10 + j
            big_image.paste(images[index], (j * image_width, i * image_height))

    big_image.save(output_filename)

create_big_image(even_files, "even_qr.png")
create_big_image(odd_files, "odd_qr.png")