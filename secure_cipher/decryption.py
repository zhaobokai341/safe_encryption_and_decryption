"""
解密模块

此模块提供了与加密模块相对应的解密功能。

此模块提供了与加密模块相对应的解密功能。
"""
import os
from typing import Union, List, Dict


class AsciiOffsetDecryption:
    """
    ASCII偏移解密类

    使用ASCII码偏移和密钥对数据进行解密。支持字符串、字节和文件输入。

    属性:
        type (str): 解密状态 ('after decryption')
        text (Union[str, bytes]): 解密后的数据
    """

    def __init__(self):
        self.type = 'after decryption'
        self.text = None

    def _process_ascii_list(self, ascii_list: List[int], offset: int = 0, key: str = None, is_bytes: bool = False) -> List[int]:
        """
        处理ASCII码列表，移除偏移量和密钥的影响

        参数:
            ascii_list: ASCII码列表
            offset: ASCII偏移量
            key: 解密密钥
            is_bytes: 是否为字节类型数据（决定使用ASCII还是Unicode范围）
        """
        # 如果有密钥，将其转换为ASCII码列表
        key_ascii = []
        if key:
            key_ascii = [ord(c) for c in key]
            # 如果密钥比文本短，循环使用密钥
            key_ascii = key_ascii * (len(ascii_list) // len(key_ascii) + 1)
            key_ascii = key_ascii[:len(ascii_list)]

        # 处理偏移量和密钥
        result = []
        for i, ascii_val in enumerate(ascii_list):
            # 如果有密钥，减去密钥对应位置的ASCII值
            new_val = ascii_val
            if key_ascii:
                new_val -= key_ascii[i]
            # 应用偏移
            new_val -= offset
            # 处理溢出
            if is_bytes:
                # 对字节类型使用ASCII范围（0-255）
                new_val = new_val % 256
            else:
                # 对字符串类型使用Unicode范围（0-65535）
                new_val = new_val % 65536
            result.append(new_val)

        return result

    def decrypt(self, data: Union[str, bytes, '_io.BufferedReader', 'AsciiOffsetEncryption'], offset: int = 0, key: str = None) -> Union[str, bytes]:
        """
        解密数据

        参数:
            data: 要解密的数据，可以是字符串、字节、文件对象(_io.BufferedReader)或AsciiOffsetEncryption对象
            offset: ASCII偏移量（可选）
            key: 解密密钥（可选）

        返回:
            解密后的数据（字符串或字节）

        异常:
            TypeError: 当输入类型不支持时抛出
            ValueError: 当AsciiOffsetEncryption对象中没有加密文本时抛出
        """
        # 处理AsciiOffsetEncryption对象
        if str(type(data).__name__) == 'AsciiOffsetEncryption':
            if data.text is None:
                raise ValueError("加密对象中没有加密后的文本")
            return self.decrypt(data.text, offset, key)

        # 处理其他类型的输入
        if hasattr(data, 'read') and hasattr(data, 'mode') and 'b' in data.mode:  # 如果是二进制文件对象
            ascii_list = list(data.read())
            result = bytes(self._process_ascii_list(ascii_list, offset, key, is_bytes=True))
            self.text = result
            return result
        elif isinstance(data, str):  # 如果是字符串
            ascii_list = [ord(c) for c in data]
            result = ''.join(chr(val) for val in self._process_ascii_list(ascii_list, offset, key, is_bytes=False))
            self.text = result
            return result
        elif isinstance(data, bytes):  # 如果是字节
            ascii_list = list(data)
            result = bytes(self._process_ascii_list(ascii_list, offset, key, is_bytes=True))
            self.text = result
            return result
        else:
            raise TypeError("输入必须是字符串、字节或二进制文件对象")


class StringReplaceDecryption:
    """
    字符替换解密类

    使用字符映射表对数据进行解密。支持字符串输入。

    属性:
        type (str): 解密状态 ('after decryption')
        text (str): 解密后的数据
    """

    def __init__(self):
        self.type = 'after decryption'
        self.text = None

    def decrypt(self, data: Union[str, 'StringReplaceEncryption'], replace_map: Dict[str, str] = None, **kwargs) -> str:
        """
        解密数据

        参数:
            data: 要解密的数据，可以是字符串或StringReplaceEncryption对象
            replace_map: 字符替换映射字典，键为加密后的字符，值为原字符
            **kwargs: 可以直接传入键值对作为替换映射

        返回:
            解密后的文本

        异常:
            TypeError: 当输入类型不支持时抛出
            ValueError: 当StringReplaceEncryption对象中没有加密文本时抛出
        """
        # 处理StringReplaceEncryption对象
        if str(type(data).__name__) == 'StringReplaceEncryption':
            if data.text is None:
                raise ValueError("加密对象中没有加密后的文本")

            # 如果没有提供替换映射，使用加密对象中的映射（反转键值对）
            if not replace_map and not kwargs:
                reverse_map = {v: k for k, v in data.replace_map.items()}
                return self.decrypt(data.text, reverse_map)

            return self.decrypt(data.text, replace_map, **kwargs)

        # 处理字符串输入
        if not isinstance(data, str):
            raise TypeError("输入必须是字符串或StringReplaceEncryption对象")

        # 合并 replace_map 和 kwargs
        combined_map = {}
        if replace_map:
            combined_map.update(replace_map)
        if kwargs:
            combined_map.update(kwargs)

        # 如果没有提供替换映射，返回原文本
        if not combined_map:
            self.text = data
            return data

        # 执行字符替换（从最长的替换键开始，避免部分替换冲突）
        result = data
        # 反转映射：如果加密用 H="b"，我们需要把"b"替换回"H"
        for target_char, encrypted_char in sorted(combined_map.items(), key=lambda x: len(x[1]), reverse=True):
            result = result.replace(encrypted_char, target_char)

        self.text = result
        return result
