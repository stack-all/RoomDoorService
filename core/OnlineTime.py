import ntptime
import utime
from machine import RTC

class OnlineTime:
    def __init__(self, timezone_offset=8):
        """
        初始化在线时间类
        :param timezone_offset: 时区偏移量（小时），默认为8（北京时间）
        """
        self.timezone_offset = timezone_offset
        self.rtc = RTC()

    def sync_time(self, ntp_server='192.168.3.1'):
        """
        从NTP服务器同步时间，并设置到硬件RTC
        :param ntp_server: NTP服务器地址
        :return: 成功返回True，失败返回False
        """
        try:
            # 设置NTP服务器
            ntptime.host = ntp_server
            # 同步时间
            ntptime.settime()
            
            # 将同步的时间设置到硬件RTC
            utc_time = utime.time()
            local_time = utc_time + (self.timezone_offset * 3600)
            time_tuple = utime.localtime(local_time)
            
            # 设置RTC时间 (年, 月, 日, 星期, 时, 分, 秒, 微秒)
            self.rtc.datetime((time_tuple[0], time_tuple[1], time_tuple[2], 
                                time_tuple[6], time_tuple[3], time_tuple[4], 
                                time_tuple[5], 0))
            return True
        except:
            return False
    
    def get_local_time(self):
        """
        获取本地时间（考虑时区偏移）
        :return: 格式化的时间字符串
        """
        try:
            # 获取UTC时间
            utc_time = utime.time()
            # 加上时区偏移
            local_time = utc_time
            # 转换为本地时间元组
            time_tuple = utime.localtime(local_time)
            
            # 格式化时间字符串 YYYY-MM-DD HH:MM:SS
            formatted_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                time_tuple[0], time_tuple[1], time_tuple[2],
                time_tuple[3], time_tuple[4], time_tuple[5]
            )
            return formatted_time
        except Exception as e:
            return None
    
    def get_timestamp(self):
        """
        获取当前时间戳
        :return: 时间戳
        """
        try:
            return utime.time() + 946656000
        except Exception as e:
            return None