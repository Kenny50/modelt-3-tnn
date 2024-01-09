from PIL import Image

def is_valid_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verifies if the file is a valid image
        return True
    except Exception as e:
        print(f"Invalid image: {e}")
        return False
    
print(is_valid_image("tmp.png"))