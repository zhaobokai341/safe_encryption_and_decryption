import unittest
import os
from secure_cipher.encryption import AsciiOffsetEncryption
from secure_cipher.decryption import AsciiOffsetDecryption
from io import BytesIO, StringIO


class TestSecureCipher(unittest.TestCase):
    def setUp(self):
        """测试前的设置"""
        self.encryption = AsciiOffsetEncryption()
        self.decryption = AsciiOffsetDecryption()

        # 创建测试数据
        self.test_string = "Hello, World!"
        self.test_bytes = b"Hello, World!"
        self.test_offset = 5
        self.test_key = "secret"

        # 创建测试文件
        self.test_file_path = "test_data.txt"
        with open(self.test_file_path, "wb") as f:
            f.write(self.test_bytes)

    def tearDown(self):
        """测试后的清理"""
        # 删除测试文件
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_string_encryption_decryption(self):
        """测试字符串的加密和解密"""
        # 加密
        encrypted = self.encryption.encrypt(self.test_string, offset=self.test_offset, key=self.test_key)
        # 解密
        decrypted = self.decryption.decrypt(encrypted, offset=self.test_offset, key=self.test_key)
        # 验证
        self.assertEqual(self.test_string, decrypted)

    def test_bytes_encryption_decryption(self):
        """测试字节的加密和解密"""
        # 加密
        encrypted = self.encryption.encrypt(self.test_bytes, offset=self.test_offset, key=self.test_key)
        # 解密
        decrypted = self.decryption.decrypt(encrypted, offset=self.test_offset, key=self.test_key)
        # 验证
        self.assertEqual(self.test_bytes, decrypted)

    def test_file_encryption_decryption(self):
        """测试文件对象的加密和解密"""
        # 打开文件进行加密
        with open(self.test_file_path, "rb") as f:
            encrypted = self.encryption.encrypt(f, offset=self.test_offset, key=self.test_key)

        # 解密
        decrypted = self.decryption.decrypt(encrypted, offset=self.test_offset, key=self.test_key)
        # 验证
        self.assertEqual(self.test_bytes, decrypted)

    def test_large_offset(self):
        """测试大偏移量"""
        large_offset = 1000
        # 加密
        encrypted = self.encryption.encrypt(self.test_bytes, offset=large_offset, key=self.test_key)
        # 解密
        decrypted = self.decryption.decrypt(encrypted, offset=large_offset, key=self.test_key)
        # 验证
        self.assertEqual(self.test_bytes, decrypted)

    def test_negative_offset(self):
        """测试负偏移量"""
        negative_offset = -5
        # 加密
        encrypted = self.encryption.encrypt(self.test_bytes, offset=negative_offset, key=self.test_key)
        # 解密
        decrypted = self.decryption.decrypt(encrypted, offset=negative_offset, key=self.test_key)
        # 验证
        self.assertEqual(self.test_bytes, decrypted)

    def test_empty_key(self):
        """测试空密钥"""
        # 加密
        encrypted = self.encryption.encrypt(self.test_bytes, offset=self.test_offset, key="")
        # 解密
        decrypted = self.decryption.decrypt(encrypted, offset=self.test_offset, key="")
        # 验证
        self.assertEqual(self.test_bytes, decrypted)

    def test_long_key(self):
        """测试长密钥"""
        long_key = "thisisaverylongkey" * 10
        # 加密
        encrypted = self.encryption.encrypt(self.test_bytes, offset=self.test_offset, key=long_key)
        # 解密
        decrypted = self.decryption.decrypt(encrypted, offset=self.test_offset, key=long_key)
        # 验证
        self.assertEqual(self.test_bytes, decrypted)

    def test_empty_input(self):
        """测试空输入"""
        empty_string = ""
        empty_bytes = b""

        # 测试空字符串
        encrypted = self.encryption.encrypt(empty_string, offset=self.test_offset, key=self.test_key)
        decrypted = self.decryption.decrypt(encrypted, offset=self.test_offset, key=self.test_key)
        self.assertEqual(empty_string, decrypted)

        # 测试空字节
        encrypted = self.encryption.encrypt(empty_bytes, offset=self.test_offset, key=self.test_key)
        decrypted = self.decryption.decrypt(encrypted, offset=self.test_offset, key=self.test_key)
        self.assertEqual(empty_bytes, decrypted)

    def test_ascii_overflow(self):
        """测试ASCII溢出处理"""
        # 创建一个包含接近255的字节值的测试数据
        test_data = bytes([254, 255, 0, 1])
        # 使用较大的偏移量进行加密
        encrypted = self.encryption.encrypt(test_data, offset=10, key=self.test_key)
        # 解密
        decrypted = self.decryption.decrypt(encrypted, offset=10, key=self.test_key)
        # 验证
        self.assertEqual(test_data, decrypted)

    def test_unicode_overflow(self):
        """测试Unicode溢出处理"""
        # 创建一个包含接近65535的Unicode字符的测试数据
        test_data = "".join([chr(65534), chr(65535), chr(0), chr(1)])
        # 使用较大的偏移量进行加密
        encrypted = self.encryption.encrypt(test_data, offset=10, key=self.test_key)
        # 解密
        decrypted = self.decryption.decrypt(encrypted, offset=10, key=self.test_key)
        # 验证
        self.assertEqual(test_data, decrypted)

    def test_encryption_object_input(self):
        """测试使用加密对象作为输入"""
        # 创建并加密数据
        self.encryption.encrypt(self.test_string, offset=self.test_offset, key=self.test_key)
        # 直接传入加密对象进行解密
        decrypted = self.decryption.decrypt(self.encryption, offset=self.test_offset, key=self.test_key)
        # 验证
        self.assertEqual(self.test_string, decrypted)

    def test_encryption_object_without_text(self):
        """测试使用未加密数据的加密对象作为输入"""
        # 创建一个新的加密对象但不加密任何数据
        empty_encryption = AsciiOffsetEncryption()
        # 尝试解密应该抛出ValueError
        with self.assertRaises(ValueError):
            self.decryption.decrypt(empty_encryption, offset=self.test_offset, key=self.test_key)


class TestStringReplace(unittest.TestCase):
    def setUp(self):
        """测试前的设置"""
        from secure_cipher.encryption import StringReplaceEncryption
        from secure_cipher.decryption import StringReplaceDecryption
        
        self.encryption = StringReplaceEncryption()
        self.decryption = StringReplaceDecryption()
        self.test_string = "Hello, World! 你好，世界！"
        
        # 测试用的替换映射
        self.replace_map = {
            'H': '#',
            'e': '3',
            'o': '0',
            'l': '1',
            'W': '@',
            'd': '4'
        }
        
        # 多字符替换映射
        self.multi_char_map = {
            'Hello': 'HELLO',
            'World': 'WORLD',
            '你好': '您好',
            '世界': '世间'
        }

    def test_dictionary_mapping(self):
        """测试使用字典映射进行加密解密"""
        # 加密
        encrypted = self.encryption.encrypt(self.test_string, replace_map=self.replace_map)
        
        # 解密（使用相同的映射）
        decrypted = self.decryption.decrypt(encrypted, replace_map=self.replace_map)
        
        # 验证
        self.assertEqual(self.test_string, decrypted)

    def test_keyword_arguments(self):
        """测试使用关键字参数进行加密解密"""
        # 加密
        encrypted = self.encryption.encrypt(
            self.test_string,
            H='#', e='3', o='0', l='1', W='@', d='4'
        )
        
        # 解密（使用相同的关键字参数）
        decrypted = self.decryption.decrypt(
            encrypted,
            H='#', e='3', o='0', l='1', W='@', d='4'
        )
        
        # 验证
        self.assertEqual(self.test_string, decrypted)

    def test_encryption_methods_equality(self):
        """测试不同加密方法的结果一致性"""
        # 使用字典映射加密
        encrypted1 = self.encryption.encrypt(self.test_string, replace_map=self.replace_map)
        
        # 使用关键字参数加密
        encrypted2 = self.encryption.encrypt(
            self.test_string,
            H='#', e='3', o='0', l='1', W='@', d='4'
        )
        
        # 验证两种方法结果相同
        self.assertEqual(encrypted1, encrypted2)

    def test_multi_char_replacement(self):
        """测试多字符替换功能"""
        # 加密
        encrypted = self.encryption.encrypt(self.test_string, replace_map=self.multi_char_map)
        
        # 解密（使用相同的映射）
        decrypted = self.decryption.decrypt(encrypted, replace_map=self.multi_char_map)
        
        # 验证
        self.assertEqual(self.test_string, decrypted)

if __name__ == '__main__':
    unittest.main()
