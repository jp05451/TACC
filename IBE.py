from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from Crypto.Util import number
import random
import shamirs

random.seed()


class IBE:
    def __init__(self):
        # self.master_key = get_random_bytes(16)  # 128-bit隨機主密鑰
        self.p = number.getPrime(2**4 - 1)
        self.__generateMasterKeyShares(5, 5)

    def __generateMasterKeyShares(self, N=5, T=5):
        masterKey = random.randint(0, self.p - 1)
        self.__k = random.randint(0, self.p - 1)

        # split master key to key shares
        self.__masterkeyShare = shamirs.shares(
            masterKey, quantity=N, threshold=T, modulus=self.p
        )

    def generateSecretKeyShares(self, session):
        idNumber = int(sha256(session.encode()).hexdigest(), 16) % self.p
        # print(idNumber)

        # make secretShare by masterkeyshare + id + k
        self.__secretKeyShares = [s for s in self.__masterkeyShare]

        for i in range(len(self.__masterkeyShare)):
            self.__secretKeyShares[i].value = (
                self.__masterkeyShare[i].value + idNumber + self.__k
            )%self.p

    def getSecretKeyShare(self, keyNumber):
        return self.__secretKeyShares[keyNumber]


    def secretKeyReconstruct(self, secretKeyShares):
        # 將身份和主密鑰組合在一起
        print(secretKeyShares)
        print(shamirs.interpolate(secretKeyShares,5))
        return shamirs.interpolate(secretKeyShares)

    def encrypt(self, message, key: int):
        
        cipher = AES.new(key.to_bytes(16,'little'), AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        iv = cipher.iv
        return ciphertext, iv

    def decrypt(self, ciphertext, iv, key: int):
        
        cipher = AES.new(key.to_bytes(16, "little"), AES.MODE_CBC,iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode()


if __name__ == "__main__":
    # 使用範例
    ibe = IBE()

    shares = []
    print("generating secret key")
    ibe.generateSecretKeyShares("aaa")
    for i in range(5):
        shares.append(ibe.getSecretKeyShare(i))
    print(shares)

    key = ibe.secretKeyReconstruct(shares)
    print(key)

    # 加密消息
    message = "Hello, world!"
    ciphertext, iv = ibe.encrypt(message, key)

    # 解密消息
    decrypted_message = ibe.decrypt(ciphertext, iv, key)
    print("Decrypted message:", decrypted_message)
