#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import sys
import subprocess
import requests

idGun = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(12, GPIO.OUT)


def evento_pulsador(channel):
    print("Shot")
    subprocess.Popen(['irsend', 'SEND_ONCE', '/home/pi/lircd.conf', 'KEY_' + idGun])  # Try to send the message for 10ms
    GPIO.output(12, GPIO.LOW)
    time.sleep(300)
    GPIO.output(12, GPIO.HIGH)


GPIO.add_event_detect(17, GPIO.RISING)
GPIO.add_event_callback(17, evento_pulsador)

p = subprocess.Popen(["irw"], stdout=subprocess.PIPE)
for line in p.stdout:
    shot = line.split()[2]
    print(shot)
    idShot = shot[-1]
    payload = {'idGun': idShot, 'idVelt': 0}
    r = requests.post("http://lasertag.coredumped.es/match/shot", data=payload)
    print(r.text)
