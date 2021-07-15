import threading
import time
import RPi.GPIO as GPIO

SCAN_INTERVAL = 0.2
#### GPIO assignments
# OUTPUTs
RED_LIGHT = 11
YELLOW_LIGHT = 13
GREEN_LIGHT = 15
# INPUTs
MODE = 12
MANUAL_CHANGE = 31
RED_LIGHT_BUTTON = 16
YELLOW_LIGHT_BUTTON = 18
GREEN_LIGHT_BUTTON = 22

UPDATE_INTERVAL = .1

inputs = [MODE,RED_LIGHT_BUTTON,YELLOW_LIGHT_BUTTON,GREEN_LIGHT_BUTTON]
input_state = {}
output_state = {}
last_mode = False


def InputUpdate(channel):
    if GPIO.input(channel):
        print(f"GPIO {channel}:Off")
        input_state[channel]=False

    else:
        print(f"GPIO {channel}:On")
        input_state[channel]=True

def InputOff(channel):
    print(f"GPIO {channel} is Off")
    input_state[channel]:False



def init_gpio():
    print('Init GPIO')
    GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme
    GPIO.setup(RED_LIGHT, GPIO.OUT) # RED_LIGHT pin set as output
    GPIO.setup(YELLOW_LIGHT, GPIO.OUT) # YELLOW_LIGHT pin set as output
    GPIO.setup(GREEN_LIGHT, GPIO.OUT) # GREEN_LIGHT pin set as output

    # Inputs
    for input in inputs:
        GPIO.setup(input, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(input, GPIO.BOTH, callback=InputUpdate, bouncetime=100)

        # initialize input_state dict
        InputUpdate(input)

    return True

def clean_gpio():
    all_off()
    GPIO.cleanup()


def all_off():
    global output_state
    print('All off...')
    GPIO.output(RED_LIGHT, GPIO.HIGH)
    GPIO.output(YELLOW_LIGHT, GPIO.HIGH)
    GPIO.output(GREEN_LIGHT, GPIO.HIGH)
    output_state = {RED_LIGHT:False,YELLOW_LIGHT:False,GREEN_LIGHT:False}
    return True



def delay():
    global DELAY_END
    DELAY_END = True

def Update_Light(lights):
    global output_state
    for light,state in lights.items():
        if state:
            GPIO.output(light,GPIO.LOW)
            output_state[light:True]
        else:
            GPIO.output(light,GPIO.HIGH)
            output_state[light:False]
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
    t = None
    t = threading.Timer(amount, delay)
    t.start()


DELAY_END = False



# Main loop

if __name__ == '__main__':

    init_gpio()
    all_off()
    AUTO_MODE = input_state.get(MODE)


#    scan_thread = threading.Thread(target=Scan_Input, args=(SCAN_INTERVAL,), daemon=True)
#    scan_thread.start()


    try:
        while True:
            print(input_state)

            # Scan input
            # Update global registers

            # AUTO mode
            # change lights with threading.Timer
            while input_state[MODE]:
                last_mode = True
                Update_Light({RED_LIGHT:True,YELLOW_LIGHT:False,GREEN_LIGHT:False})
                t_start=time.time()
                while (time.time() <= t_start+10) and input_state[MODE]:
                    time.sleep(UPDATE_INTERVAL)
                if input_state[MODE]:
                    Update_Light({RED_LIGHT:True,YELLOW_LIGHT:True,GREEN_LIGHT:False})
                    t_start=time.time()

                    while (time.time() <= t_start+3) and input_state[MODE]:
                        time.sleep(UPDATE_INTERVAL)
                if input_state[MODE]:
                    Update_Light({RED_LIGHT:False,YELLOW_LIGHT:False,GREEN_LIGHT:True})
                    t_start=time.time()

                    print(t_start)
                    while (time.time() <= t_start+10) and input_state[MODE]:
                        time.sleep(UPDATE_INTERVAL)

                if input_state[MODE]:
                    Update_Light({RED_LIGHT:False,YELLOW_LIGHT:True,GREEN_LIGHT:False})
                    t_start=time.time()
                    while (time.time() <= t_start+4) and input_state[MODE]:
                        time.sleep(UPDATE_INTERVAL)
                print(input_state)
            if not input_state[MODE]:
                if last_mode == True:
                    all_off()
                    last_mode = False

                if not input_state[RED_LIGHT_BUTTON] == output_state[RED_LIGHT]:
                    Update_Light({RED_LIGHT:input_state[RED_LIGHT_BUTTON]})
                if not input_state[YELLOW_LIGHT_BUTTON] == output_state[YELLOW_LIGHT]:
                    Update_Light({YELLOW_LIGHT:input_state[YELLOW_LIGHT_BUTTON]})
                if not input_state[GREEN_LIGHT_BUTTON] == output_state[GREEN_LIGHT]:
                    Update_Light({GREEN_LIGHT:input_state[GREEN_LIGHT_BUTTON]})


                time.sleep(.2)


    except KeyboardInterrupt:
        print("Exit...")
        clean_gpio()
