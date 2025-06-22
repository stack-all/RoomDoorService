from machine import PWM, Pin
import time

class Servo:
    def __init__(self, servo_pin, freq=50):
        self.servo_pin = servo_pin
        self.freq = freq
        self.servo = None
    
    def servo_start(self):
        """
        启动PWN信号
        """
        self.servo = PWM(Pin(self.servo_pin))
        self.servo.freq(self.freq) # 设置PWM频率为50Hz（舵机标准频率）

    def servo_stop(self):
        """
        完全停止PWM
        注意: 180度舵机通常保持PWM信号以维持位置
        """
        self.servo.deinit()

class Servo180(Servo):
    def servo_set_angle(self, angle):
        """
        设置180度舵机到指定角度位置
        
        参数:
            angle: 0-180度的角度值
                0度: 舵机最左位置
                90度: 舵机中间位置  
                180度: 舵机最右位置
        """
        # 限制角度范围
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
        
        # 计算占空比：1638 + (angle/180) * (8192-1638)
        duty = int(1638 + (angle / 180) * 6554)
        self.servo.duty_u16(duty)
