import socket
from base64 import b64decode
from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from time import sleep


class client:
    def __init__(self):
        self.key = RSA.generate(2048)
        self.clientSocket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM
        )  # TCP宣告

    def __del__(self):
        self.clientSocket.close()

    def getPublicKey(self):
        return self.key.publickey().exportKey()

    def getPrivateKey(self):
        return self.key.exportKey()

    def connectSocket(self, addr, port):
        self.clientSocket.connect((addr, port))

    def RSA_Decrypt(self, cypherText):
        key = RSA.importKey(self.getPrivateKey())
        cipher = PKCS1_OAEP.new(key)
        plainText = cipher.decrypt(b64decode(cypherText))
        return plainText

    def RSA_Encrypt(self, msg):
        key = RSA.importKey(self.getPrivateKey())
        cipher = PKCS1_OAEP.new(key)
        cypherText = cipher.encrypt(msg.encode("utf-8"))
        # return cypherText
        return b64encode(cypherText).decode()

    def sendPublicKey(self):
        self.clientSocket.send(self.getPublicKey())


if __name__ == "__main__":
    Client = client()

    Client.connectSocket("127.0.0.1", 8888)
    Client.sendPublicKey()
    encryptKeyShare = Client.clientSocket.recv(1024).decode()
    keyshare=Client.RSA_Decrypt(encryptKeyShare)
    print(keyshare)
