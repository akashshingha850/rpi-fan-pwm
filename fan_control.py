#! /usr/bin/env python3
import RPi.GPIO as GPIO
import time
import signal
import sys

# The Noctua PWM control actually wants 25 kHz (kilo!), see page 6 on:
# https://noctua.at/pub/media/wysiwyg/Noctua_PWM_specifications_white_paper.pdf
# However, the RPi.GPIO library causes high CPU usage when using high
# frequencies - probably because it can currently only do software PWM.
# So we set a lower frequency in the 10s of Hz here. You should expect that
# this value doesn't work very well and adapt it to what works in your setup.
# We will work on the issue and try to use hardware PWM in the future:
PWM_FREQ = 25         # [Hz] PWM frequency #25

FAN_PIN = 14           # BCM pin used to drive PWM fan
WAIT_TIME = 2           # [s] Time to wait between each refresh

OFF_TEMP = 60           # [°C] temperature below which to stop the fan
MIN_TEMP = 65           # [°C] temperature above which to start the fan
MAX_TEMP = 80           # [°C] temperature at which to operate at max fan speed
FAN_LOW = 10
FAN_HIGH = 100
FAN_OFF = 0
FAN_MAX = 100
FAN_GAIN = float(FAN_HIGH - FAN_LOW) / float(MAX_TEMP - MIN_TEMP)

FAN_STATE= 0 #to resolve the speed display in the standby 

def getCpuTemperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return float(f.read()) / 1000
        


def handleFanSpeed(fan, temperature):
    global fan_speed
    global FAN_STATE

    if temperature > MIN_TEMP:  #FAN START
        delta = min(temperature, MAX_TEMP) - MIN_TEMP
        fan_speed = FAN_LOW + delta * FAN_GAIN
        fan.start(fan_speed)
        FAN_STATE = 1
        print(f"Temperature: {temperature:.2f}, Fan Speed: {fan_speed:.2f}") #Fan Start

    elif temperature < OFF_TEMP:  #FAN STOP
        fan.start(FAN_OFF)
        fan_speed=0
        FAN_STATE = 0
        print(f"Temperature: {temperature:.2f}, Fan Speed: {fan_speed:.2f}") #Fan Off
        
    else:						#STANDBY
        if (FAN_STATE==1):
            fan_speed= FAN_LOW
        else:
            fan_speed= 0
        
        print(f"Temperature: {temperature:.2f}, Fan Speed: {fan_speed:.2f}") #Standby


try:
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
    fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
    while True:
        handleFanSpeed(fan, getCpuTemperature())
        time.sleep(WAIT_TIME)

except KeyboardInterrupt:
    pass

finally:
    print("exited")
    fan.start(FAN_OFF)
    #GPIO.cleanup()
