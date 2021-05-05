from concurrent.futures import ThreadPoolExecutor
import time
import RPi.GPIO as GPIO

# GPIO assignments
RED = 17
YELLOW = 27
GREEN = 22


def delay(seconds):
    time.sleep(seconds)
    return True

def init_gpio():
    print('Init GPIO')
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    GPIO.setup(RED, GPIO.OUT) # RED pin set as output
    GPIO.setup(YELLOW, GPIO.OUT) # YELLOW pin set as output
    GPIO.setup(GREEN, GPIO.OUT) # GREEN pin set as output
    return True

def all_off():
    print('All off...')
    GPIO.output(RED, GPIO.HIGH)
    GPIO.output(YELLOW, GPIO.HIGH)
    GPIO.output(GREEN, GPIO.HIGH)
    return True

def clean_gpio():
    all_off()
    GPIO.cleanup()


if __name__ == '__main__':

    init_gpio()
    all_off()


    pool = ThreadPoolExecutor(1)

    try:
        while True:
            print('Start main loop...')

            GPIO.output(RED,GPIO.LOW)
            future=pool.submit(delay(5))
            while future.done() == False:
                print('wait for RED/YELLOW...')
                time.sleep(0.1)

            GPIO.output(YELLOW,GPIO.LOW)
            future=pool.submit(delay(2))
            while future.done() == False:
                print('wait for GREEM...')
                time.sleep(0.1)

            GPIO.output(GREEN,GPIO.LOW)
            GPIO.output(RED, GPIO.HIGH)
            GPIO.output(YELLOW, GPIO.HIGH)
            future=pool.submit(delay(5))
            while future.done() == False:
                print('wait for YELLOW...')
                time.sleep(0.1)

            GPIO.output(GREEN, GPIO.HIGH)
            GPIO.output(YELLOW, GPIO.LOW)
            future=pool.submit(delay(3))
            while future.done() == False:
                print('wait for RED...')
                time.sleep(0.1)

            GPIO.output(YELLOW, GPIO.HIGH)


    except KeyboardInterrupt:
        clean_gpio()
