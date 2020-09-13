import RPi.GPIO as GPIO
import time, os, urllib, urllib2
from RPLCD import CharLCD
import time
import Adafruit_CharLCD as LCD

PERIOD = 15 #seconds
BASE_URL = 'https://api.thingspeak.com/update.json'
KEY = 'DW3WHNUJQL2M1AXI'
# Raspberry Pi pin setup
lcd_rs = 21
lcd_en = 8
lcd_d4 = 23
lcd_d5 = 18
lcd_d6 = 15
lcd_d7 = 14 
lcd_backlight = 4 
# Define LCD column ani9oifgd row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)


trigger_pin = 19
echo_pin = 26

trigger_pin1 = 6
echo_pin1 = 5

counter =0


s1=0
s2=0
GPIO.setmode(GPIO.BCM)

GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

GPIO.setup(trigger_pin1, GPIO.OUT)
GPIO.setup(echo_pin1, GPIO.IN)
def send_data_counter(counter):
data = urllib.urlencode({'api_key': KEY, 'field1': counter})
response = urllib2.urlopen(url=BASE_URL, data=data)
print(response.read())
def send_trigger_pulse():
GPIO.output(trigger_pin,True)
time.sleep(0.0001)
GPIO.output(trigger_pin,False)

def wait_for_echo(value, timeout):
count=timeout
while GPIO.input(echo_pin) != value and count>0:
count = count - 1

def get_distance():
send_trigger_pulse()
wait_for_echo(True,10000)
start = time.time()
wait_for_echo(False,10000)
finish = time.time()
pulse_len = finish - start
distance_cm = pulse_len / 0.000058
return(distance_cm)



def send_trigger_pulse1():
GPIO.output(trigger_pin1,True)
time.sleep(0.0001)
GPIO.output(trigger_pin1,False)

def wait_for_echo1(value, timeout):
count1=timeout
while GPIO.input(echo_pin1) != value and count1>0:
count1 = count1 - 1

def get_distance1():
send_trigger_pulse1()
wait_for_echo1(True,10000)
start1 = time.time()
wait_for_echo1(False,10000)
finish1 = time.time()
pulse_len1 = finish1 - start1
distance_cm1 = pulse_len1/ 0.000058
return(distance_cm1)
while True: 
distance = get_distance()
distance1 = get_distance1()
#print("Distance 1: %f"%distance)
#print("Distance 2: %f"%distance1)
if distance < 4:
s1 = 1
if s2 == 0:
print("entering")
counter = counter+1
print("Counter : %f"%counter)
#counter = counter+1
#print("Counter 1: %f"%counter)
#lcd.clear()
lcd.clear()
lcd.message(str(counter))
send_data_counter(counter)
time.sleep(PERIOD)
s1 = 0
if distance1 < 4:
s2 = 1
if s1 == 0:
print("exiting")
if counter > 0 :
counter = counter -1 
print("Counter : %f"%counter)
#counter1 = counter1+1
#print("Counter 2: %f"%counter1)
#lcd.clear()
lcd.clear()
lcd.message(str(counter))
send_data_counter(counter)
time.sleep(PERIOD)
s2 = 0
