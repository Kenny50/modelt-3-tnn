import cv2 as cv
import subprocess
import time
import numpy as np
import redis
import base64
import atexit
import json
import random
import os

rtmp_url = os.environ.get('rtmp_url')
# rtmp_url = 'rtmp://127.0.0.1:1935/live/cv-top'

colors = {
    'Car': (0, 255, 0),             # Green
    'Bus': (0, 255, 255),           # Yellow
    'Truck': (255, 0, 0),           # Blue
    'Heavy_truck': (255, 192, 203),  # Pink
    'Motorcyclist': (135, 206, 250), # Sky Blue
    'Cyclist': (255, 165, 0),       # Orange
    'Wheelchair': (255, 69, 0),      # Red-Orange
    'Pedestrian': (255, 140, 105)    # Salmon
}

img_width = 320
img_height = 180
# command and params for ffmpeg
command = ['ffmpeg',
    '-re',
    '-y',
    '-f', 'rawvideo',
    '-s', f'{img_width}x{img_height}',
    '-r', '15',
    '-pixel_format', 'bgr24',
    '-vcodec', 'rawvideo',
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'veryfast',
    '-r', '15',  # Set the output frame rate
    '-g', '5',  # Set keyframe interval 
    '-bufsize', '64M',  # Adjust the buffer size as needed
    '-f', 'flv',
    '-threads', '2',  # Adjust the number of threads for encoding
    '-flvflags', 'no_duration_filesize',
    '-drop_pkts_on_overflow','1',
    '-attempt_recovery','1',
    '-recovery_wait_time','1',
    '-loglevel', 'warning',
    rtmp_url]



p = subprocess.Popen(command, stdin=subprocess.PIPE)


def draw_current_time(frame):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    cv.putText(frame, current_time, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv.LINE_AA)

def drawRectangle(frame, objects):

    # print(objects)
    for obj in objects:
        x, y, width, height = obj["x"], obj["y"], obj["width"], obj["height"]
        class_label = obj["class"]

        # Draw a rectangle on the image with class-specific color
        cv.rectangle(frame, (x, y), (x + width, y + height), colors[class_label], 1)

        # Display class label with class-specific color
        cv.putText(frame, class_label, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, colors[class_label], 1)
    
def base64_to_stdin(base64_data, objects):

    # frame = cv.imdecode(np.frombuffer(base64.b64decode(base64_data), np.uint8), cv.IMREAD_COLOR)
    # Decode base64 data to bytes
    image_bytes = base64.b64decode(base64_data)

    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # Decode the image array
    frame = cv.imdecode(nparr, cv.IMREAD_COLOR)
    # draw_current_time(frame)
    drawRectangle(frame, objects)

    # Write the frame to the FFmpeg subprocess
    p.stdin.write(frame.tobytes())
    # p.stdin.flush()
    del image_bytes, nparr, frame

def subscribe_to_redis(topic="object_detection_2d"):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    pubsub = r.pubsub()
    pubsub.subscribe(topic)

    for message in pubsub.listen():
        if message["type"] == "message":
            json_data = json.loads(message['data'].decode('utf-8'))
            position = os.environ.get('position')

            # Check the position and assign the corresponding image URL to the variable 'image'
            if position == 'top':
                image = json_data['images'][0]
                objects = json_data['objects_top']
            elif position == 'left':
                image = json_data['images'][1]
                objects = json_data['objects_left']
            elif position == 'right':
                image = json_data['images'][2]
                objects = json_data['objects_right']
            # first_image = json_data['images'][0]
            # first_objects = json_data['objects_top']
            base64_to_stdin(image, objects)



def close_subprocess():
    if p.poll() is None:
        p.stdin.close()
        p.wait()

if __name__ == "__main__":
    atexit.register(close_subprocess)
    subscribe_to_redis()
