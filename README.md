# OnAir

This project modifies an existing "OnAir" sign to work with a Raspberry Pi Pico W. With this setup, you can control the sign remotely over WiFi through a web page.

## Components Needed
- OnAir sign or its equivalent
- Raspberry Pi Pico W
- Wires

## Build

Quick and dirty - connecting GPIO (3.3v) & GND to LED strip.

![onair](https://github.com/user-attachments/assets/416dcb22-204b-416d-9ef9-6adf0eca72aa)

## Setup

Ensure you replace the `ssid` & `password` fields your wifi settings.

```python
ssid='ENTER_WIFI_SSID'
password='ENTER_WIFI_PASSWORD'
```
