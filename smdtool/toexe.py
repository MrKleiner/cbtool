import subprocess, os, shutil, sys, base64, json
from pathlib import Path

thisdir = Path(__file__).parent
project = Path(__file__).parent.parent

cmpileprms = [
	# because this is an older python
	str(project / 'bdsm' / 'python' / 'bin' / 'python.exe'),
	'-m',
	'PyInstaller',
	'--noconfirm',
	'--onefile',
	# '--windowed',
	'--console',
	'--icon', str(thisdir / 'icont.ico'),
	str(thisdir / 'smdt.py')
]

subprocess.call(cmpileprms)


# move exe
shutil.move(str(thisdir / 'dist' / 'smdt.exe'), str(thisdir / 'smdt.exe'))

# delete shit
shutil.rmtree(str(thisdir / 'build'))
shutil.rmtree(str(thisdir / 'dist'))
(thisdir / 'smdt.spec').unlink(missing_ok=True)



