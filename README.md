# RoomDoorService

基于 ESP32 的智能门锁控制系统，使用 MicroPython 开发。

## 功能特性

- 🔐 智能门锁控制
- 📶 WiFi 连接支持
- 📡 蓝牙 BLE 通信
- 🔆 光传感器检测
- ⏰ 在线时间同步
- 🎛️ 舵机门锁控制
- 🔐 AES 加密安全

## 项目结构

```
├── boot.py              # 启动脚本
├── main.py              # 主程序入口
├── core/                # 核心功能模块
│   ├── AES.py          # AES 加密模块
│   ├── Ble.py          # 蓝牙通信模块
│   ├── LightSensor.py  # 光传感器模块
│   ├── OnlineTime.py   # 在线时间同步
│   ├── Servo.py        # 舵机控制模块
│   └── Wifi.py         # WiFi 连接模块
└── task/                # 任务处理模块
    ├── MainTask.py     # 主任务处理
    └── OpenDoorTask.py # 开门任务处理
```

## 硬件要求

- ESP32 开发板
- 舵机（用于门锁控制）
- 光传感器
- 其他相关硬件组件

## 安装和使用

1. 将项目文件上传到 ESP32 设备
2. 配置 WiFi 连接参数
3. 根据需要调整硬件引脚配置
4. 运行 `main.py` 启动系统

## 开发环境

- MicroPython
- ESP32 开发环境
- VS Code (推荐)

## 许可证

本项目采用 MIT 许可证。