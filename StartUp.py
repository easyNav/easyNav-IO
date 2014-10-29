import subprocess

#startup dispatcher
with open('dispatcher.txt', 'w') as output:
    dispatcher = subprocess.Popen('easyNav-pi-dispatcher', stdout=output)
    #dispatcher.communicate()

#startup Nav
with open('navigation.txt', 'w') as output:
    nav = subprocess.Popen('easyNav-pi-nav', stdout=output)
    #nav.communicate()

#start voice
with open('voice.txt', 'w') as output:
    voice = subprocess.Popen(['sudo', 'python' ,'/home/pi/repos/easyNav-IO/voice.py'], stdout=output)
    #voice.communicate()

#startup Voice
#os.system("sudo python /easyNav-IO/voice.py")

