import socket
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class client:
    def __init__(self):
        self.key = RSA.generate(2048)
        self.clientSocket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM
        )  # TCP宣告

    def __del__(self):
        self.clientSocket.close()

    def getPublicKey(self):
        return self.key.publickey().exportKey("DER")

    def getPrivateKey(self):
        return self.key.exportKey("DER")

    def connectSocket(self, addr, port):
        self.clientSocket.connect((addr, port))

    # def RSA_Decrypt(self, cypherText, key=0):
    #     if key == 0:
    #         key = self.getPrivateKey
    #     cipher = PKCS1_OAEP.new(key)
    #     plainText = cipher.decrypt(base64.b64decode(cypherText))
    #     return plainText

    # def RSA_Encrypt(self, msg, key=0):
    #     if key == 0:
    #         key = self.getPrivateKey
    #     cipher = PKCS1_OAEP.new(key)
    #     cypherText = cipher.encrypt(msg.encode("utf-8"))
    #     return base64.b64encode(cypherText).decode()

    def RSA_Decrypt(self, cypherText,key=0):
        if key == 0:
            key = self.getPrivateKey()
        cipher = PKCS1_OAEP.new(self.key)
        plainText = cipher.decrypt(base64.b64decode(cypherText))
        return plainText

    def RSA_Encrypt(self, msg,key=0):
        if key == 0:
            key=self.getPrivateKey()
        cipher = PKCS1_OAEP.new(self.key)
        cypherText = cipher.encrypt(msg.encode("utf-8"))
        # return cypherText
        return base64.b64encode(cypherText).decode()

    def sendPublicKey(self):
        self.clientSocket.send(self.getPublicKey())


if __name__ == "__main__":
    Client = client()
    cypher = Client.RSA_Encrypt(msg="1234",key=Client.getPrivateKey())
    print("Cypher:")
    print(cypher)

    print(Client.RSA_Decrypt(cypherText=cypher,key=Client.getPublicKey()))
    # from server import server

    # Server = server()
    # print(base64.b64decode(cypher))
    # text = Server.RSA_Decrypt(cypher, Client.getPublicKey())
    # print(text)
    # Client.connectSocket("127.0.0.1", 8888)
    # Client.sendPublicKey()
