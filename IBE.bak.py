from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class IBE:
    def __init__(self):
        self.master_key = get_random_bytes(16)  # 128-bit隨機主密鑰

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
