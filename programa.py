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
GPIO.output(12, GPIO.HIGH)

last_shot = time.time()
last_shot_r = last_shot
wait_time = 0.3
wait_time_r = 1
print(last_shot)

def evento_pulsador(channel):
    global last_shot
    global wait_time
    global idGun
    new_shot = time.time()
    if (new_shot - last_shot) > wait_time:
        last_shot = new_shot
        print('Shot KEY_' + str(idGun))
        subprocess.Popen(['irsend', 'SEND_ONCE', '/home/pi/lircd.conf', 'KEY_0'])  # Try to send the message for 10ms

GPIO.add_event_detect(17, GPIO.RISING, evento_pulsador)

p = subprocess.Popen(["irw"], stdout=subprocess.PIPE)
for line in p.stdout:
    new_shot = time.time()
    if new_shot - last_shot_r > wait_time_r:
        last_shot_r = new_shot
        shot = line.split()[2]
        idShot = chr(shot[-1])
        payload = {'idGun': idShot, 'idVelt': 0}
        r = requests.post("http://lasertag.coredumped.es/match/shot", data=payload)
        print(r.text)
