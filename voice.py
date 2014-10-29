#for interprocess communication
import smokesignal
from easyNav_pi_dispatcher import DispatcherClient
import json
import speaker 
import KeypadLogic


class Voice(object):
	def __init__(self): 


		self.speaker = speaker.newSpeaker()

        #interprocess 
		self.DISPATCHER_PORT = 9002
		self.dispatcherClient = DispatcherClient(port=self.DISPATCHER_PORT)

		self.inputBuffer =[]

	def presentMenu(self):
		self.speaker.say("Key * 1 # to choose map and level and locations")
		self.speaker.say("Key * 2 # to choose locations")
		self.speaker.say("Key * 3 # to change destination")
		self.speaker.say("Key * 4 # to end")

	def start(self):
		self.dispatcherClient.start()
		#present menu
		#self.presentMenu();

		#keep listening for keypad activity
		print "in start"
		try:
			print "try statrement"
			while(1):
				print "before getInput"
				self.inputBuffer = KeypadLogic.getInput()

				print "in infinite"

				strInput = ''.join(self.inputBuffer)
				print strInput

				if (strInput == '*1'):
					buildingBuf = []
					levelBuff=[]
					startNodeBuff=[]
					endNodeBuff=[]	

					self.speaker.say("Key in building ID")
					buildingBuf = KeypadLogic.getInput()

					self.speaker.say("Key in level ID")
					levelBuff = KeypadLogic.getInput()

					self.speaker.say("Key in start point ID")
					startNodeBuff = KeypadLogic.getInput()

					self.speaker.say("Key in destination ID")
					endNodeBuff = KeypadLogic.getInput()

					del buildingBuf[:]
					del levelBuff[:]
					del startNodeBuff[:]
					del endNodeBuff[:]

				elif (strInput == '*2'):
					startNodeBuff=[]
					endNodeBuff=[]


					self.speaker.say("Key in start point ID")
					startNodeBuff = KeypadLogic.getInput()

					self.speaker.say("Key in destination ID")
					endNodeBuff = KeypadLogic.getInput()

					strStart = ''.join(startNodeBuff)
					strEnd = ''.join(endNodeBuff)

					dispatcherClient.send(9003, "starting", int(strStart))
					dispatcherClient.send(9001, "newPath", {"from":int(strStart), "to": int(strEnd)})

					del startNodeBuff[:]
					del endNodeBuff[:]

				elif (strInput == '*3'):
					self.speaker.say("Stopping previous navigation")

					endNodeBuff=[]

					self.speaker.say("Key in destination ID")
					endNodeBuff = KeypadLogic.getInput()

					del endNodeBuff[:]

				elif (strInput == '*4'):
					self.speaker.say("Goodbye!")

		except:
			pass



def runMain():
	voice = Voice()
	voice.start()

if __name__ == '__main__':
    runMain()