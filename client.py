from socket import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class client():
    def __init__(self):
        self.key = RSA.generate(2048)
        self.clientSocket=socket()

    def getPublicKey(self):
        return self.key.publickey().exportKey("PEM")

    def connectSocket(self,addr,port):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP宣告
        self.clientSocket.connect(addr,port)

    def RSA_ecrypt(self,cipherText):
        cipher = PKCS1_OAEP.new(self.key)
        plainText = cipher.decrypt(cipherText)
        return plainText
    
    def RSA_encrypt(self,plainText):
        cipher = PKCS1_OAEP.new(self.key)
        cipherText = cipher.encrypt(plainText)
        return cipherText