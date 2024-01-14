import cv2 as cv
import subprocess
import time
import numpy as np
import redis
import base64
import atexit
import os

rtmp_url = os.environ.get('rtmp_url')


img_width = 250
img_height = 250
# command and params for ffmpeg
command = ['ffmpeg',
    '-re',
    '-y',
    '-f', 'rawvideo',
    '-s', f'{img_width}x{img_height}',
    '-r', '13',
    '-pixel_format', 'bgr24',
    '-vcodec', 'rawvideo',
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'veryslow',
    '-r', '13',  # Set the output frame rate
    '-g', '30',  # Set keyframe interval 
    # '-bufsize', '64M',  # Adjust the buffer size as needed
    '-f', 'flv',
    # '-maxrate', '4M',
    '-flvflags', 'no_duration_filesize',
    '-drop_pkts_on_overflow','1',
    '-attempt_recovery','1',
    '-recovery_wait_time','1',
    '-loglevel', 'warning',
    rtmp_url]

image_count = 1

p = subprocess.Popen(command, stdin=subprocess.PIPE)

# del
def convert_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def pre_produce_images(image_count):
    base64_images = {}
    for i in range(1, image_count + 1):
        image_path = f"/public/{i}.jpg"
        base64_data = convert_to_base64(image_path)
        base64_images[str(i)] = base64_data
    return base64_images
# del

def draw_current_time(frame):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    cv.putText(frame, current_time, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv.LINE_AA)
    
def base64_to_stdin(base64_data):
    # Decode base64 data to bytes
    # image_bytes = base64.b64decode(base64_data)
    # Convert bytes to numpy array
    # nparr = np.frombuffer(image_bytes, np.uint8)
    # Decode the image array
    frame = cv.imdecode(np.frombuffer(base64.b64decode(base64_data), np.uint8), cv.IMREAD_COLOR)

    # Draw current time on the frame
    draw_current_time(frame)
    # frame_bytes = nparr.tobytes()

    # Write the frame to the FFmpeg subprocess
    p.stdin.write(frame.tobytes())
    # p.stdin.flush()
    del frame

def message_handler(message):
    base64_to_stdin(message['data'].decode('utf-8'))

counter = 0
pre_time = time.time()
def subscribe_to_redis(topic="od"):
    r = redis.Redis(host='localhost', port=6379, db=0)
    pubsub = r.pubsub()
    pubsub.subscribe(topic)

    for message in pubsub.listen():
        if message["type"] == "message":
            receive_time = time.time()  # Record the start time
            global counter, pre_time
            counter += 1
            # message_handler(message)
            base64_to_stdin(message['data'].decode('utf-8'))
            execution_time = receive_time - pre_time
            pre_time = receive_time  # Record the end time
            print(f'Received {counter} messages. Execution time: {execution_time} seconds')

def mock_redis_sub(base64_images):
    while True:
        for key, value in base64_images.items():
            base64_to_stdin(value)
            time.sleep(0.066)
def close_subprocess():
    if p.poll() is None:
        p.stdin.close()
        p.wait()

if __name__ == "__main__":
    atexit.register(close_subprocess)
    # subscribe_to_redis()
    image_count = 50
    base64_images = pre_produce_images(image_count)
    mock_redis_sub(base64_images)