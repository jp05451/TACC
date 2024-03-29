import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class Client:
    def __init__(self):
        self.key = RSA.generate(2048)
        self.clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # TCP宣告

    def __del__(self):
        self.clientSocket.close()

    def getPublicKey(self):
        return self.key.publickey().exportKey("PEM")

    def connectSocket(self, addr, port):
        self.clientSocket.connect((addr, port))

    def RSA_PrivateKeyEcrypt(self, cypherText):
        cipher = PKCS1_OAEP.new(self.key)
        plainText = cipher.decrypt(cypherText)
        return plainText

    def RSA_PrivateKeyDecrypt(self, plainText):
        cipher = PKCS1_OAEP.new(self.key)
        cypherText = cipher.encrypt(plainText)
        return cypherText

    def sendPublicKey(self):
        self.clientSocket.send(self.getPublicKey())


if __name__ == "__main__":
    Client = Client()
    Client.connectSocket("127.0.0.1",8888)
    Client.sendPublicKey()
