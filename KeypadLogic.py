import RPi.GPIO as GPIO
import time


class Keypad(object):
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)

		self.MATRIX=[['1','2','3'],
				['4','5','6'],
				['7','8','9'],
				['*','0','#']]

		#GPIO Pin Numbers

		self.ROW=[8,10,12,16]
		self.COL=[15,13,11]
		self.inputId = [] 
		self.temp=[]
		
		for j in range(3):
			GPIO.setup(self.COL[j], GPIO.OUT)
			GPIO.output(self.COL[j], 1)    #set output as high


		for i in range(4):
			GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) #input set on high

	def getInput(self):

		try:
			while(True):
				for j in range(3):

					GPIO.output(self.COL[j], 0)

					for i in range(4):
						if(GPIO.input(self.ROW[i]) == 0):   # a key is pressed
							print self.MATRIX[i][j]
							if(self.MATRIX[i][j] != '#'):			 	#not the end yet
								self.inputId.append(self.MATRIX[i][j])
							else:
								print self.inputId
								self.temp = self.inputId
								del self.inputId[:] #clear buffer
								return self.temp    #break infinite loop
								

							while(GPIO.input(self.ROW[i]) == 0):
								pass

					GPIO.output(self.COL[j], 1)

		except KeyboardInterrupt:
			GPIO.cleanup()


def runMain():
	keypad = Keypad()
	keypad.getInput()

if __name__ == '__main__':
    runMain()
	