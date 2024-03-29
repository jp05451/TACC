from socket import socket
from base64 import b64decode,b64encode
# import random

from Crypto.Cipher import PKCS1_OAEP


class server:
    def __init__(self):
        self.serverSocket = socket()
        self.share = 0

    def socketConnect(self, addr, port):
        self.serverSocket.bind((addr, port))
        self.serverSocket.listen(5)

    def __del__(self):
        self.serverSocket.close()

    def recvPublicKey(self):
        client, addr = self.serverSocket.accept()
        self.clientPublicKey = client.recv(1024).decode()
        client.close()

    def RSA_Decrypt(self, cypherText,key):
        cipher = PKCS1_OAEP.new(key)
        plainText = cipher.decrypt(b64decode(cypherText))
        return plainText.decode("utf-8")

    def RSA_Encrypt(self, msg,key):
        cipher = PKCS1_OAEP.new(key)
        cypherText = cipher.encrypt(msg.encode("utf-8"))
        return b64encode(cypherText).decode()

    def SendKeyShares(self):
        client, addr = self.serverSocket.accept()
        clientRequest = client.recv(1024).decode()
        
        
        if clientRequest == "1234":
            client.send(self.RSA_Encrypt(self.share))

        client.close()

if __name__ == "__main__":
    Server = server()
    Server.socketConnect("0.0.0.0", 8888)
    Server.recvPublicKey()
    print(Server.clientPublicKey)
