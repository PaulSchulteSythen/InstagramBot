# Program to update the config folder + the programm#
REPOSITORY = "https://raw.githubusercontent.com/PaulSchulteSythen/InstagramBot/master/"

# get system path
import os
path = os.getcwd().replace("\\", "/") + "/"

# files to update
config_files = [REPOSITORY+"config/like_mainpage_xpaths.conf", REPOSITORY+"config/like_xpaths.conf", REPOSITORY+"config/save_xpaths.conf", REPOSITORY+"config/xpaths.conf"]
exe_file = [REPOSITORY+"dist/GUI.exe"]


import requests
import ctypes
# get files and replace old ones
#try:
# replace config files
for file_url in config_files:
	r = requests.get(file_url, allow_redirects=True)
	open(path + "config/" + file_url.split("/")[-1], 'wb').write(r.content)

"""except Exception as e:
	print(e)
	ctypes.windll.user32.MessageBoxW(None, u"Das Update hat nicht funktioniert. Überprüfen Sie die Internetverbindung oder ob das Verzeichnis schreibgeschützt ist.", u"Fehler", 0)
"""