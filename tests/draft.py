from secure_cipher.encryption import AsciiOffsetEncryption
from secure_cipher.decryption import AsciiOffsetDecryption

# 创建ASCII偏移加密实例
ascii_encryptor = AsciiOffsetEncryption()
ascii_decryptor = AsciiOffsetDecryption()

# 使用偏移量和密钥进行加密
text = "Hello, World!"
encrypted = ascii_encryptor.encrypt(text, offset=5, key="secret")
print(f"Encrypted: {encrypted}")

# 使用相同的偏移量和密钥解密
decrypted = ascii_decryptor.decrypt(encrypted, offset=5, key="secret")
print(f"Decrypted: {decrypted}")  # 输出: Hello, World!
