import redis
import base64
import time

def convert_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def pre_produce_images(image_count):
    base64_images = {}
    for i in range(1, image_count + 1):
        image_path = f"/Users/chang/nodejs/modelt-3-tnn/public/{i}.jpg"
        base64_data = convert_to_base64(image_path)
        base64_images[str(i)] = base64_data
    return base64_images

def publish_to_redis(base64_images, topic="od"):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    while True:
        for key, value in base64_images.items():
            r.publish(topic, value)
            # r.hset(topic, key, value)  # Using a hash to store key-value pairs in Redis
            time.sleep(0.066)

if __name__ == "__main__":
    image_count = 50
    base64_images = pre_produce_images(image_count)
    publish_to_redis(base64_images)
