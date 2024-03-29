from socket import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class client:
    def __init__(self):
        self.key = RSA.generate(2048)
        self.clientSocket = socket()

    def __del__(self):
        self.clientSocket.close()

    def getPublicKey(self):
        return self.key.publickey().exportKey("PEM")

    def connectSocket(self, addr, port):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP宣告
        self.clientSocket.connect(addr, port)

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
    client = client()
