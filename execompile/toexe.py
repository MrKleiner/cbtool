import subprocess, os, shutil, sys, base64, json
from pathlib import Path

project = Path(__file__).parent.parent

freshstruct = Path(r'E:\!webdesign\bootlegger\bootlegger\lightstruct.py')

if freshstruct.is_file():
	shutil.copyfile(str(freshstruct), str(project / 'lightstruct.py'))
else:
	from urllib.request import urlopen
	with urlopen('https://raw.githubusercontent.com/MrKleiner/bootlegger/main/lightstruct.py') as response:
	    litestruct = response.read()
	    (project / 'lightstruct.py').write_bytes(litestruct)

cmpileprms = [
	# str(project / 'app'/ 'src' / 'bins' / 'python' / 'bin' / 'python.exe'),
	'py',
	'-m',
	'PyInstaller',
	'--noconfirm',
	'--onefile',
	'--windowed',
	# '--console',
	'--icon', str(project / 'doubt.ico'),
	# add icon file
	'--add-data', str(project / 'doubt.ico;.'),
	# some critical custom tkinter shit
	'--add-data', str(Path(sys.executable).parent / 'Lib/site-packages/customtkinter;customtkinter/') + '/',
	str(project / 'cbt.py')
]

subprocess.call(cmpileprms)


# move exe
shutil.move(str(project / 'execompile' / 'dist' / 'cbt.exe'), str(project / 'execompile' / 'cbt.exe'))

# delete shit
shutil.rmtree(str(project / 'execompile' / 'build'))
shutil.rmtree(str(project / 'execompile' / 'dist'))
(project / 'execompile' / 'cbt.spec').unlink(missing_ok=True)