import subprocess, os, shutil, sys, base64, json
from pathlib import Path

project = Path(__file__).parent.parent

freshstruct = Path(r'E:\!webdesign\bootlegger\bootlegger\lightstruct.py')

if freshstruct.is_file():
	shutil.copyfile(str(freshstruct), str(project / 'bdsm' / 'lightstruct.py'))
else:
	from urllib.request import urlopen
	with urlopen('https://raw.githubusercontent.com/MrKleiner/bootlegger/main/lightstruct.py') as response:
	    litestruct = response.read()
	    (project / 'bdsm' / 'lightstruct.py').write_bytes(litestruct)

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
	str(project / 'bdsm' / 'icon' / 'enginer.ico'),
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