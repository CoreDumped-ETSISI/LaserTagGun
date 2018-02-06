#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import sys
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

def evento_pulsador(channel):
  print("creciente")
  subprocess.Popen(['irsend','SEND_ONCE','/home/pi/lircd.conf','KEY_0'])

GPIO.add_event_detect(17, GPIO.RISING)
GPIO.add_event_callback(17, evento_pulsador)

#time.sleep(1000)
p = subprocess.Popen(["irw"], stdout=subprocess.PIPE)
for line in p.stdout:
  print(line.split()[2])
