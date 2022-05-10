from base64 import decode
import sys
import serial
import os
import threading
import queue
import time

COMMAND_CHECK_STATE = "PWR?\n"
COMMAND_POW_ON = "PWR ON\n"
COMMAND_POW_OFF = "PWR OFF\n"

STATE_STANDBY = "Standby Mode"
STATE_LASER_ON = "Laser ON"

CURR_DIR = os.path.split(os.path.realpath(__file__))[0]

def read_input(inputQueue, fd):
    while (True):
        inputQueue.put(fd.read().decode("utf-8"))

def get_state(serialFd, CMD):
    serialFd.write(CMD)
    while True:
        input_waiting_size = serialFd.inWaiting()
        if input_waiting_size > 0:
            return serialFd.read(input_waiting_size).decode("UTF-8")

def main():
    serial_device_list = os.popen("python "+ CURR_DIR + "/../tools/find_serial_com.py --des Arduino").read().split(' ')
    if(serial_device_list is None or len(serial_device_list[0].strip()) == 0):
        print("Error has no projector")
        sys.exit(2)

    inputQueue = queue.Queue()
    serialFd = serial.Serial(serial_device_list[0].strip(), 9600, timeout=60)

    inputThread = threading.Thread(target=read_input, args=(inputQueue, serialFd), daemon=True)
    inputThread.start()
    time.sleep(2) # Arduino 需要近2s时间重新启动

    buffer = ''
    serialFd.write(COMMAND_CHECK_STATE.encode())
    while(True):
        buffer = buffer + inputQueue.get()
        if(buffer.endswith(':')):
            if(STATE_LASER_ON in buffer):
                print("OK")
                break
            elif(STATE_STANDBY in buffer):
                print("Processing Standby weak up")
                get_state(serialFd, COMMAND_POW_ON.encode())
                time.sleep(2)
                serialFd.write(COMMAND_CHECK_STATE.encode())


if (__name__ == '__main__'):
    main()