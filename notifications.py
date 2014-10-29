#for interprocess communication
import smokesignal
from easyNav_pi_dispatcher import DispatcherClient
import json
import speaker 

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


def runMain():

	notifications = Notifications()
 	notifications.start()

if __name__ == '__main__':
	runMain()
