from core import Servo, AES
import asyncio
import hashlib
import random
import time

class OpenDoorTask:
    def __init__(self, ble):
        self.ble = ble
        self.passwd = "123456"
        # 将密码转换为32字节的AES密钥
        self.aes_key = hashlib.sha256(self.passwd.encode('utf-8')).digest()
    
        self.SERVICE_UUID_STR = "1F04F3B3-0000-63B0-B612-3A8B9FE101AB"        # 用于接收加密响应的特征
        self.CHARACTERISTIC_UUID_STR = "1F04F3B3-0001-63B0-B612-3A8B9FE101AB"
        # 用于发送随机数挑战的特征
        self.CHALLENGE_CHARACTERISTIC_UUID_STR = "1F04F3B3-0002-63B0-B612-3A8B9FE101AB"
        self.servo = Servo.Servo180(15)
        
        # 当前挑战随机数和上次生成时间
        self.current_challenge = None
        self.last_challenge_time = 0

        self.ble.add_service(self.SERVICE_UUID_STR)
        self.ble.add_characteristic(self.SERVICE_UUID_STR, self.CHARACTERISTIC_UUID_STR, write=True)
        self.ble.add_characteristic(self.SERVICE_UUID_STR, self.CHALLENGE_CHARACTERISTIC_UUID_STR, read=True, notify=True)

    def generate_new_challenge(self):
        """生成新的8字节随机数挑战"""
        self.current_challenge = bytes([random.randint(0, 255) for _ in range(8)])
        print(f"生成新挑战: {self.current_challenge.hex()}")

    async def task(self):
        while True:
            # 每30秒生成新的挑战随机数
            current_time = time.time()
            if current_time - self.last_challenge_time >= 30 or self.current_challenge is None:
                self.generate_new_challenge()
                self.last_challenge_time = current_time
                # 通过蓝牙特征发送新的挑战
                self.ble.write_data(self.SERVICE_UUID_STR, self.CHALLENGE_CHARACTERISTIC_UUID_STR, self.current_challenge)
            
            # 检查是否有加密响应数据
            data = await self.ble.read_data(self.SERVICE_UUID_STR, self.CHARACTERISTIC_UUID_STR)
            if self.verify(data):
                print("验证成功，开门！")
                self.servo.servo_start()
                self.servo.servo_set_angle(30)
                await asyncio.sleep(5)
                self.servo.servo_set_angle(180)
                await asyncio.sleep(2)
                self.servo.servo_stop()
                # 开门后生成新的挑战，防止重放攻击
                self.generate_new_challenge()
                self.last_challenge_time = current_time
                self.ble.write_data(self.SERVICE_UUID_STR, self.CHALLENGE_CHARACTERISTIC_UUID_STR, self.current_challenge)
            await asyncio.sleep(1)
    
    def verify(self, data):
        """验证加密响应是否正确"""
        if data is None or self.current_challenge is None:
            return False
        
        try:
            # 解密接收到的数据
            aes = AES.AES()
            decrypted_data = aes.AES_decrypt(data, self.aes_key)
            
            # 比较解密后的数据与当前挑战随机数
            if decrypted_data == self.current_challenge:
                print("挑战验证成功！")
                return True
            else:
                print(f"挑战验证失败，期望: {self.current_challenge.hex()}, 收到: {decrypted_data.hex()}")
                return False
        except Exception as e:
            print(f"解密失败: {e}")
            return False