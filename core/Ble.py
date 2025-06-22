import bluetooth
from micropython import const
import asyncio
import aioble

class Ble:
    def __init__(self):
        self.ble = bluetooth.BLE()
        self.ble.active(False)
        self.ble.active(True)
        self.device_info = {
            "name": "ESP32",
        }
        # 蓝牙相关常量
        self._ADV_APPEARANCE_GENERIC = const(0) # 设备类型
        self._ADV_INTERVAL_MS = 500  # 广播间隔
        self._TIMEOUT_MS = 10_000  # 超时时间
        # 蓝牙服务和特征
        self.service_dict = {}
        self.characteristic_dict = {}

    async def advertise(self):
        services_list = [bluetooth.UUID(UUID) for UUID in self.service_dict.keys()]
        while True:
            try:
                async with await aioble.advertise(
                    self._ADV_INTERVAL_MS,
                    name=self.device_info["name"],
                    services=services_list,
                    appearance=self._ADV_APPEARANCE_GENERIC,
                ) as connection:
                    await connection.disconnected(timeout_ms=self._TIMEOUT_MS)
            except asyncio.CancelledError:
                pass
            except Exception as e:
                pass

    def add_service(self, service_UUID):
        if service_UUID in self.service_dict:
            return
        SERVICE_UUID = bluetooth.UUID(service_UUID)
        service = aioble.Service(SERVICE_UUID)
        self.service_dict[service_UUID] = service
    
    def add_characteristic(self, service_UUID, characteristic_UUID, write = False, read = False, notify = False):
        CHARACTERISTIC_UUID = bluetooth.UUID(characteristic_UUID)
        service = self.service_dict[service_UUID]
        characteristic = aioble.Characteristic(
            service, CHARACTERISTIC_UUID, write=write, read=read, notify=notify
        )
        self.characteristic_dict[service_UUID + characteristic_UUID] = characteristic

    def register_services(self):
        for service in self.service_dict.values():
            aioble.register_services(service)

    async def read_data(self, service_UUID, characteristic_UUID):
        characteristic = self.characteristic_dict[service_UUID + characteristic_UUID]
        connection = await characteristic.written()
        # 读取写入的数据
        data = characteristic.read()
        if data:
            return data
        await asyncio.sleep(1)

    def write_data(self, service_UUID, characteristic_UUID, data):
        characteristic = self.characteristic_dict[service_UUID + characteristic_UUID]
        characteristic.write(data)
