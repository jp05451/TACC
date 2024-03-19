from socket import socket
from Crypto.PublicKey import RSA

class client():
    def __init__(self):
        self.key = RSA.generate(2048)

    def getPublicKey(self):
        return self.key.publickey().exportKey("PEM")

    # def 