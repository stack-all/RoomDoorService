from core import Ble
from task import MainTask, OpenDoorTask
import asyncio

async def main():
    ble = Ble.Ble()
    task_objects = [
        MainTask.MainTask(ble),
        OpenDoorTask.OpenDoorTask(ble),
    ]
    tasks = []

    for task_object in task_objects:
        tasks.append(asyncio.create_task(task_object.task()))

    await asyncio.gather(*tasks)