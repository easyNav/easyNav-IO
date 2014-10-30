import requests
import json
import logging
import re
from num2words import num2words
import sys



"""
	This module gets the location list from the server and returns them the vocabcompiler
	in a lingustic form

	Numbers are transformed to words and spaces are inserted for vocabulary compilation

	#TODO:
		finding out short forms!! They can't be pronounced ! for e.g. LT has no meaning, COM has meaning, but its hard
"""

class  Locations(object):

#HOST_ADDR = "http://192.249.57.162:1337/"
	HOST_ADDR = "http://localhost:1337/"

	def __init__(self):
		super(Locations, self).__init__()
		
		#TODO: to dameonize
		self.RUN_INTERVAL = 5 
		logging.basicConfig(filename='getLocationLog.log',level=logging.DEBUG)

	def getLoc(self):

		def insert_space(string, integer):
			return string[0:integer] + ' ' + string[integer:]

		def takeOutNumInsertWord(listToUpdate, word, start, end):
			"""
				args:
				listToUpdate
				word: the word to insert
				start: start indice
				end: end indice
			"""	
			del listToUpdate[start:end]
			listToUpdateStr = str(''.join(listToUpdate))
			newStr = listToUpdateStr[0:start] + word + listToUpdateStr[start:]
			listToUpdate = list(newStr)
			return listToUpdate

		def updateLocationsTextFile(locationListForFile):
			locationFile = open( "locations.txt", "w+")
			
			for line in locationListForFile:
				locationFile.write(line)
				locationFile.write('\n')
			locationFile.close()

		def updateSUIDTextFile(SUIDList):
			SUIDFile = open( "SUIDFile.txt", "w+")
			for line in SUIDList:
				SUIDFile.write(line)
				SUIDFile.write('\n')
			SUIDFile.close()

		def updateCoordTextFile(coordList):
			CoordinateFile = open( "CoordinateFile.txt", "w+")
			for line in coordList:
				print line
				CoordinateFile.write(line)
				CoordinateFile.write('\n')
			CoordinateFile.close()
			
		logging.info("Starting to retrieve locations")
		r = requests.get(Locations.HOST_ADDR + "node")
		print r.status_code

		locationList = []
		SUIDList = []
		coordList=[]
		#print r.json()

		for location in r.json():
			strName = str(location['name'])
			SUID = str(location['SUID'])
			loc = str(location['loc'])
			locationList.append(strName.upper())
			SUIDList.append(SUID)
			coordList.append(loc)

		#print locationList
		#print coordList
		testDigit = re.compile("\d+")

		for k, location in enumerate(locationList):
			p = testDigit.finditer(location)
			locList = list(location)   
			stringGrowthAmount = 0

			"""
					Hardcoding here!
			"""
			# #TODO: find way to detect hyphen
			# if "-" in location:
			# 	locationList.pop(k)
			# 	continue

			for l,match in enumerate(p):

				if l > 0:
					start = match.start() + stringGrowthAmount
					end = match.end() + stringGrowthAmount
				else:
					start = match.start()
					end = match.end()


				inWords = str(num2words(int(match.group())).upper())
				locList = takeOutNumInsertWord(locList, inWords, start, end)
				offset = len(inWords) - (end-start)

				#correct start and end indices
				offsetEnd = end + offset
				stringGrowthAmount += offset

				#handle spaces
				if start != 0 and locList[start-1] != " ":
					locList = list(insert_space(''.join(locList), start))
					offsetStart = start + 1 #correct for space offset
					offsetEnd +=1
					stringGrowthAmount +=1

				if offsetEnd != len(locList) and locList[offsetEnd] != " ":
					locList = list(insert_space(''.join(locList), offsetEnd))
					stringGrowthAmount+=1


			locationList.pop(k)
		 	locationList.insert(k, ''.join(locList))

		updateLocationsTextFile(locationList)
		updateSUIDTextFile(SUIDList)
		updateCoordTextFile(coordList)

		return
	
def runMain():

	loc = Locations()
	loc.getLoc()

if __name__ == '__main__':
	runMain()

