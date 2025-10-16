import rpyc
import socket
import time


def wait_for_host(host, port, timeout=20):
	start = time.time()
	while time.time() - start < timeout:
		try:
			s = socket.create_connection((host, port), timeout=1)
			s.close()
			return True
		except OSError:
			time.sleep(0.5)
	return False


def main(host='localhost'):
	if not wait_for_host(host, 18080, timeout=20):
		print(f"Timed out waiting for {host}:18080")
		return
	conn = rpyc.connect(host, 18080)
	primes = conn.root.rpc_prima(11)
	print(primes)


if __name__ == '__main__':
	main(host='server')