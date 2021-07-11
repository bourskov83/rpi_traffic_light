import threading
import time
import RPi.GPIO as GPIO

SCAN_INTERVAL = 0.2
#### GPIO assignments
# OUTPUTs
RED_LIGHT_LIGHT = 11
YELLOW_LIGHT_LIGHT = 13
GREEN_LIGHT_LIGHT = 15
# INPUTs
MODE = 1
MANUAL_CHANGE = 1
RED_LIGHT_BUTTON = 1
YELLOW_LIGHT_BUTTON = 1
GREEN_LIGHT_BUTTON = 1



def init_gpio():
    print('Init GPIO')
    GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme
    GPIO.setup(RED_LIGHT, GPIO.OUT) # RED_LIGHT pin set as output
    GPIO.setup(YELLOW_LIGHT_LIGHT, GPIO.OUT) # YELLOW_LIGHT pin set as output
    GPIO.setup(GREEN_LIGHT_LIGHT, GPIO.OUT) # GREEN_LIGHT pin set as output
    return True

def clean_gpio():
    all_off()
    GPIO.cleanup()


def all_off():
    print('All off...')
    GPIO.output(RED_LIGHT, GPIO.HIGH)
    GPIO.output(YELLOW_LIGHT_LIGHT, GPIO.HIGH)
    GPIO.output(GREEN_LIGHT_LIGHT, GPIO.HIGH)
    return True



def delay():
    global DELAY_END
    DELAY_END = True

def Update_Light(lights):
    for light,state in lights.items():
        if state:
            pass
            GPIO.output(light,GPIO.LOW)
        else:
            pass
            GPIO.output(light,GPIO.HIGH)
        print(f"{light}:{state}")

def Scan_Input(scan_interval):
    global AUTO_MODE
    print("Scan_Input() started")
    while True:
        print("Scanning GPIO and updating global variables")
        time.sleep(scan_interval)

def Start_Delay(amount):
    global DELAY_END
    DELAY_END = False
    t = threading.Timer(amount, delay)
    t.start()


AUTO_MODE = True
DELAY_END = False



# Main loop

if __name__ == '__main__':

    init_gpio()
    all_off()

    scan_thread = threading.Thread(target=Scan_Input, args=(SCAN_INTERVAL,), daemon=True)
    scan_thread.start()

    try:
        while True:

            # Scan input
            # Update global registers

            # AUTO mode
            # change lights with threading.Timer
            while AUTO_MODE:
                Update_Light({'RED_LIGHT':True,'YELLOW_LIGHT':False,'GREEN_LIGHT':False})
                Start_Delay(10)
                while DELAY_END == False and AUTO_MODE:
                    pass
                print("\n")
                Update_Light({'RED_LIGHT':True,'YELLOW_LIGHT':True,'GREEN_LIGHT':False})
                Start_Delay(3)
                while DELAY_END == False and AUTO_MODE:
                    pass
                print("\n")
                Update_Light({'RED_LIGHT':False,'YELLOW_LIGHT':False,'GREEN_LIGHT':True})
                Start_Delay(10)
                while DELAY_END == False and AUTO_MODE:
                    pass
                print("\n")
                Update_Light({'RED_LIGHT':False,'YELLOW_LIGHT':True,'GREEN_LIGHT':False})
                Start_Delay(4)
                while DELAY_END == False and AUTO_MODE:
                    pass

            if not AUTO_MODE:
                print("Manual Mode...")


    except KeyboardInterrupt:
        print("Exit...")
