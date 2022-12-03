import customtkinter, tkinter, subprocess, shutil, sys, os
from pathlib import Path
from zipfile import ZipFile

flag_dict = {
	'Point Sampling':                               0x0001,
	'Trilinear Sampling':                           0x0002,
	'Clamp S':                                      0x0004,
	'Clamp T':                                      0x0008,
	'Anisotropic Sampling':                         0x0010,
	'Hint DXT5':                                    0x0020,
	'PWL Corrected':                                0x0040,
	'No Compress':                                  0x0040,
	'Normal Map':                                   0x0080,
	'No Mipmaps':                                   0x0100,
	'No Level Of Detail':                           0x0200,
	'No Minimum Mipmap':                            0x0400,
	'Procedural':                                   0x0800,
	'Render Target':                                0x8000,
	'Depth Render Target':                          0x10000,
	'No Debug Override':                            0x20000,
	'Single Copy':                                  0x40000,
	'Pre SRGB':                                     0x80000,
	'One Over Mipmap Level In Alpha':               0x80000,
	'Premultiply Color By One Over Mipmap Level':   0x100000,
	'Normal To DuDv':                               0x200000,
	'Alpha Test Mipmap Generation':                 0x400000,
	'No Depth Buffer':                              0x800000,
	'Nice Filtered':                                0x1000000,
	'Clamp U':                                      0x2000000,
	'Vertex Texture':                               0x4000000,
	'SSBump':                                       0x8000000,
	'Border':                                       0x20000000
}


application_path = os.path.dirname(sys.executable)
thisdir = Path(application_path).absolute()


# ==============================================
#              TKINTER CORE CONFIG
# ==============================================

# set tk theme
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')

# create the app frame
root = customtkinter.CTk()
# set initial height/width
root.geometry('650x950')
root.minsize(650, 800)
# set name
root.title('Chuck Norris')


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath('.')

	return os.path.join(base_path, relative_path)


try:
	theicon = resource_path('doubt.ico') if Path(resource_path('doubt.ico')).is_file() else 'doubt.ico'
	root.iconbitmap(theicon)
except:
	pass

# create the root frame
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=10, padx=10, fill='both', expand=True)

# SCROLLBARS ?!
# ctk_textbox_scrollbar = customtkinter.CTkScrollbar(frame)
# ctk_textbox_scrollbar.pack()




# ==============================================
#                      TEST
# ==============================================
def login(vr='DED'):
	print('Test', vr)

def test():
	frame = customtkinter.CTkFrame(master=root)
	frame.pack(pady=20, padx=60, fill='both', expand=True)

	label = customtkinter.CTkLabel(master=frame, text='Login System')
	label.pack(pady=12, padx=10)

	entry1 = customtkinter.CTkEntry(master=frame, placeholder_text='username')
	entry1.pack(pady=12, padx=10)

	entry2 = customtkinter.CTkEntry(master=frame, placeholder_text='password', show='*')
	entry2.pack(pady=12, padx=10)


	button = customtkinter.CTkButton(master=frame, text='Login', command=login)
	button.pack(pady=12, padx=10)

	checkbox = customtkinter.CTkCheckBox(master=frame, text='remember Me')
	checkbox.pack(pady=12, padx=10)

	root.mainloop()









# ==============================================
#           Basically the app itself
# ==============================================

class sex:
	def __init__(self):

		#
		# Collapse/Expand preferences, because scrollbars are borken
		#
		self.prefs_expanded = True
		self.toggle_prefs_pool = customtkinter.CTkButton(
			master=frame,
			width=120,
			height=25,
			border_width=0,
			corner_radius=5,
			text='Collapse/Expand prefs pool (scrollbars are broken)',
			command=self.toggle_prefs_pool_vis
		)
		self.toggle_prefs_pool.pack(pady=5, padx=10)


		self.config_section = customtkinter.CTkFrame(master=frame, fg_color='transparent')
		self.config_section.pack(pady=0, padx=5, fill='x')

		# folder with bsp files
		customtkinter.CTkLabel(master=self.config_section, text='Folder containing bsp files to fix', font=('', 16)).pack(pady=2, padx=10, anchor='w')
		self.bsp_files = customtkinter.CTkEntry(master=self.config_section, placeholder_text='Folder containing bsp files to fix')
		self.bsp_files.pack(pady=0, padx=10, fill='both')


		# bspzip folder
		customtkinter.CTkLabel(
			master=self.config_section,
			# wraplength=500,
			justify='left',
			text="""Path to the folder containing bspzip""",
			font=('', 16)
		).pack(pady=5, padx=10, anchor='w')
		self.bspzip_folder = customtkinter.CTkEntry(master=self.config_section, placeholder_text='Bspzip folder')
		self.bspzip_folder.pack(pady=0, padx=10, fill='both')


		# game folder (what the fuck ???)
		customtkinter.CTkLabel(
			master=self.config_section,
			wraplength=500,
			justify='left',
			text="""Path to the folder containing gameinfo. Yes, what the fuck? I don't know... It has to be a game within the engine you're using your bspzip from.""",
			font=('', 16)
		).pack(pady=5, padx=10, anchor='w')
		self.game_folder = customtkinter.CTkEntry(master=self.config_section, placeholder_text='Game folder')
		self.game_folder.pack(pady=0, padx=10, fill='both')



		#
		# Button to SEX!
		#
		button = customtkinter.CTkButton(
			master=frame,
			width=120,
			height=32,
			border_width=0,
			corner_radius=8,
			text='SEX!',
			command=self.exec_sex
		)
		# button.pack(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
		button.pack(pady=10, padx=10, fill='both')




		#
		# Collapse/Expand checkbox pool, because scrollbars are weird and broken
		#
		self.flagpool_expanded = True
		self.toggle_vis_btn = customtkinter.CTkButton(
			master=frame,
			width=120,
			height=25,
			border_width=0,
			corner_radius=5,
			text='Collapse/Expand flag pool (scrollbars are broken)',
			command=self.toggle_flags_pool_vis
		)
		self.toggle_vis_btn.pack(pady=5, padx=10)


		# section with flags to add
		cbframe = customtkinter.CTkFrame(master=frame)
		# cbframe.pack(pady=5, padx=5, fill='both', expand=True)
		cbframe.pack(pady=0, padx=5, fill='x')
		self.cbframe = cbframe


		# Label indicator that this column adds flags
		customtkinter.CTkLabel(master=cbframe, text='Add', font=('', 16)).grid(row=0, column=0, pady=2, padx=15, sticky='w')

		# flags to add
		self.cb_flags_add = []
		for add_ind, flg_add in enumerate(flag_dict):
			check_var = tkinter.StringVar()
			check_var.set('fuckoff')
			self.cb_flags_add.append(check_var)

			checkbox_add_flag = customtkinter.CTkCheckBox(
				master=cbframe,
				text=flg_add,
				height=5,
				border_width=1,
				corner_radius=4,
				checkbox_width=17,
				checkbox_height=17,
				font=('', 12),

				variable=check_var,
				onvalue=flg_add,
				offvalue='fuckoff'
			)
			checkbox_add_flag.grid(row=add_ind + 1, column=0, pady=0, padx=10, sticky='w')



		# Label indicator that this column removes flags
		customtkinter.CTkLabel(master=cbframe, text='Remove', font=('', 16)).grid(row=0, column=1, pady=2, padx=15, sticky='w')

		# flags to remove
		self.cb_flags_remove = []
		for sub_ind, flg_subt in enumerate(flag_dict):
			check_var = tkinter.StringVar()
			check_var.set('fuckoff')
			self.cb_flags_remove.append(check_var)

			checkbox2 = customtkinter.CTkCheckBox(
				master=cbframe,
				height=5,
				text=flg_subt,
				border_width=1,
				corner_radius=4,
				checkbox_width=17,
				checkbox_height=17,
				font=('', 12),

				variable=check_var,
				onvalue=flg_subt,
				offvalue='fuckoff'
			)
			checkbox2.grid(row=sub_ind + 1, column=1, pady=2, padx=10, sticky='w')





		#
		# Init the App
		#
		root.mainloop()
		

	def toggle_flags_pool_vis(self):
		if self.flagpool_expanded:
			self.cbframe.pack_forget()
		else:
			self.cbframe.pack(pady=0, padx=5, fill='x', after=self.toggle_vis_btn)

		self.flagpool_expanded = not self.flagpool_expanded


	def toggle_prefs_pool_vis(self):
		if self.prefs_expanded:
			self.config_section.pack_forget()
		else:
			self.config_section.pack(pady=0, padx=5, fill='x', after=self.toggle_prefs_pool)

		self.prefs_expanded = not self.prefs_expanded


	# flgs_add and flgs_subtract take an array of integers which represent flag values
	def mod_vtf(self, vtfpath, flgs_add=[], flgs_subtract=[]):
		with open(str(vtfpath), 'r+b') as vtf_file:
			# flags are stored in the 21st byte of the vtf file
			# move the cursor there
			vtf_file.seek(20, 0)
			# read the byte containing vtf flags as an int
			current_flags = int.from_bytes(vtf_file.read(1), sys.byteorder)

			print('got flags', current_flags)

			# subtract flags
			# todo: what do these c++ operators actually do ??
			for subtr in flgs_subtract:
				current_flags &= ~subtr

			# add flags
			for add_flg in flgs_add:
				current_flags |= add_flg

			# move the cursor 1 byte back to overwrite the flags byte with the new value
			vtf_file.seek(20, 0)
			# overwrite the thing
			vtf_file.write(current_flags.to_bytes(4, sys.byteorder))
			# vtf_file.write(bytes.fromhex(hex(current_flags)[2:]))


	# unpack bsp cubemaps into a certain location
	# bsp_path = path to the .bsp file
	# tmp_path = path to the folder to store temp files in
	# bspzip = path to the bspzip executable
	def unpack_cubes(self, bsp_path, tmp_path, bspzip, game_dir):

		print('unpacking cubes for', bsp_path)

		tmp_path = Path(tmp_path)
		bsp_path = Path(bsp_path)

		unpack_prms = [
			# bspzip executable
			str(bspzip),
			'-extractcubemaps',
			str(bsp_path),
			str(tmp_path)
		]

		waiting = None
		with subprocess.Popen(unpack_prms, stdout=subprocess.PIPE, bufsize=10**8, cwd=str(game_dir)) as unpack_pipe:
			waiting = unpack_pipe.stdout.read()


		#
		# Delete cubemaps, because this is the only way to overwrite the files
		#
		delcubes = [
			# bspzip executable
			str(bspzip),
			'-deletecubemaps',
			str(bsp_path)
		]

		# subprocess.call(delcubes, cwd=str(game_dir))

		waiting = None
		with subprocess.Popen(delcubes, stdout=subprocess.PIPE, bufsize=10**8, cwd=str(game_dir)) as unpack_pipe:
			waiting = unpack_pipe.stdout.read()



		print('getting all vtfs from', (tmp_path / 'materials' / 'maps' / bsp_path.stem))

		return [mat for mat in (tmp_path / 'materials' / 'maps' / bsp_path.stem).glob('*.vtf')]


	# the thing which does sex, basically
	def exec_sex(self):
		print('bsp directory val:', self.bsp_files.get())

		# grab .bsp files from here
		tgt_dir = Path(self.bsp_files.get().strip().strip('"').strip())
		# this is required, because bspzip relies on this...
		game_folder = Path(self.game_folder.get().strip().strip('"').strip())
		# bspzip executable
		bspzip_exe = Path(self.bspzip_folder.get().strip().strip('"').strip()) / 'bspzip.exe'

		# ensure that the temp dir exists
		# for now just silently create it as a sibling
		tmpdir = (game_folder / 'temp_delete_me')
		tmpdir.mkdir(exist_ok=True)

		# collapse flag pool in gui
		if self.flagpool_expanded:
			self.cbframe.pack_forget()
			self.flagpool_expanded = False

		# process every map
		for bsp in tgt_dir.glob('*.bsp'):
			# unpack cubemap vtfs from bsp and return paths to them
			vtfs = self.unpack_cubes(bsp, tmpdir, bspzip_exe, game_folder)

			print('unpacked cubes for', bsp, vtfs)

			# add flags to each one of these vtfs
			add_flags = [flag_dict.get(fl.get()) for fl in self.cb_flags_add if flag_dict.get(fl.get()) != None]
			rm_flags = [flag_dict.get(rmfl.get()) for rmfl in self.cb_flags_remove if flag_dict.get(rmfl.get()) != None]

			# print(f'{add_flags=}')
			# print(f'{rm_flags=}')

			# list for repack
			bsplist = ''
			return
			# actually add the fucking flags
			for vtf in vtfs:
				# add flags
				self.mod_vtf(vtf, add_flags, rm_flags)
				# add entries to list file
				# internal-abs
				bsplist += f'materials\\maps\\{bsp.stem}\\{vtf.name}' + '\n' + str(vtf) + '\n'


			# save list file to a temp location
			listfile = (game_folder / 'warcrimes_list.txt')
			listfile.write_bytes(bsplist.encode())

			# now repack the bsp with new shit
			repack_prms = [
				str(bspzip_exe),
				'-addlist',
				# map file
				str(bsp),
				# list file
				str(listfile),
				# write new bsp to this location
				# can be the same bsp location as src (overwrite)
				str(bsp)
			]

			waiting = None
			with subprocess.Popen(repack_prms, stdout=subprocess.PIPE, bufsize=10**8, cwd=str(game_folder)) as unpack_pipe:
				waiting = unpack_pipe.stdout.read()

			# delete the list file
			# listfile.unlink(missing_ok=True)

			# delete all the temp vtf files
			shutil.rmtree(str(tmpdir))
			tmpdir.mkdir(exist_ok=True)


# launch app
app = sex()