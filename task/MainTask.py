from micropython import const

class MainTask:
    def __init__(self, ble):
        self.ble = ble
        self.ble._ADV_APPEARANCE_GENERIC = const(1036)
        self.ble.device_info['name'] = "StackAll's Headquarters"

    async def task(self):
        self.ble.register_services()
        await self.ble.advertise()