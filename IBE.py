from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# from Crypto.Random import get_random_bytes
from Crypto.Util import number
from random import Random
import shamirs

Random.seed()


class IBE:
    def __init__(self):
        # self.master_key = get_random_bytes(16)  # 128-bit隨機主密鑰
        self.p = number.getPrime(2**16 - 1)

    def generateMasterKeyShares(self, N=5, T=5):
        masterKey = Random.randint(0, self.p - 1)
        self.__k = Random.randint(0, self.p - 1)

        # split master key to key shares
        self.__masterkeyShare = shamirs.shares(
            masterKey, quantity=N, threshold=T, modulus=self.p
        )

    def generateSecretKeyShare(self, masterKeyShare: shamirs.share, id):
        idNumber = int(sha256(id)) % self.p

        self.__secretKeyShare = []
        self.__secretKeyShare.append(masterKeyShare.value + idNumber + self.__k)

    def getSecretKeyShare(self, keyNumber):
        return self.__secretKeyShare[keyNumber]

    def getMasterKey(self, keyNumber):
        return (self.__masterkeyShare[keyNumber], self.__k)

    def generate_secret_key(self, identity):
        # 將身份和主密鑰組合在一起
        combined_key = identity.encode() + self.master_key
        # 使用 SHA-256 哈希來生成身份密鑰
        hashed_key = sha256(combined_key).digest()
        return hashed_key

    def encrypt(self, message, identity):
        secret_key = self.generate_secret_key(identity)
        cipher = AES.new(secret_key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        iv = cipher.iv
        return ciphertext, iv

    def decrypt(self, ciphertext, iv, identity):
        secret_key = self.generate_secret_key(identity)
        cipher = AES.new(secret_key, AES.MODE_CBC, iv=iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode()


# 使用範例
ibe = IBE()

# 加密消息
message = "Hello, world!"
identity = "user@example.com"
ciphertext, iv = ibe.encrypt(message, identity)

# 解密消息
decrypted_message = ibe.decrypt(ciphertext, iv, identity)
print("Decrypted message:", decrypted_message)
