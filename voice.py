#for interprocess communication
import smokesignal
from easyNav_pi_dispatcher import DispatcherClient
import json
import speaker 
import KeypadLogic


class Voice(object):
	def __init__(self): 

		#get instance of keypad 
		keypad = Keypad()

		self.speaker = speaker.newSpeaker()

        #interprocess 
		self.DISPATCHER_PORT = 9002
		self.dispatcherClient = DispatcherClient(port=self.DISPATCHER_PORT)

		self.inputBuffer =[]

	def presentMenu():
		self.speaker.say("Key * 1 # to choose map and level and locations")
		self.speaker.say("Key * 2 # to choose locations")
		self.speaker,say("Key * 3 # change destination")
		self.speaker.say("Key * 4 # to end")

	def start(self):
		
		#present menu
		presentMenu();

		#keep listening for keypad activity

		try:
			while(1):
				self.inputBuffer = keypad.getInput()

				strInput = ''.join(self.inputBuffer)

				if (strInput == '*1'):
					buildingBuf = []
					levelBuff=[]
					startNodeBuff=[]
					endNodeBuff=[]

					self.speaker.say("Key in building ID")
					buildingBuf = keypad.getInput()

					self.speaker.say("Key in level ID")
					levelBuff = keypad.getInput()

					self.speaker.say("Key in start point ID")
					startNodeBuff = keypad.getInput()

					self.speaker.say("Key in destination ID")
					endNodeBuff = keypad.getInput()

					del buildingBuf[:]
					del levelBuff[:]
					del startNodeBuff[:]
					del endNodeBuff[:]

				elif (strInput == '*2'):
					startNodeBuff=[]
					endNodeBuff=[]


					self.speaker.say("Key in start point ID")
					startNodeBuff = keypad.getInput()

					self.speaker.say("Key in destination ID")
					endNodeBuff = keypad.getInput()

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
				endNodeBuff = keypad.getInput()

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