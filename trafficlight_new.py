import threading
import time
import RPi.GPIO as GPIO
import logging

SCAN_INTERVAL = 0.2
#### GPIO assignments
# OUTPUTs
RED_LIGHT = 11
YELLOW_LIGHT = 13
GREEN_LIGHT = 15
# INPUTs
MODE = 12
MANUAL_CHANGE = 24
RED_LIGHT_BUTTON = 16
YELLOW_LIGHT_BUTTON = 18
GREEN_LIGHT_BUTTON = 22

UPDATE_INTERVAL = .1

inputs = [MODE,RED_LIGHT_BUTTON,YELLOW_LIGHT_BUTTON,GREEN_LIGHT_BUTTON,MANUAL_CHANGE]
input_state = {}
output_state = {}

logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(name)s.%(funcName)-15s][%(levelname)-9s]%(filename)s:%(lineno)-4s:%(message)s')
logger.setLevel(logging.DEBUG)

def InputUpdate(channel):
    if GPIO.input(channel):
        logger.debug(f"GPIO {channel}:Off")
        input_state[channel]=False

    else:
        logger.debug(f"GPIO {channel}:On")
        input_state[channel]=True



def init_gpio():
    logger.info('Init GPIO')
    GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme
    GPIO.setup(RED_LIGHT, GPIO.OUT) # RED_LIGHT pin set as output
    GPIO.setup(YELLOW_LIGHT, GPIO.OUT) # YELLOW_LIGHT pin set as output
    GPIO.setup(GREEN_LIGHT, GPIO.OUT) # GREEN_LIGHT pin set as output

    # Inputs
    for input in inputs:
        GPIO.setup(input, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(input, GPIO.BOTH, callback=InputUpdate, bouncetime=200)

        # initialize input_state dict
        InputUpdate(input)

    return True

def clean_gpio():
    all_off()
    GPIO.cleanup()


def all_off():
    global output_state
    logger.info('Set all configured GPIO output to off...')
    GPIO.output(RED_LIGHT, GPIO.HIGH)
    GPIO.output(YELLOW_LIGHT, GPIO.HIGH)
    GPIO.output(GREEN_LIGHT, GPIO.HIGH)
    output_state = {RED_LIGHT:False,YELLOW_LIGHT:False,GREEN_LIGHT:False}
    return True




def Update_Light(lights):
    global output_state
    for light,state in lights.items():
        if state:
            GPIO.output(light,GPIO.LOW)
            output_state[light]=True
        else:
            GPIO.output(light,GPIO.HIGH)
            output_state[light]=False
        logger.debug(f"GPIO {light}: STATE:{state}")


# Main loop

def run():
    last_mode_auto = False
    manual_change = False
    manual_change_last = False
    manual_change_last_state = "RED"
    init_gpio()
    all_off()

    global input_state,output_state,UPDATE_INTERVAL
    try:
        while True:
            while input_state[MODE]:
                logger.debug('In AUTOMODE')
                last_mode_auto = True
                logger.debug('Turn on RED')
                Update_Light({RED_LIGHT:True,YELLOW_LIGHT:False,GREEN_LIGHT:False})
                t_start=time.time()
                logger.debug('Wait for RED/YELLOW')
                while (time.time() <= t_start+10) and input_state[MODE]:
                    time.sleep(UPDATE_INTERVAL)
                if input_state[MODE]:
                    logger.debug('Turn on RED/YELLOW')
                    Update_Light({RED_LIGHT:True,YELLOW_LIGHT:True,GREEN_LIGHT:False})
                    t_start=time.time()
                    logger.debug('Wait for GREEN')
                    while (time.time() <= t_start+3) and input_state[MODE]:
                        time.sleep(UPDATE_INTERVAL)
                if input_state[MODE]:
                    logger.debug('Turn on GREEN')
                    Update_Light({RED_LIGHT:False,YELLOW_LIGHT:False,GREEN_LIGHT:True})
                    t_start=time.time()
                    logger.debug('Wait for YELLOW')

                    while (time.time() <= t_start+10) and input_state[MODE]:
                        time.sleep(UPDATE_INTERVAL)
                if input_state[MODE]:
                    logger.debug('Turn on YELLOW')
                    Update_Light({RED_LIGHT:False,YELLOW_LIGHT:True,GREEN_LIGHT:False})
                    t_start=time.time()
                    logger.debug('Wait for RED')

                    while (time.time() <= t_start+4) and input_state[MODE]:
                        time.sleep(UPDATE_INTERVAL)
                logger.debug(f"Input state: {input_state}")
            if not input_state[MODE]:
                if last_mode_auto == True:
                    logger.info('Starting manual mode')
                    all_off()
                    last_mode_auto = False
                if input_state[MANUAL_CHANGE]:
                    logger.info('Manual change started')
                    manual_change = True
                    manual_change_last = True
                    if manual_change_last_state == "RED":
                        logger.debug('Start RED --> GREEN transition')
                        logger.debug('Turn on RED/YELLOW')
                        Update_Light({RED_LIGHT:True,YELLOW_LIGHT:True,GREEN_LIGHT:False})
                        t_start=time.time()
                        logger.debug('Wait for GREEN')

                        while (time.time() <= t_start+3):
                            time.sleep(UPDATE_INTERVAL)

                        logger.debug('Turn on GREEN')
                        Update_Light({RED_LIGHT:False,YELLOW_LIGHT:False,GREEN_LIGHT:True})
                        manual_change_last_state = "GREEN"

                    elif manual_change_last_state == "GREEN":
                        logger.debug('Start GREEN --> RED transition')
                        logger.debug('Turn on YELLOW')
                        Update_Light({RED_LIGHT:False,YELLOW_LIGHT:True,GREEN_LIGHT:False})
                        t_start=time.time()
                        logger.debug('Wait for RED')
                        while (time.time() <= t_start+4):
                            time.sleep(UPDATE_INTERVAL)
                        logger.debug('Turn on RED')
                        Update_Light({RED_LIGHT:True,YELLOW_LIGHT:False,GREEN_LIGHT:False})



                if input_state[RED_LIGHT_BUTTON] or input_state[YELLOW_LIGHT_BUTTON] or input_state[GREEN_LIGHT_BUTTON]:
                    manual_change = False
                if not manual_change and manual_change_last:
                    logger.info('Manual color selected')
                    manual_change_last = False


                if not manual_change:
                    if  input_state[RED_LIGHT_BUTTON] != output_state[RED_LIGHT]:
                        Update_Light({RED_LIGHT:input_state[RED_LIGHT_BUTTON]})
                    if  input_state[YELLOW_LIGHT_BUTTON] != output_state[YELLOW_LIGHT]:
                        Update_Light({YELLOW_LIGHT:input_state[YELLOW_LIGHT_BUTTON]})
                    if  input_state[GREEN_LIGHT_BUTTON] != output_state[GREEN_LIGHT]:
                        Update_Light({GREEN_LIGHT:input_state[GREEN_LIGHT_BUTTON]})


                time.sleep(UPDATE_INTERVAL)


    except KeyboardInterrupt:
        print("Exit...")
        clean_gpio()

if __name__ == '__main__':
    run()
