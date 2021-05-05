import RPi.GPIO as GPIO
import time

RED = 17
YELLOW = 27
GREEN = 22
WAIT = 1

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(RED, GPIO.OUT) # LED pin set as output
GPIO.setup(YELLOW, GPIO.OUT) # PWM pin set as output
GPIO.setup(GREEN, GPIO.OUT) # PWM pin set as output

# Initial state for LEDs:
GPIO.output(RED, GPIO.HIGH)
GPIO.output(YELLOW, GPIO.HIGH)
GPIO.output(GREEN, GPIO.HIGH)


try:
    while True:
        GPIO.output(RED,GPIO.LOW)
        time.sleep(WAIT)
        GPIO.output(YELLOW,GPIO.LOW)
        GPIO.output(RED, GPIO.HIGH)
        time.sleep(WAIT)
        GPIO.output(YELLOW, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.LOW)
        time.sleep(WAIT)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(YELLOW, GPIO.LOW)
        time.sleep(WAIT)
        GPIO.output(YELLOW, GPIO.HIGH)
        GPIO.output(RED,GPIO.LOW)
        time.sleep(WAIT)
except KeyboardInterrupt:
    GPIO.output(RED, GPIO.HIGH)
    GPIO.output(YELLOW, GPIO.HIGH)
    GPIO.output(GREEN, GPIO.HIGH)
    GPIO.cleanup() 
      
