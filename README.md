# Secure Ciphertext

一个简单而灵活的Python文本加密解密库，支持自定义字符映射规则。

## 特性

- 支持自定义字符映射进行加密和解密
- 支持使用字典或关键字参数定义映射规则
- 支持多字符替换
- 简单易用的API

## 安装

### 注意：pip暂不支持，因为我没有上传到pypi，后面上传了可能会支持
```bash
pip install secure-ciphertext
```

## 快速开始

```python
from secure_cipher.encryption import StringReplaceEncryption
from secure_cipher.decryption import StringReplaceDecryption

# 创建加密和解密实例
encryptor = StringReplaceEncryption()
decryptor = StringReplaceDecryption()

# 使用关键字参数定义映射规则
text = "Hello, World!"
encrypted = encryptor.encrypt(text, H="b", W="c")
print(f"Encrypted: {encrypted}")  # 输出: bello, corld!

# 使用相同的映射规则解密
decrypted = decryptor.decrypt(encrypted, H="b", W="c")
print(f"Decrypted: {decrypted}")  # 输出: Hello, World!

# 使用字典定义映射规则
mapping = {
    'H': 'b',
    'W': 'c'
}
encrypted = encryptor.encrypt(text, replace_map=mapping)
decrypted = decryptor.decrypt(encrypted, replace_map=mapping)
```

## 高级用法

### 多字符替换

支持将一个字符替换为多个字符：

```python
from secure_cipher.encryption import StringReplaceEncryption
from secure_cipher.decryption import StringReplaceDecryption

# 创建加密和解密实例
encryptor = StringReplaceEncryption()
decryptor = StringReplaceDecryption()

# 定义多字符替换映射
mapping = {
    'H': 'hello',
    'W': 'world'
}
text = "Hi, World!"
encrypted = encryptor.encrypt(text, replace_map=mapping)
print(f"Encrypted: {encrypted}")

decrypted = decryptor.decrypt(encrypted, replace_map=mapping)
print(f"Decrypted: {decrypted}")  # 输出: Hi, World!
```

### ASCII偏移加密

除了字符替换加密外，还支持ASCII偏移加密：

```python
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

# 支持字符串、字节和文件对象
# 此代码需要example.exe文件，当然你可以忽略注释或删除此代码
with open('example.txt', 'rb') as f:
    encrypted_file = ascii_encryptor.encrypt(f, offset=3, key="key")
```

## 开发

1. 克隆仓库
```bash
git clone https://github.com/yourusername/secure-ciphertext.git
cd secure-ciphertext
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行测试
```bash
python -m unittest discover tests
```

## 贡献

欢迎提交Pull Request或创建Issue！

## 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件
