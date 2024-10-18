import os, sys, io
import M5
from M5 import *
import requests2
import time
from hardware import *
from unit import ENVUnit
import network


http_req = None
i2c0 = None
wlan = None
rgb = None
env4_0 = None


postbody = None
message = None
past_tick = None
env = None
status_code = None
mes = None
now_tick = None
cdeg = None
now = None
hum = None
atmpres = None
read_result_map = None


# Describe this function...
def getenv():
    global postbody, message, past_tick, env, status_code, mes, now_tick, cdeg, now, hum, atmpres, read_result_map, http_req, i2c0, wlan, rgb, env4_0
    past_tick = time.ticks_ms()
    try:
        cdeg = env4_0.read_temperature()
        hum = env4_0.read_humidity()
        atmpres = env4_0.read_pressure()
    except:
        mes = "Read error: ENV4 read error"
        post_error_log(mes)
        i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
        env4_0 = ENVUnit(i2c=i2c0, type=4)

    now = time.localtime()
    env = {"timestamp": now, "sensor_id": "atoms3lite+env4", "temperature": cdeg, "humidity": hum, "pressure": atmpres}
    return env


# Describe this function...
def post_json(postbody):
    global message, past_tick, env, status_code, mes, now_tick, cdeg, now, hum, atmpres, read_result_map, http_req, i2c0, wlan, rgb, env4_0
    try:
        http_req = requests2.post(
            "http://hostname:8000/post-env4",
            json=postbody,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        status_code = http_req.status_code
        if status_code != 200:
            rgb.fill_color(0xFF0000)
    except:
        mes = str("HTTP request error") + str((str(status_code)))
        mes = str(mes) + str(": post-env4")
        post_error_log(mes)

    return status_code


# Describe this function...
def post_error_log(message):
    global postbody, past_tick, env, status_code, mes, now_tick, cdeg, now, hum, atmpres, read_result_map, http_req, i2c0, wlan, rgb, env4_0
    http_req = requests2.post(
        "http://hostname:8000/post-log",
        json={"level": "ERROR", "message": message},
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )


def setup():
    global http_req, i2c0, wlan, rgb, env4_0, past_tick, env, status_code, mes, now_tick, cdeg, now, postbody, hum, atmpres, message, read_result_map

    M5.begin()
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    env4_0 = ENVUnit(i2c=i2c0, type=4)
    wlan = network.WLAN(network.STA_IF)
    wlan.config(reconnects=3)
    wlan.connect("SSID", "PASSWORD")
    rgb = RGB()
    rgb.set_brightness(20)
    rgb.fill_color(0x009900)
    past_tick = time.ticks_ms()


def loop():
    global http_req, i2c0, wlan, rgb, env4_0, past_tick, env, status_code, mes, now_tick, cdeg, now, postbody, hum, atmpres, message, read_result_map
    M5.update()
    now_tick = time.ticks_ms()
    if (time.ticks_diff(now_tick, past_tick)) >= 60000:
        try:
            read_result_map = getenv()
            status_code = post_json(read_result_map)
            if status_code == 200:
                rgb.fill_color(0x009900)
        except:
            rgb.fill_color(0xFF0000)

    if BtnA.wasDoubleClicked():
        try:
            read_result_map = getenv()
            status_code = post_json(read_result_map)
            if status_code == 200:
                rgb.fill_color(0x009900)
        except:
            rgb.fill_color(0xFF0000)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
