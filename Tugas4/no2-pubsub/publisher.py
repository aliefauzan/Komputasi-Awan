import os
import time
import json
import random
import zmq

# ZeroMQ PUSH socket will bind to this port
PORT = int(os.environ.get('ZMQ_PORT', 5557))
INTERVAL = int(os.environ.get('INTERVAL_SEC', 60))


def generate_dummy_sensor():
    return {
        'sensor_id': 'sensor-1',
        'timestamp': int(time.time()),
        'temperature': round(20 + random.random() * 10, 2),
        'humidity': round(30 + random.random() * 40, 2)
    }


def main():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    bind_addr = f"tcp://*:{PORT}"
    sock.bind(bind_addr)
    print(f"Publisher (PUB) bound to {bind_addr}")

    # publish two different topics
    topics = [
        os.environ.get('TOPIC_TEMP', 'sensors.temperature'),
        os.environ.get('TOPIC_HUM', 'sensors.humidity'),
    ]

    # Give subscribers time to connect and subscribe
    time.sleep(2)

    try:
        while True:
            msg = generate_dummy_sensor()
            payload = json.dumps(msg)
            # send one message for each topic
            for topic in topics:
                sock.send_string(f"{topic} {payload}")
                print(f"Published [{topic}]: {payload}")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Publisher stopping")
    finally:
        sock.close()
        ctx.term()


if __name__ == '__main__':
    main()
