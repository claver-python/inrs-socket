import socket
from sys import argv
from threading import Thread
from time import sleep

class Client:
    client = None
    host = None
    port = None
    active = False

    def __init__(self):
        self.host = None
        self.port = None
        #Client.connect(self, host, port)

    def connect(self, host=None, port=None):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if host == None and port == None:
            self.client.connect((self.host, self.port))
            self.active = True
            return
        self.client.connect((host, port))
        self.active = True

    def close(self):
        if self.client == None:
            return
        self.client.close()
        self.active = False

    def send(self, msg):
        if self.client == None or not self.active:
            return
        self.client.send(msg.encode("utf-8"))

if __name__ == "__main__":
    try:
        newClient = Client()
        newClient.connect("localhost", 8000)
        newClient.send("Client message to the server1\n")
        print("-messag1 sent")
        sleep(2)
        newClient.send("Client message to the server2\n")
        print("-messag2 sent")
        sleep(2)
        newClient.send("Client message to the server3\n")
        print("-messag3 sent")
        sleep(1)
        newClient.close()
        print("done!")
    except:
        print("Failed connecting to server")
