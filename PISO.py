import RPi.GPIO as GPIO
import time
import sys

shld_pin = 3
clk_pin = 5

data_pin = 22
data_pin_1 = 24

ce_pin = 21
ce_pin_1 = 23

LSB = 0
MSB = 1

def initialize():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(7, GPIO.OUT)
  GPIO.setup(shld_pin, GPIO.OUT)
  GPIO.setup(ce_pin, GPIO.OUT)
  GPIO.setup(ce_pin_1,GPIO.OUT)
  GPIO.setup(clk_pin,GPIO.OUT)
  GPIO.setup(data_pin, GPIO.IN)
  GPIO.setup(data_pin_1, GPIO.IN)
  
  GPIO.output(7, 1)
  GPIO.output(clk_pin, 1)
  GPIO.output(shld_pin, 1)
  return;

def fmat(var):
	ns = ""
	for i in range(0,8):
		num = (var >> i) & 1
		if(num == 0):
			num = "0"
		else:
			num = "1"
		ns += num + " "
	ns = ns[::-1]
	return ns;

def read_shift_regs(data,ce):
  the_shifted = 0
  GPIO.output(shld_pin, 0)
  time.sleep(5/1000000.0)
  GPIO.output(shld_pin, 1)
  time.sleep(5/1000000.0)
  
  GPIO.output(clk_pin, 1)
  GPIO.output(ce, 0)
  
  the_shifted = ShiftIn(data, clk_pin, MSB)
  GPIO.output(ce, 1)
  return the_shifted;

def ShiftIn(data, clk, order):
  value = 0
  for i in range(0,8):
    GPIO.output(clk, 1)
    if(order == 0):
      value |= GPIO.input(data) << i
    else:
      value |= GPIO.input(data) << (7-i)
    GPIO.output(clk, 0)
  return value;
	
initialize()
fh = open('/home/pi/PISO/data.txt',"w")
try:
	while(True):
		val = read_shift_regs(data_pin,ce_pin)
		val1 = read_shift_regs(data_pin_1,ce_pin_1)
		s1 = fmat(val)
		s2 = fmat(val1)
		
		fh.write(s1 + '' + s2 + "\r\n")
		print(s1),
		print"\t",
		print(val),
		print "\t",
		print(s2),
		print "\t",
		print(val1)
		time.sleep(0.5)
except (KeyboardInterrupt, SystemExit):
	print "\nKeyboard interrupt detected. Cleaning up GPIO...",
	GPIO.cleanup()
	fh.close()
	print "Done"
except:
	print "Fatal Error"
	GPIO.cleanup()
	fh.close()
	print "Fix that stupid bug"
