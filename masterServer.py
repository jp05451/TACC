from socket import socket
from base64 import b64decode,b64encode
import random

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util import number
import shamirs


class server:
    def __init__(self):
        self.serverSocket = socket()
        self.share = 1111
        random.seed()
        self.generateMasterKey()
        

    def socketConnect(self, addr, port):
        self.serverSocket.bind((addr, port))
        self.serverSocket.listen(5)

    def __del__(self):
        print("connection close")
        self.serverSocket.close()


    def RSA_Decrypt(self, cypherText,key):
        cipher = PKCS1_OAEP.new(key)
        plainText = cipher.decrypt(b64decode(cypherText))
        return plainText.decode("utf-8")

    def RSA_Encrypt(self, msg,key):
        key=RSA.importKey(key)
        cipher = PKCS1_OAEP.new(key)
        cypherText = cipher.encrypt(msg.encode("utf-8"))
        return b64encode(cypherText).decode()

    def recvPublicKey(self):
        client, addr = self.serverSocket.accept()
        self.clientPublicKey = client.recvfrom(1024).decode()
        client.close()
        
    def keySharing(self,secret:int,N,T):
        self.__secretShares = shamirs.shares(secret, quantity=N,threshold=T)
        

    def getShare(self,part:int):
        return self.__secretShares[part]
    
    def generateMasterKey(self):
        number_length = 4
        self.p = number.getPrime(number_length)
        
        # generate base number
        self.g1 = number.getPrime(number_length-1)
        self.g2 = number.getPrime(number_length-1)
        
        # generate index alpha
        alpha=random.randint(0,self.p-1)
        
        # generate PK and MSK
        self.PK=(self.g1,self.g1**alpha)
        # MSK=self.g2**alpha
        
        # split alpha
        alphaShares=shamirs.shares(alpha , modulus=self.p, quantity=5,threshold=5)
        self.MSK_shares=[(self.g1**i.value)%self.p for i in alphaShares]
        
        print(f"{self.g1} * {alpha}")
        
        print(f"p: {self.p}")
        print(self.MSK_shares)
        
        
        
        
        
        
    
        

if __name__ == "__main__":
    Server = server()
    # Server.generateMasterKey()
    # Server.socketConnect("0.0.0.0", 8888)
    # Server.serverSocket.listen(5)

    # connection, addr = Server.serverSocket.accept()

    # print('connected by ' + str(addr))
    # print("recv RSA:")
    # publickey=connection.recv(1024)
    # print(publickey)
    
    # print("sharing key")
    # Server.keySharing(1234,3,2)
    # keyshare=Server.getShare(2)
    # print(keyshare)
    
    # print("encrypting keyshare")
    # encryptKeyShare=Server.RSA_Encrypt(str(keyshare),publickey)

    # print("sending encrypted key share")
    # connection.send(encryptKeyShare.encode())
    
    # connection.close()