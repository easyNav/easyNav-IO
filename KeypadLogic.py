import RPi.GPIO as GPIO
import time


class Keypad(object):
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)

		MATRIX=[['1','2','3'],
				['4','5','6'],
				['7','8','9'],
				['*','0','#']]

		#GPIO Pin Numbers

		ROW=[8,10,12,16]
		COL=[15,13,11]
		inputId = [] 
		temp=[]

	def getInput(self):
		for j in range(3):
			GPIO.setup(COL[j], GPIO.OUT)
			GPIO.output(COL[j], 1)    #set output as high


		for i in range(4):
			GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) #input set on high

		try:
			while(True):
				for j in range(3):

					GPIO.output(COL[j], 0)

					for i in range(4):
						if(GPIO.input(ROW[i]) == 0):   # a key is pressed
							print MATRIX[i][j]
							if(MATRIX[i][j] != '#'):			 	#not the end yet
								inputId.append(MATRIX[i][j])
							else:
								print inputId
								temp = inputId
								del inputId[:] #clear buffer
								return temp    #break infinite loop
								

							while(GPIO.input(ROW[i]) == 0):
								pass

					GPIO.output(COL[j], 1)

		except KeyboardInterrupt:
			GPIO.cleanup()
	