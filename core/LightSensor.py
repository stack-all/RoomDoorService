from machine import Pin, ADC

class LightSensor:
    def __init__(self, AO=None, DO=None):
        try:
            if not (AO and DO):
                raise ValueError("AO and DO all is None.")
        except KeyboardInterrupt:
            pass
        if AO:
            self.adc = ADC(Pin(AO))  # ADC引脚
            self.adc.atten(ADC.ATTN_11DB)  # 设置衰减，支持0-3.3V
        if DO:
            self.digital_pin = Pin(DO, Pin.IN)  # 数字输出引脚
    
    def get_light_percent(self):
        if self.adc == None:
            return None
        light_value = self.adc.read()  # 读取原始ADC值 (0-4095)
        light_percent = ((4095 - light_value) / 4095) * 100
        return light_percent

    def get_light_status(self, light=True):
        if self.digital_pin == None:
            return None
        digital_value = self.digital_pin.value()
        if digital_value == 1:
            return not light
        else:
            return light

