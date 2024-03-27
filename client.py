from socket import socket
from Crypto.PublicKey import RSA

class client():
    def __init__(self):
        self.key = RSA.generate(2048)
        self.clientSocket=socket()

    def getPublicKey(self):
        return self.key.publickey().exportKey("PEM")

    def connectSocket(self,addr,port):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP宣告
        self.clientSocket.connect(addr,port)
