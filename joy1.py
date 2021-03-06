
from RPLCD import CharLCD
import RPi.GPIO as GPIO
import time
import xbox
import serial

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(15,GPIO.IN)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)

lcd = CharLCD(cols = 16, rows = 2, pin_rs = 15 , pin_e = 11, pins_data=[22,12,18,16])

lcd.write_string(u"Ready to RACE!!!")

serial = serial.Serial(
	port = '/dev/ttyUSB0',
	baudrate = 38400,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
	)

GAMEPADBUTTONA = 0
GAMEPADBUTTONB = 0
GAMEPADLEFTX   = 0
GAMEPADLEFTY   = 0
GAMEPADRIGHTX = 0
GAMEPADRIGHTY = 0
GAMEPADTRIGGERLEFT = 0
GAMEPADTRIGGERRIGHT = 0

START_BYTE = 227

PA = 0
PB = 0
PX = 0
PY = 0
PSTART = 0
PBACK = 0	

#Defining bit positions to send through UART
#for GAMEPADBUTTONB
BUTTON_X 		= 0
BUTTON_Y		= 1
BUTTON_A		= 2
BUTTON_B		= 3
BUTTON_BACK		= 4
BUTTON_START		= 5
BUTTON_RIGHTSHOULDER	= 6
#for GAMEPADBUTTONA
BUTTON_LEFTSHOULDER	= 0
BUTTON_RIGHTSTICK	= 1
BUTTON_LEFTSTICK	= 2
BUTTON_DPADUP		= 3
BUTTON_DPADDOWN		= 4
BUTTON_DPADLEFT		= 5
BUTTON_DPADRIGHT	= 6

joy = xbox.Joystick()

while True:
	if joy.connected:
		GAMEPADLEFTX =  ((1+joy.leftX())*100)
		GAMEPADLEFTY = ((1+joy.leftY())*100)
		GAMEPADRIGHTX = ((1+joy.rightX())*100)
		GAMEPADRIGHTY = ((1+joy.rightY())*100)
		GAMEPADTRIGGERRIGHT = (joy.rightTrigger()*100)
		GAMEPADTRIGGERLEFT = (joy.leftTrigger()*100)
		
		if joy.A() :
			if PA == 0:		
				GAMEPADBUTTONB |= (1<<BUTTON_A)
				PA = 1
		else:
			PA = 0
		if joy.B() :
			if PB == 0:		
				GAMEPADBUTTONB |= (1<<BUTTON_B)
				PB = 1
		else:
			PB = 0
		if joy.X() :
			if PX == 0:		
				GAMEPADBUTTONB |= (1<<BUTTON_X)
				PX = 1
		else:
			PX = 0
		if joy.Y() :
			if PY == 0:		
				GAMEPADBUTTONB |= (1<<BUTTON_Y)
				PY = 1
		else:
			PY = 0
		if joy.BACK() :
			if PBACK == 0:		
				GAMEPADBUTTONB |= (1<<BUTTON_BACK)
				PBACK = 1
		else:
			PBACK = 0
		if joy.START() :
			if PSTART == 0:		
				GAMEPADBUTTONB |= (1<<BUTTON_START)
				PSTART = 1
		else:
			PSTART = 0
		if joy.rightBumper():
			GAMEPADBUTTONB |= (1<<BUTTON_RIGHTSHOULDER)
			#print"rt"
		if joy.leftBumper():
			GAMEPADBUTTONA |= (1<<BUTTON_LEFTSHOULDER)
			#print"lt"
		if joy.rightThumbstick():
			GAMEPADBUTTONA |= (1<<BUTTON_RIGHTSTICK)
			#print"rst"
		if joy.leftThumbstick():
			GAMEPADBUTTONA |= (1<<BUTTON_LEFTSTICK)
			#print"lst"
		if joy.dpadUp():
			GAMEPADBUTTONA |= (1<<BUTTON_DPADUP)
			#print"up"
		if joy.dpadDown():
			GAMEPADBUTTONA |= (1<<BUTTON_DPADDOWN)
			#print"down"
		if joy.dpadLeft():
			GAMEPADBUTTONA |= (1<<BUTTON_DPADLEFT)
			#print"left"
		if joy.dpadRight():
			GAMEPADBUTTONA |= (1<<BUTTON_DPADRIGHT)
			#print"right"
	else:
		GAMEPADLEFTX = 100
		GAMEPADLEFTY = 100
		GAMEPADRIGHTX = 100
		GAMEPADRIGHTY = 100
		GAMEPADTRIGGERLEFT = 100
		GAMEPADTRIGGERRRIGHT = 100
	
	serial.write(chr(int(START_BYTE)))
	time.sleep(0.001)
	serial.write(chr(int(GAMEPADBUTTONA)))
	time.sleep(0.001)
	serial.write(chr(int(GAMEPADBUTTONB)))
	time.sleep(0.001)
	serial.write(chr(int(GAMEPADLEFTX)))
	time.sleep(0.001)
	serial.write(chr(int(GAMEPADLEFTY)))
	time.sleep(0.001)
	serial.write(chr(int(GAMEPADRIGHTX)))
	time.sleep(0.001)
	serial.write(chr(int(GAMEPADRIGHTY)))
	time.sleep(0.001)
	serial.write(chr(int(GAMEPADTRIGGERLEFT)))
	time.sleep(0.001)
	serial.write(chr(int(GAMEPADTRIGGERRIGHT)))
	time.sleep(0.001)
	

	
	GAMEPADBUTTONA = 0
	GAMEPADBUTTONB = 0
	time.sleep(0.01)
	
