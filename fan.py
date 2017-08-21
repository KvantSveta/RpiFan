import signal
from time import sleep
from datetime import datetime
from threading import Event
from subprocess import check_output

import RPi.GPIO as GPIO


__author__ = "Evgeny Goncharov"

run_service = Event()
run_service.set()


def handler(signum, frame):
    run_service.clear()


signal.signal(signal.SIGTERM, handler)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

RELAY = 20

GPIO.setup(RELAY, GPIO.OUT, initial=GPIO.LOW)

while run_service.is_set():
	temp = check_output(["cat", "/sys/class/thermal/thermal_zone0/temp"])
	temp = temp.decode()
	temp = round(int(temp) / 1000, 1)

    if (6 <= datetime.now().hour < 22) or (temp > 45):
        # relay - off, fan - on
        GPIO.output(RELAY, GPIO.LOW)

    else:
        # relay - on, fan - off
        GPIO.output(RELAY, GPIO.HIGH)

    sleep(60)

GPIO.cleanup(RELAY)
