#for interprocess communication
import smokesignal
from easyNav_pi_dispatcher import DispatcherClient
import json
import speaker 
import KeypadLogic
import multiprocessing


class Notifications(object):

	def __init__(self):
		self.speaker = speaker.newSpeaker()

        #interprocess 
		self.DISPATCHER_PORT = 9002
		self.dispatcherClient = DispatcherClient(port=self.DISPATCHER_PORT)

        ## Attach event listeners
		self.attachEvents(self.speaker)

	def start(self):
		self.dispatcherClient.start()
		
		#run notifier forever
		while(1):
			pass


	def attachEvents(self, mic):
        ## clear all signals
		smokesignal.clear()
		text = ""
		@smokesignal.on('say')
		def onSay(args):
			print "Info from Nav"
			infoFromNav = eval(args.get('payload'))
			print infoFromNav
			infotosay = infoFromNav["text"]
			print infotosay
			print "Info from Nav before Mic"
			mic.say(infotosay)


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

					try:

						self.dispatcherClient.send(9003, "starting", int(strStart))
						self.dispatcherClient.send(9001, "newPath", {"from":int(strStart), "to": int(strEnd)})
					except ValueError:
						self.speaker.say("Error, key in a proper ID")

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


def runVoice(ns):
	voice = Voice()
	voice.start()

def runNotifications(ns):
	notifications = Notifications()
	notifications.start()


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    ns = manager.Namespace()

    p1 = multiprocessing.Process(target=runVoice, args=(ns,))
    p1.start()
    p2 = multiprocessing.Process(target=runNotifications, args=(ns,))
    p2.start()

    while(1):
    	time.sleep(1)

    p1.join()
    p2.join()