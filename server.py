from socket import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import shamirs


class server:
    def __init__(self):
        self.serverSocket = socket()

    def socketConnect(self, addr, port):
        self.serverSocket.bind((addr, port))
        self.serverSocket.listen(5)

    def __del__(self):
        self.serverSocket.close()
        
    def recvPublicKey(self):
        client,addr=self.serverSocket.accept()
        self.clientPublicKey=client.recv(1024).decode()
        client.close()
        
    # def 
        
if __name__ == "__main__":
    Server=server()
    Server.socketConnect("0.0.0.0",8888)
    Server.recvPublicKey()
    print(Server.clientPublicKey)
        
        