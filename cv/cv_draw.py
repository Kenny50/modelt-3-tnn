import cv2 as cv
import base64
import time
import numpy as np

def draw_current_time(frame):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    cv.putText(frame, current_time, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv.LINE_AA)

def convert_to_base64(file_path):
    with open(file_path, "rb") as file:
        data = file.read()
        return base64.b64encode(data).decode()
    
image_count = 1


# image_path = f"/Users/chang/nodejs/modelt-3-tnn/public/{image_count}.jpg"
image_path = f"/Users/chang/nodejs/modelt-3-tnn/public/image.jpg"
base64_data = convert_to_base64(image_path)


# Decode base64 data to bytes
image_bytes = base64.b64decode(base64_data)

# Convert bytes to numpy array
nparr = np.frombuffer(image_bytes, np.uint8)

# Decode the image array
frame = cv.imdecode(nparr, cv.IMREAD_COLOR)

# Draw current time on the frame
draw_current_time(frame)

# Encode the frame to raw bytes
# Display the frame
cv.imshow('Current Time Prototype', frame)
cv.waitKey(0)
cv.destroyAllWindows()