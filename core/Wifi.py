import network
import asyncio

class Wifi:
    def __init__(self, ssid, passwd):
        self.wlan = network.WLAN(network.STA_IF)
        self.ssid = ssid
        self.passwd = passwd

    def connect(self, ssid=None, passwd=None):
        if ssid != None:
            self.ssid = ssid
        if passwd != None:
            self.passwd = passwd
        if not self.wlan.isconnected():
            self.wlan.active(False)
            self.wlan.active(True)
            self.wlan.connect(self.ssid, self.passwd)
            asyncio.sleep(5)
            if not self.wlan.isconnected():
                return False
        return True

    def dis_connect(self):
        if self.wlan.isconnected():
            self.wlan.disconnect()
        self.wlan.active(False)
        return True
    