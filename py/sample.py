import redis
import logging
import json

def subscribe_to_redis(topic="object_detection_2d"):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    print(r.ping())
    logging.info(r.ping())
    pubsub = r.pubsub()
    pubsub.subscribe(topic)

    for message in pubsub.listen():
        print('on listen')
        if message["type"] == "message":
            json_data = json.loads(message['data'].decode('utf-8'))
            first_image = json_data['images'][0]
            print('len')
            print(len(first_image))

if __name__ == "__main__":
    logging.info('start')
    subscribe_to_redis()