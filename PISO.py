# import modules
import RPi.GPIO as GPIO
import time
import sys

# pin names
data_pin = 16
shld_pin = 11
clk_pin = 13
ce_pin = 15
LSB = 0
MSB = 1

# setup pins
def initialize():
  GPIO.setmode(GPIO.BOARD)
  
  GPIO.setup(shld_pin, GPIO.OUT)
  GPIO.setup(ce_pin, GPIO.OUT)
  GPIO.setup(clk_pin,GPIO.OUT)
  GPIO.setup(data_pin, GPIO.IN)
  
  GPIO.output(clk_pin, 1)
  GPIO.output(shld_pin, 1)
  return;

def read_shift_regs():
  the_shifted = 0
  GPIO.output(shld_pin, 0)
  time.sleep(5/1000000.0)
  GPIO.output(shld_pin, 1)
  time.sleep(5/1000000.0)
  
  GPIO.output(clk_pin, 1)
  GPIO.output(ce_pin, 0)
  
  the_shifted = ShiftIn(data_pin, clk_pin, MSB)
  GPIO.output(ce_pin, 1)
  return the_shifted;

def ShiftIn(data, clk, order):
  value = 0
  for i in range(0,8):
    GPIO.output(clk, 1)
    if(order == 0):
      value = value or (GPIO.input(data) << i)
    else:
      value = value or (GPIO.input(data) << (7-i))
    GPIO.output(clk, 0)
  return value;

def display_byte(x):
  y = 0
  for i in range(0,8):
    y = x >> i and 1
    print(bin(y))

initialize()
while(True):
  val = read_shift_regs()
  print "ABCDEFGH: "
  display_byte(val)
  time.sleep(1)
GPIO.cleanup()