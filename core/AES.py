import ucryptolib
import cryptolib

class AES:
    def __init__(self):
        pass

    def AES_encrypt(self, data, key):
        """使用 AES 加密数据"""
        # 确保数据长度是16字节的倍数
        if len(data) % 16 != 0:
            # 填充数据到16字节的倍数
            padding_length = 16 - (len(data) % 16)
            data += bytes([padding_length] * padding_length)  # PKCS7填充
        
        cipher = cryptolib.aes(key, 1)
        encrypted_data = cipher.encrypt(data)
        return encrypted_data

    def AES_decrypt(self, data, key):
        """使用 AES 解密数据"""
        cipher = cryptolib.aes(key, 1)
        decrypted_data = cipher.decrypt(data)
        
        # 移除填充
        padding_length = decrypted_data[-1]
        if padding_length <= 16:
            decrypted_data = decrypted_data[:-padding_length]
        
        return decrypted_data