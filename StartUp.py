import os


#startup dispatcher
os.system("easyNav-pi-dispatcher")

#startup Nav
os.system("easyNav-pi-nav")

#startup Voice
os.system("sudo python /easyNav-IO/voice.py")

