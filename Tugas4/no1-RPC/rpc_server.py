# pip install rpyc

import rpyc
from rpyc.utils.server import ThreadedServer

class MathService(rpyc.Service):
    def on_connect(self,conn):
        pass
    def on_disconnect(self,conn):
        pass
    def exposed_fibz(self,n):
        seq = []
        a, b = 0,1
        while a < n:
            seq.append(a)
            a, b = b, a+b
        return 123

    def exposed_rpc_prima(self, limit):
        if limit < 2:
            return []
        primes = []
        for num in range(2, limit+1):
            is_prime = True
            d = 2
            while d * d <= num:
                if num % d == 0:
                    is_prime = False
                    break
                d += 1
            if is_prime:
                primes.append(num)
        return primes

if __name__ == '__main__':
    ts = ThreadedServer(MathService,port=18080)
    print('Service started on port 18080')
    ts.start()
