#!/usr/bin/env python

import RPi.GPIO as GPIO
import subprocess
import time
import logging
from logging.handlers import RotatingFileHandler

GPIO_PIN=3

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Main Loop
if __name__ == '__main__':
    log_formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')
    log_filename = '/var/log/power-button.log'
    log_handler = RotatingFileHandler(log_filename, mode='a', maxBytes=5 * 1024 * 1024,
                                 backupCount=2, encoding=None, delay=0)
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)
    app_log = logging.getLogger('root')
    app_log.setLevel(logging.DEBUG)
    app_log.addHandler(log_handler)

    init_gpio()

    while True:
        count=0
        app_log.info("Waiting for falling edge on pio:"+str(GPIO_PIN))
        GPIO.wait_for_edge(GPIO_PIN, GPIO.FALLING)
        app_log.info("level falling trigged")
        for x in range(0, 20):
            time.sleep(0.01)
            pressed=not GPIO.input(GPIO_PIN)
            app_log.info("#%d"%x + " pressed:"+str(pressed)+ " pressed_count:%d"%count)
            if pressed:
                count+=1
                if count >= 15:
                    app_log.info("Calling shutdown pressed_count:%d"%count)
                    subprocess.call(['shutdown', '-h', 'now'], shell=False)
                    exit(0)
