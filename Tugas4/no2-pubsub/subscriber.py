import os
import zmq

PORT = int(os.environ.get('ZMQ_PORT', 5557))
SUB_ID = os.environ.get('SUB_ID', 'sub-1')
TOPIC = os.environ.get('TOPIC', 'sensors')


def main():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    connect_addr = f"tcp://publisher:{PORT}"
    fallback_addr = f"tcp://127.0.0.1:{PORT}"
    try:
        sock.connect(connect_addr)
        print(f"{SUB_ID} connected to {connect_addr}")
    except Exception:
        sock.connect(fallback_addr)
        print(f"{SUB_ID} connected to fallback {fallback_addr}")

    # subscribe to topic
    sock.setsockopt_string(zmq.SUBSCRIBE, TOPIC)

    try:
        while True:
            s = sock.recv_string()
            # message format: "<topic> <json>"
            topic, _, payload = s.partition(' ')
            print(f"{SUB_ID} Received on [{topic}]: {payload}")
    except KeyboardInterrupt:
        print(f"{SUB_ID} stopping")
    finally:
        sock.close()
        ctx.term()


if __name__ == '__main__':
    main()
