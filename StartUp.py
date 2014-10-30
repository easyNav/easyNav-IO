import subprocess

# #startup dispatcher
dispatcher = subprocess.Popen('easyNav-pi-dispatcher > dispatcher.txt 2>&1', shell=True)

# #startup Nav
nav = subprocess.Popen('easyNav-pi-nav > navigation.txt 2>&1', shell=True)

voice = subprocess.Popen('sudo python /home/pi/repos/easyNav-IO/voice.py > voice.txt 2>&1', shell=True)

serial = subprocess.Popen('sudo python /home/pi/repos/easyNav-serial/sprotpy/serialmod.py > serial.txt 2>&1' , shell=True)

alert = subprocess.Popen('sudo python /home/pi/repos/easyNav-serial/sprotpy/alert.py > alert.txt 2>&1', shell=True)

cruncher = subprocess.Popen('sudo python /home/pi/repos/easyNav-gears2/Cruncher/cruncher.py pi > cruncher.txt 2>&1', shell=True)






