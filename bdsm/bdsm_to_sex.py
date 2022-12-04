import subprocess, os, shutil, sys, base64, json
from pathlib import Path

project = Path(__file__).parent.parent

cmpileprms = [
	str(project / 'bdsm' / 'python' / 'bin' / 'python.exe'),
	# 'py',
	'-m',
	'PyInstaller',
	'--noconfirm',
	'--onefile',
	# '--windowed',
	'--console',
	'--icon',
	'E:/!webdesign/cbtool/doubt.ico',
	# add icon file
	# '--add-data', str(project / 'doubt.ico;.'),
	# some critical custom tkinter shit
	# '--add-data', 'C:/Users/DrHax/AppData/Local/Programs/Python/Python310/Lib/site-packages/customtkinter;customtkinter/',
	str(project / 'bdsm' / 'bdsm.py')
]

subprocess.call(cmpileprms)


# move exe
shutil.move(str(project / 'bdsm' / 'dist' / 'bdsm.exe'), str(project / 'bdsm' / 'bdsm.exe'))

# delete shit
shutil.rmtree(str(project / 'bdsm' / 'build'))
shutil.rmtree(str(project / 'bdsm' / 'dist'))
(project / 'bdsm' / 'bdsm.spec').unlink(missing_ok=True)