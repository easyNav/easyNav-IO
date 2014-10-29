import subprocess

# #startup dispatcher
#output = open('dispatcher.txt', 'w'
dispatcher = subprocess.Popen('easyNav-pi-dispatcher > dispatcher.txt 2>&1', shell=True)
#dispatcher.communicate()[0]

# #startup Nav
nav = subprocess.Popen('easyNav-pi-nav > dispatcher.txt 2>&1', shell=True)


#start voice
#output = open('voice.txt', 'w')
voice = subprocess.Popen('sudo python voice.py > voice.txt 2>&1', shell=True)

#voice.communicate()

#startup Voice
#os.system("sudo python /easyNav-IO/voice.py")
