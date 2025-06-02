"""
加密模块
=======

此模块提供了各种数据加密功能。
"""
import os
from typing import Union, List, Dict


class AsciiOffsetEncryption:
    """
    ASCII偏移加密类

    使用ASCII码偏移和密钥对数据进行加密。支持字符串、字节和文件输入。

    属性:
        type (str): 加密状态 ('after encryption')
        text (Union[str, bytes]): 加密后的数据
    """

    def __init__(self):
        self.type = 'after encryption'
        self.text = None

    def _process_ascii_list(self, ascii_list: List[int], offset: int = 0, key: str = None, is_bytes: bool = False) -> List[int]:
        """
        处理ASCII码列表，应用偏移量和密钥

        参数:
            ascii_list: ASCII码列表
            offset: ASCII偏移量
            key: 加密密钥
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
            # 应用偏移
            new_val = ascii_val + offset
            # 如果有密钥，加上密钥对应位置的ASCII值
            if key_ascii:
                new_val += key_ascii[i]
            # 处理溢出
            if is_bytes:
                # 对字节类型使用ASCII范围（0-255）
                new_val = new_val % 256
            else:
                # 对字符串类型使用Unicode范围（0-65535）
                new_val = new_val % 65536
            result.append(new_val)

        return result

    def encrypt(self, data: Union[str, bytes, '_io.BufferedReader'], offset: int = 0, key: str = None) -> Union[str, bytes]:
        """
        加密数据

        参数:
            data: 要加密的数据，可以是字符串、字节或文件对象(_io.BufferedReader)
            offset: ASCII偏移量（可选）
            key: 加密密钥（可选）

        返回:
            加密后的数据（字符串或字节）
        """
        # 处理不同类型的输入
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


class StringReplaceEncryption:
    """
    字符替换加密类

    使用字符映射表对文本进行加密。支持使用字典或关键字参数定义替换规则。

    属性:
        type (str): 加密状态 ('after encryption')
        text (str): 加密后的文本
        replace_map (Dict[str, str]): 当前使用的字符替换映射
    """

    def __init__(self):
        self.type = 'after encryption'
        self.text = None
        self.replace_map = {}

    def encrypt(self, text: str, replace_map: Dict[str, str] = None, **kwargs) -> str:
        """
        加密文本

        参数:
            text: 要加密的文本
            replace_map: 字符替换映射字典（可选）
            **kwargs: 字符替换的关键字参数（例如：a='@'）

        返回:
            加密后的文本

        示例:
            >>> encryption = StringReplaceEncryption()
            >>> # 使用字典方式
            >>> encrypted = encryption.encrypt("Hello", {"H": "#", "e": "3"})
            >>> # 使用关键字参数方式
            >>> encrypted = encryption.encrypt("Hello", H="#", e="3")
        """
        # 合并替换映射
        self.replace_map = {}
        if replace_map:
            self.replace_map.update(replace_map)
        if kwargs:
            self.replace_map.update(kwargs)

        # 如果没有提供替换规则，抛出异常
        if not self.replace_map:
            raise ValueError("必须提供字符替换映射（通过replace_map或关键字参数）")

        # 执行字符替换
        result = text
        for old_char, new_char in self.replace_map.items():
            result = result.replace(old_char, new_char)

        self.text = result
        return result
