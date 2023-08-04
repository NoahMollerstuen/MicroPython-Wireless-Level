# MicroPython-Wireless-Level
MicroPython server for an embedded device in a wireless level prototype

## Hardware
This script is designed to run on an Arduino Nano RP2040 Connect. It uses the onboard IMU to measure pitch and roll, and a MLX90393 magnetometer in I2C mode for comapss heading (the prototype uses [this](https://www.sparkfun.com/products/14571) breakout from Sparkfun). The Arduino can optionally use an LED connected to the A0 and A1 pins to indicate when it is powered on. The prototype is powered by 4 AA batteries.

## Installation
Refer to [this](https://docs.arduino.cc/tutorials/nano-rp2040-connect/rp2040-python-api) page for MicroPython installation instructions. After installing MicroPython on your Arduino, clone this repo and flash it to the Arduino.

## Usage
After deploying the script and resestting the device, wait until the LED turns on, then wait for an additional 5 seconds until a new Wi-Fi network appears. Connect to the Wi-Fi network from any browser and navigate to http://192.168.1.1. It can take 10 to 15 seconds for the page to load. Your device may warn you that the Wi-Fi network has no connection to the internet. This is expected, you should remain connected to the network.

### Magnetometer Calibration
Whenever the device is moved to a new location, the magnetormeter should be calibrated for accurate compass readings. To calibrate the magnetometer, click "Show Compass Calibration" on the browser app. The app will begin plotting magnetomoter data as it is recieved. Rotate the device 360 degrees around three perpendicular axes, one after another (roll, pitch, and yaw). Ideally, you should see three circular plots. When you are satisfied with the plots, click "Calibrate". All the plots should move to be centered at (0, 0). These calibration offsets are stored on the server, so it is not necessary to recalibrate after restarting the device. You can delete these stored offsets remove the effects of calibration by pressing the "Reset Calibration" button.

By default, the heading readings are relative to magnetic North. To measure the heading to geographic North, you must input your local magnetic declination on the calibration page. You can lookup the magnetic declination in your area [here](https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml). If your declination is in the Eastern direction (E) enter it as a positive number. If the declination is in the Western direction (W), enter it as a negative number.

### Tare
If the device is not mounted exactly parallel to the surface whose orientation you wish to measure, some error will be introduced in the measurement. To compensate for this error, you can level the surface using traditional means, then press the "Tare" button on the primary screen of the browser app. This will fix the device's current orientation to 0 degrees, allowing you to easily see whether the device has returned to the same orientation later. To return to the defualt behavior, press "Reset Tare". This tare is not saved when the device is powered off.
