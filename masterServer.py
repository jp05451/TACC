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
    
    def generateMasterKey(self,N,T):\
        # N = split of the master key
        # T = least shares to combine master key
        
        number_length = 4
        self.p = number.getPrime(number_length)
        
        # generate master key
        masterKey=random.randint(0,self.p-1)
        
        # split the master key to N splits
        self.__masterkeyShare=shamirs.shares(masterKey,quantity=N,threshold=T,modulus=self.p)
        
        
        
        
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