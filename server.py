import socket
import threading
from time import sleep

CHUNK = 1024
MAX_CONNECTION = 1

class StopWatcherException(Exception):
    def __init__(self, msg='server has been stopped'):
        self.message = msg
        super().__init__(msg)

class StopWatchException(Exception):
    def __init__(self, msg='server has stopped watching messages'):
        self.message = msg
        super().__init__(msg)
 
class Server():
    def __init__(self, host="localhost", port=8000):
        self._server = None
        self._callback = None
        self._client = None 
        self._running = False
        self._host = host
        self._port = port
        self.thread_server = None
        self.thread_msg = None

    def _accept(self):
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self._host, self._port))
        s.listen(MAX_CONNECTION)
        self._server = s
        while True:
            try:
                print("[accept]: Waiting for connection")
                conn, addr = s.accept()
                print(f"C[accept]: lient with ip {addr} is connected")
                self._client = conn
            except:
                print("[accept]: Cannot accept connections")
                print("[accept]: Removing client")
                self._client = None
                break

    def bind(self, host, port):
        self._host = host
        self._port = port
        return self

    def run(self):
        self._running = True
        print(f"[run]: Server listening on {self._host}:{self._port}")
        self.thread_server = threading.Thread(target=self._accept)
        self.thread_server.start()
        self.thread_msg = threading.Thread(target=self._on_message)
        self.thread_msg.start()
        return self

    def stop(self):
        print("[stop]: stopping server")
        self._running = False
        self._server.shutdown(socket.SHUT_RDWR)
        self._server.close()

    def register_cb(self, cb):
        self._callback = cb

    def _on_message(self):
        while True:
            try:
                msg = self._client.recv(CHUNK).decode("utf-8")
                print(f"[on_message]: received {msg}")
                if not msg or msg == "":
                    sleep(1)
                    continue
                self._callback(msg)
                print(f"[on_message]: sending '{msg}'")
            except:
                if not self._running:
                    print(f"[on_message]: stopping watching for messages")
                    break
                print("[on_message]: watching...")
                sleep(1)
                # if self._client:
                #     self._client.close()
                # raise StopWatcherException()

if __name__ == "__main__":
    server = Server().bind("localhost", 8000).run()
    # threading.Timer(5, server.stop).start()
    # threading.Timer(10, server.run).start()
    # threading.Timer(15, server.stop).start()
