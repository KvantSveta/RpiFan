import signal
from time import sleep
from datetime import datetime
from threading import Event

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
    if 6 <= datetime.now().hour < 22:
        # relay - off, fan - on
        GPIO.output(RELAY, GPIO.LOW)

    else:
        # relay - on, fan - off
        GPIO.output(RELAY, GPIO.HIGH)

    sleep(60)

GPIO.cleanup(RELAY)
