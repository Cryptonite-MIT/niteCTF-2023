from PIL import Image

def extract_frames(gif_path, output_folder):
    # Open the GIF
    with Image.open(gif_path) as img:
        # Iterate through each frame
        for frame in range(img.n_frames):
            img.seek(frame)
            # Save each frame as a new image
            img.save(f"{output_folder}/{frame+1}.png")

# Specify the path to your GIF file
gif_path = "chal.gif"

# Specify the folder where you want to save the extracted frames
output_folder = "gif_frame"

# Call the function to extract frames
extract_frames(gif_path, output_folder)
