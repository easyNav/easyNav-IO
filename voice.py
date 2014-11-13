#for interprocess communication
import smokesignal
from easyNav_pi_dispatcher import DispatcherClient
import json
import speaker 
import KeypadLogic
import multiprocessing
import time
import GetLocations
import requests

import os


class Notifications(object):

	def __init__(self):
		self.speaker = speaker.newSpeaker()

  #       #interprocess 
		self.DISPATCHER_PORT = 9002
		self.dispatcherClient = DispatcherClient(port=self.DISPATCHER_PORT)

		## For collision detection: lock navigation until ready
		self.collisionLocked = False
		self.obstacle = None
		self.OngoingNav = 0
		self.cruncherAlert = 0

		self.infotosay =None
		self.cruncherInfotosay=""
		## Attach event listeners
		self.attachEvents(self.speaker)


	def attachEvents(self, mic):
		## clear all signals
		smokesignal.clear()
		text = ""
		@smokesignal.on('say')
		def onSay(args):
			print "Info from Nav"
			infoFromNav = eval(args.get('payload'))
			print infoFromNav
			self.infotosay = infoFromNav["text"]
			if(self.infotosay == 'Retrieved new path.'):
				self.OngoingNav = 1
			if(self.infotosay == 'Destination reached!'):
				self.OngoingNav = 0

			print self.infotosay

		@smokesignal.on('cruncherAlert')
		def onSay(args):
			print "Info from Nav"
			if(self.OngoingNav == 1):
				os.system("sudo pkill -SIGTERM -f \"aplay\" ")

			infoFromCruncher = eval(args.get('payload'))
			print infoFromCruncher
			self.cruncherInfotosay = infoFromCruncher["text"]
			self.cruncherAlert = 1

			print self.cruncherInfotosay


		@smokesignal.on('obstacle')
		def onObstacle(args):
			response = int(json.loads(args.get('payload')).get('status'))
			if (response == 0):
				self.obstacle = None
				return
			elif (response == 1):
				self.obstacle = 'FRONT'
				self.collisionLocked = True
			elif (response == 2):
				self.obstacle = 'LEFT'
				self.collisionLocked = True
			elif (response == 3):
				self.obstacle = 'RIGHT'
				self.collisionLocked = True

			# If collision, set to true
			if(self.OngoingNav==1 and not self.collisionLocked):
				os.system("sudo pkill -SIGTERM -f \"aplay\" ")
			#self.collisionLocked = True

	def start(self):
		self.dispatcherClient.start()
		
		#run notifier forever

		while(1):
			try:
				regis = ns.sem

				## Collision detection first
				if (self.collisionLocked and self.OngoingNav == 1 and regis == 0):
					if (self.obstacle == None):
						# Unlock collisionLocked
						self.speaker.say('Obstacle cleared.  Move forward!')
						self.collisionLocked = False


					elif (self.obstacle == 'FRONT'):
						self.speaker.say('Obstacle ahead.  Turn 45 degrees left or right!')

					elif (self.obstacle == 'LEFT'):
						self.speaker.say('Obstacle on the left!')

					elif (self.obstacle == 'RIGHT'):
						self.speaker.say('Obstacle on the right!')
				elif(self.cruncherAlert == 1 and self.OngoingNav == 1 and regis == 0):

					self.speaker.say(self.cruncherInfotosay)
					self.cruncherAlert=0
					self.cruncherInfotosay=None

				else: 
					if(self.infotosay != None and regis == 0):
						self.speaker.say(self.infotosay)
						self.infotosay=None
			except:
				pass

			time.sleep(0.1)

	
class Voice(object):

	HOST_ADDR = "http://localhost:1337/"
	def __init__(self): 

		self.speaker = speaker.newSpeaker()

        #interprocess 
		self.DISPATCHER_PORT = 9002
		self.dispatcherClient = DispatcherClient(port=self.DISPATCHER_PORT)

		self.inputBuffer =[]

		#update locations
		# self.getLocation = GetLocations.Locations()
		# self.getLocation.getLoc()

	def presentMenu(self):
		self.speaker.say("Key * 1 # to choose map and level and locations")
		self.speaker.say("Key * 2 # to choose locations")
		self.speaker.say("Key * 3 # to change destination")
		self.speaker.say("Key * 4 # to end")

	def getLocations(self):
		#get a list of locations
		filename = "locations.txt"
		locationFile = open(filename, "r")
		print "Opened file!!"

		locations = []
		for line in locationFile.readlines():
			line = line.replace("\n", "")
			locations.append(line)
		print locations
		return locations

	def getCoord(self, index):
		filename = "CoordinateFile.txt"
		CoordinateFile = open(filename, "r")
		ctr = 0
		startCoord = "" 

		for line in CoordinateFile.readlines():
			if ctr == index:
				line = line.replace("\n", "")
				startCoord = line

			ctr+=1

		return startCoord

	def getSUIDIndex(self, SUID):
		print "in method"
		filename = "SUIDFile.txt"

		SUIDFile = open(filename, "r")
		print "Opened file"
		index = 0

		for line in SUIDFile.readlines():
			line = line.replace("\n", "")
			print line
			if int(line) == SUID:
				return index
			ctr+=1

		return -1

	def isCancel(self, inputVal):
		if(inputVal == '999'):
			self.speaker.say("Cancelling operation")
			return True
		return False

	def start(self):
		self.dispatcherClient.start()
		#present menu
		#self.presentMenu();

		#keep listening for keypad activity

		while(1):
			try:
				self.inputBuffer = KeypadLogic.getInput(self.speaker)


				strInput = ''.join(self.inputBuffer)
				print strInput

				if (strInput == '*1'):

					startBuildingBuf = []
					startLevelBuff=[]
					startNodeBuff=[]

					endBuildingBuf = []
					endLevelBuff=[]
					endNodeBuff=[]


					self.speaker.say("Key in start building ID, one for com one, two for com two")
					startBuildingBuf = KeypadLogic.getInput(self.speaker)
					strStartBuildingID = ''.join(startBuildingBuf)
					
					if(self.isCancel(strStartBuildingID)):
						continue
					else:
						self.speaker.say("you have chosen building " + strStartBuildingID)


					self.speaker.say("Key in start level ID, zero is basement.")
					startLevelBuff = KeypadLogic.getInput(self.speaker)
					strStartLevelID = ''.join(startLevelBuff)

					if(self.isCancel(strStartLevelID)):
						continue
					else:
						self.speaker.say("you have entered level " + strStartLevelID)


					self.speaker.say("Key in start node ID")
					startNodeBuff = KeypadLogic.getInput(self.speaker)
					strStartNodeID = ''.join(startNodeBuff)
					if(self.isCancel(strStartNodeID)):
						continue
					else:
						self.speaker.say("you have entered start node " + strStartNodeID)


					self.speaker.say("Key in destination building ID ")
					endBuildingBuf = KeypadLogic.getInput(self.speaker)
					strEndBuildingID = ''.join(endBuildingBuf)
					if(self.isCancel(strEndBuildingID)):
						continue
					else:
						self.speaker.say("you have entered building " + strEndBuildingID)

					self.speaker.say("Key in destination level ID")
					endLevelBuff = KeypadLogic.getInput(self.speaker)
					strEndLevelID = ''.join(endLevelBuff)
					if(self.isCancel(strEndLevelID)):
						continue
					else:
						self.speaker.say("you have entered level " + strEndLevelID)

					self.speaker.say("Key in destination node ID")
					endNodeBuff = KeypadLogic.getInput(self.speaker)
					strEndNodeID = ''.join(endNodeBuff)
					if(self.isCancel(strEndNodeID)):
						continue
					else:
						self.speaker.say("you have entered destination node " + strEndNodeID)


					#construct start point SUid
					strStartSUID = strStartBuildingID+strStartLevelID+strStartNodeID
					#construct dest SUid
					strEndSUID = strEndBuildingID+strEndLevelID+strEndNodeID

					try:

						startSUID = int(strStartSUID)
						endSUID = int(strEndSUID)
						print startSUID
						print endSUID
						print "not int problem"
						#get coord
						r = requests.get(Voice.HOST_ADDR + "node/?SUID=" + strStartSUID)	
						print r
						for location in r.json():
							print location
							startCoord = location['loc']
							print startCoord

						self.dispatcherClient.send(9003, "starting", eval(startCoord))
						self.dispatcherClient.send(9001, "newPath", {"from":startSUID, "to": endSUID})
						self.speaker.say("Routing!")

					except:
						self.speaker.say("Invalid ID")


				
					#find builiding map and get coordinates


				elif (strInput == '*2'):
					print "note"
					startNodeBuff=[]
					endNodeBuff=[]

					self.speaker.say("Key in start point ID")
					startNodeBuff = KeypadLogic.getInput(self.speaker)
					strStart = ''.join(startNodeBuff)
					self.speaker.say("you have entered " + strStart)
					print strStart

					self.speaker.say("Key in destination ID")
					endNodeBuff = KeypadLogic.getInput(self.speaker)
					strEnd = ''.join(endNodeBuff)
					self.speaker.say("you have entered " + strEnd)

					try:

						startSUID = int(strStart)
						endSUID = int(strEnd)
						print startSUID
						print endSUID

						#get coord
						r = requests.get(Voice.HOST_ADDR + "node/?SUID=" + strStart)	
						print r

						for location in r.json():
							print location
							startCoord = location['loc']
							print startCoord

						self.dispatcherClient.send(9003, "starting", eval(startCoord))
						self.dispatcherClient.send(9001, "newPath", {"from":startSUID, "to": endSUID})
						self.speaker.say("Routing!")

					except:
						self.speaker.say("Invalid ID")


				elif (strInput == '*333'):
					self.speaker.say("Restarting Nav and Voice")
					os.system("sudo pkill -SIGTERM -f \"nav\"")
					os.system("sudo pkill -SIGTERM -f \"voice\"")

					

				elif (strInput == '*4'):
					self.speaker.say("Ending EasyNav, Are you sure?")
					self.speaker.say("Key in 1 to confirm, 2 to cancel")

					option = KeypadLogic.getInput(self.speaker)
					strOption = ''.join(option)
					try:
						if(strOption == '1'):
							self.speaker.say("Hope you had a good journey!")
							self.speaker.say("Ending all processes, Please wait")
							time.sleep(1)
							self.speaker.say("Please remember to switch off the shoe and bag switches...GoodBye")
							
							os.system("sudo pkill -SIGTERM -f \"node\" ")
							time.sleep(1)
							os.system("sudo sh shutdown.sh")
						else:
							self.speaker.say("Cancelling")

					except ValueError:
						self.speaker.say("Error, key in a proper ID")


					#troubleshooting commands
				elif (strInput == "*444"):
					#lock speech mechanism
					ns.sem = 1 
					self.speaker.say("Finding i p")
					os.system("ifconfig wlan0 | grep inet  > myIp.txt")
					ipFound = False

					with open("myIp.txt") as IPText:
						for line in IPText:
							if "inet" in line:
								ipFound=True
								print line
								lineDic = line.split(" ")
								for word in lineDic:
									print word
									if "addr" in word:
										print "here"
										ipAddr = word.replace("addr:", "")
										self.speaker.say("The I P is " + ipAddr)
										print word

					if(not ipFound):
						self.speaker.say("No i p assigned")

					#unlock speech mechanism
					ns.sem = 0 
			except:
				pass

			time.sleep(0.1)
	

def runVoice(ns):
	voice = Voice()
	voice.start()

def runNotifications(ns):
	notifications = Notifications()
	notifications.start()


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    ns = manager.Namespace()
    ns.sem = 0 

    p1 = multiprocessing.Process(target=runVoice, args=(ns,))
    p1.start()
    p2 = multiprocessing.Process(target=runNotifications, args=(ns,))
    p2.start()

    while(1):
    	time.sleep(1)

    p1.join()
    p2.join()