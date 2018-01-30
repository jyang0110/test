import os
import glob
import time
import RPi.GPIO as GPIO
import time
import os.path

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_temp():
    open_button = open("/home/pi/checkbutton.txt")
    read_button = open_button.read()
    get_button = read_button.split(" ")[0]
    print(get_button)
    if (GPIO.input(23) == 0) or get_button == 'True':
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        Engine_check = os.path.isfile("/sys/bus/w1/devices/28-031724d850ff/w1_slave")
        print(Engine_check)
        if Engine_check is True:
            check_file = open("/sys/bus/w1/devices/28-031724d850ff/w1_slave")
            pre_check = check_file.read()
            firstline = pre_check.split("\n")[0]
            checkdata = firstline.split(" ")[11]
            print(checkdata)
        if Engine_check is True and checkdata == 'YES':
            tfile = open("/sys/bus/w1/devices/28-031724d850ff/w1_slave")
            text = tfile.read()
            print(text)
            tfile.close()
            secondline = text.split("\n")[1]
            temperaturedata = secondline.split(" ")[9]
            temp_d = float(temperaturedata[2:])
            temp_d = temp_d / 1000
            if temp_d < 0:
                temp_b = int(temp_d)
                temp_b = ~temp_b
                temp_b += 1
            else:
                temp_b = int(temp_d)
                temp_b = '{0:07b}'.format(temp_b)
            led_a = str(temp_b)
            led_1 = int(led_a[0])
            led_2 = int(led_a[1])
            led_3 = int(led_a[2])
            led_4 = int(led_a[3])
            led_5 = int(led_a[4])
            led_6 = int(led_a[5])
            led_7 = int(led_a[6])
            if led_1 == 1:
                GPIO.output(21, True)
            if led_1 == 0:
                GPIO.output(21, False)
            if led_2 == 1:
                GPIO.output(20, True)
            if led_2 == 0:
                GPIO.output(20, False)
            if led_3 == 1:
                GPIO.output(26, True)
            if led_3 == 0:
                GPIO.output(26, False)
            if led_4 == 1:
                GPIO.output(19, True)
            if led_4 == 0:
                GPIO.output(19, False)
            if led_5 == 1:
                GPIO.output(13, True)
            if led_5 == 0:
                GPIO.output(13, False)
            if led_6 == 1:
                GPIO.output(6, True)
            if led_6 == 0:
                GPIO.output(6, False)
            if led_7 == 1:
                GPIO.output(5, True)
            if led_7 == 0:
                GPIO.output(5, False)
            res = str(temp_d) + "\n"
            with open("/home/pi/datafile.txt", "a") as myfile:
                myfile.write(res)
            return temp_d,temp_b,led_1,led_2,led_3,led_4,led_5,led_6,led_7
        else:
            GPIO.output(21, True)
            GPIO.output(20, True)
            GPIO.output(26, True)
            GPIO.output(19, True)
            GPIO.output(13, True)
            GPIO.output(6, True)
            GPIO.output(5, True)
            time.sleep(1)
            GPIO.output(21, False)
            GPIO.output(20, False)
            GPIO.output(26, False)
            GPIO.output(19, False)
            GPIO.output(13, False)
            GPIO.output(6, False)
            GPIO.output(5, False)
    else:
	print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")

while True:
    print(read_temp())
    time.sleep(0.5)
