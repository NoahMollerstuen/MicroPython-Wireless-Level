"""
MicroPython script which starts a Wi-Fi access point and provides a browser-based GUI to calibrate and monitor a
connected accelerometer and magnetometer

After running the script, wait 5 seconds, then connect to the Wi-Fi access point and visit 192.168.1.1

Copyright 2023, Noah Mollerstuen
noah@mollerstuen.com
"""

# Import typing library if available (it is not needed at runtime)
try:
    import typing as t
except ImportError:
    pass
import time
import json
import network
from machine import Pin, I2C
from lsm6dsox import LSM6DSOX
from lib.mlx90393 import MLX90393

from lib.MicroWebSrv.microWebSrv import MicroWebSrv


SSID = 'Wireless Level Prototype'  # Network SSID
KEY = None  # Network key (must be 10 chars)

# Turn on power LED
Pin(26, Pin.OUT).value(False)  # LED ground pin
led_pin = Pin(27, Pin.OUT)
led_pin.value(True)


def read_calibration():
    with open("calibration.json") as f:
        return json.loads(f.read())


def write_calibration(cal):
    with open("calibration.json", "w") as f:
        f.write(json.dumps(cal))


def ws_connect_callback(ws, client):
    print("WS ACCEPT")
    ws.RecvTextCallback = ws_text_callback
    ws.ClosedCallback = ws_closed_callback


def ws_text_callback(ws, msg):
    # Called when a client sends a websocket message
    # Update calibration file as requested
    json_msg = json.loads(msg)
    if json_msg["type"] == "calibration_set":
        calibration[json_msg["key"]] = json_msg["value"]
        write_calibration(calibration)


def ws_closed_callback(ws):
    print("WS CLOSED")


calibration = read_calibration()

# Init wlan module and connect to network
wlan = network.WLAN(network.AP_IF)
wlan.active(True)

if KEY is not None:
    wlan.config(ssid=SSID, key=KEY, security=wlan.WEP, channel=2)
else:
    wlan.config(ssid=SSID)

wlan.ifconfig(("192.168.1.1", "255.255.255.0", "192.168.0.1", "192.168.0.1"))

print(f"AP mode started. SSID: {SSID} IP: {wlan.ifconfig()[0]}")

i2c = I2C(0, scl=Pin(13), sda=Pin(12))

# Initialize IMU
imu = LSM6DSOX(i2c)

# Initialize the magnetometer
magnetometer = MLX90393(i2c)

# Initialize the web server
srv = MicroWebSrv(webPath='static/')
srv.MaxWebSocketRecvLen = 256
srv.WebSocketThreaded = False
srv.AcceptWebSocketCallback = ws_connect_callback

# Wait for the access point to start
time.sleep_ms(5000)

srv.Start()
print("Server started")

while True:
    # Handle incoming requests
    srv.run_once()

    # Read sensor data
    gyro_data = imu.gyro()
    accel_data = imu.accel()
    magnet_data = magnetometer.magnetic

    data = {
        "raw": {
            "accel": accel_data,
            "gyro": gyro_data,
            "magnet": magnet_data
        },
        "calibration": calibration
    }

    srv.broadcast_on_ws(json.dumps(data))
