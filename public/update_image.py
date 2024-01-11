import time
import base64
import fcntl
import os
from PIL import Image, ImageDraw

def convert_to_base64(file_path):
    with open(file_path, "rb") as file:
        data = file.read()
        return base64.b64encode(data).decode()

def write_to_tmp(base64_data, tmp_file):
    with open(tmp_file, "wb") as tmp:
        fcntl.flock(tmp.fileno(), fcntl.LOCK_EX)
        tmp.write(base64.b64decode(base64_data))

def is_valid_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verifies if the file is a valid image
            img.close()
        return True
    except Exception as e:
        print(f"Invalid image: {e}")
        return False
    
image_count = 1

text_color = (0, 0, 0)  # White color for the text

objects_top = "objects_top.jpg"
objects_left = "objects_left.jpg"
objects_right = "objects_right.jpg"

objects_top_tmp = "objects_top_tmp.jpg"
objects_left_tmp = "objects_left_tmp.jpg"
objects_right_tmp = "objects_right_tmp.jpg"
# tmp_file = "tmp.jpg"

while True:
    image_path = f"{image_count}.jpg"
    base64_data = convert_to_base64(image_path)
    img = Image.open(image_path)

    # Get current time
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    draw = ImageDraw.Draw(img)
    draw.text((10, 10), current_time, fill=text_color)

    # Save modified image to temporary file
    tmp_with_time = f"tmp_with_time.jpg"
    img.save(tmp_with_time)
    tmp_with_time_bas64 = convert_to_base64(tmp_with_time)

    # if(not is_valid_image(objects_top) or not is_valid_image(objects_left) or not is_valid_image(objects_right)):
    #    break

    write_to_tmp(tmp_with_time_bas64, objects_top_tmp)
    if(is_valid_image(objects_top_tmp)):
        os.rename(objects_top_tmp, objects_top)

    write_to_tmp(tmp_with_time_bas64, objects_left_tmp)
    if(is_valid_image(objects_left_tmp)):
        os.rename(objects_left_tmp, objects_left)

    write_to_tmp(tmp_with_time_bas64, objects_right_tmp)
    if(is_valid_image(objects_right_tmp)):
        os.rename(objects_right_tmp, objects_right)
    
    # Move to the next image after 66ms
    time.sleep(0.066)
    image_count = (image_count % 50) + 1  # Reset to 1 after reaching 50
