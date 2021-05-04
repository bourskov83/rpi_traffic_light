import RPi.GPIO as GPIO
import time

RED = 17
YELLOW = 27
GREEN = 22
WAIT = 10

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
        time.sleep(3)
        GPIO.output(GREEN,GPIO.LOW)
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(YELLOW, GPIO.HIGH)
        time.sleep(WAIT)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(YELLOW, GPIO.LOW)
        time.sleep(5)
        GPIO.output(YELLOW, GPIO.HIGH)
        GPIO.output(RED,GPIO.LOW)
except KeyboardInterrupt:
    GPIO.output(RED, GPIO.HIGH)
    GPIO.output(YELLOW, GPIO.HIGH)
    GPIO.output(GREEN, GPIO.HIGH)
    GPIO.cleanup() 
      
