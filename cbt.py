import customtkinter, tkinter, subprocess, shutil, sys, os, asyncio, threading
from pathlib import Path
from lightstruct import lightstruct
# from zipfile import ZipFile

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

format_dict = {
	'RGBA8888',
	'ABGR8888',
	'RGB888',
	'BGR888',
	'RGB565',
	'I8',
	'IA88',
	'P8',
	'A8',
	'RGB888_BLUESCREEN',
	'BGR888_BLUESCREEN',
	'ARGB8888',
	'BGRA8888',
	'DXT1',
	'DXT3',
	'DXT5',
	'BGRX8888',
	'BGR565',
	'BGRX5551',
	'BGRA4444',
	'DXT1_ONEBITALPHA',
	'BGRA5551',
	'UV88',
	'UVWQ8888',
	'RGBA16161616F',
	'RGBA16161616',
	'UVLX8888'
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
root.geometry('650x850')
root.minsize(650, 100)
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
# SCROLLBARS WHEN ?!
# ctk_textbox_scrollbar = customtkinter.CTkScrollbar(frame)
# ctk_textbox_scrollbar.pack()





# ==============================================
#           Basically the app itself
# ==============================================

class sex:
	def __init__(self, assloop):

		self.asc_loop = assloop

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
		customtkinter.CTkLabel(master=self.config_section, text='Folder containing bsp files to fix OR a single .bsp file', font=('', 16)).pack(pady=2, padx=10, anchor='w')
		self.bsp_files = customtkinter.CTkEntry(master=self.config_section, placeholder_text='Folder containing bsp files to fix')
		self.bsp_files.pack(pady=0, padx=10, fill='both')


		#
		# Whether to flag every single VTF in a bsp or not
		#
		self.vtf_force = tkinter.StringVar()
		self.vtf_force.set('no')

		vtf_force_checkbox = customtkinter.CTkCheckBox(
			master=self.config_section,
			text='Flag every single VTF in the bsp and dont only target PBR cubemaps',
			# height=5,
			border_width=1,
			corner_radius=4,
			checkbox_width=17,
			checkbox_height=17,
			font=('', 12),

			variable=self.vtf_force,
			onvalue='yes',
			offvalue='no'
		)
		vtf_force_checkbox.pack(pady=10, padx=10, anchor='w')





		# bspzip folder
		# customtkinter.CTkLabel(
		# 	master=self.config_section,
		# 	# wraplength=500,
		# 	justify='left',
		# 	text="""Path to the folder containing bspzip""",
		# 	font=('', 16)
		# ).pack(pady=5, padx=10, anchor='w')
		self.bspzip_folder = customtkinter.CTkEntry(master=self.config_section, placeholder_text='Bspzip folder')
		# self.bspzip_folder.pack(pady=0, padx=10, fill='both')


		# game folder (what the fuck ???)
		# customtkinter.CTkLabel(
		# 	master=self.config_section,
		# 	wraplength=500,
		# 	justify='left',
		# 	text="""Path to the folder containing gameinfo. Yes, what the fuck? I don't know... It has to be a game within the engine you're using your bspzip from.""",
		# 	font=('', 16)
		# ).pack(pady=5, padx=10, anchor='w')
		self.game_folder = customtkinter.CTkEntry(master=self.config_section, placeholder_text='Game folder')
		# self.game_folder.pack(pady=0, padx=10, fill='both')



		#
		# Button to SEX!
		#
		self.button = customtkinter.CTkButton(
			master=frame,
			width=120,
			height=32,
			border_width=0,
			corner_radius=8,
			text='SEX!',
			# command=self.exec_sex
			# self.asc_loop
			command=lambda:self.exec_sex(async_loop)
		)
		# button.pack(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
		self.button.pack(pady=10, padx=10, fill='both')

		self.progressbar = customtkinter.CTkProgressBar(
			master=frame
			# mode='indeterminate'
		)
		self.progressbar.pack(padx=20, pady=10, fill='x')
		# self.progressbar.configure(
		# 	_from=0,
		# 	to=100
		# )

		self.progressbar.set(0)

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

	def upd_progress(self, progr):
		pass

	# evaluate flags into a single integer represented as bytes
	# current_flgs = bytes or int STRICTLY
	def eval_flags(self, current_flags, flgs_add=[], flgs_subtract=[]):
		if not isinstance(current_flags, int):
			current_flags = int.from_bytes(current_flags, sys.byteorder)

		# subtract flags
		# todo: what do these c++ operators actually do ??
		for subtr in flgs_subtract:
			current_flags &= ~subtr

		# add flags
		for add_flg in flgs_add:
			current_flags |= add_flg

		# return byte representation of the result
		# return current_flags.to_bytes(4, sys.byteorder)
		return current_flags


	# modify a physical VTF file on a disk
	def mod_vtf(self, vtfpath, flgs_add=[], flgs_subtract=[]):
		with open(str(vtfpath), 'r+b') as vtf_file:
			# flags are stored in a 4-byte integer starting at 20th byte
			# move the cursor there
			vtf_file.seek(20, 0)
			# evaluate new flags
			new_flags = self.eval_flags(vtf_file.read(4), flgs_add, flgs_subtract)

			# move the cursor back and overwrite old flags with the new ones
			vtf_file.seek(20, 0)
			# overwrite the thing
			vtf_file.write(new_flags)


	# unpack bsp cubemaps into a certain location
	# bsp_path = path to the .bsp file
	# tmp_path = path to the folder to store temp files in
	# bspzip = path to the bspzip executable
	def unpack_cubes(self, bsp_path, tmp_path, bspzip, game_dir):

		print('unpacking cubes for', bsp_path)

		tmp_path = Path(tmp_path)
		bsp_path = Path(bsp_path)

		#
		# extract stuff with zip files, because extracting it with bspzip kills cubemap vtfs
		#
		with ZipFile(str(bsp_path), 'r') as unz:
			unz.extractall(path=str(tmp_path))


		#
		# Delete cubemaps, because this is the only way to overwrite the files
		#
		delcubes = [
			# bspzip executable
			str(bspzip),
			'-deletecubemaps',
			str(bsp_path)
		]

		subprocess.call(delcubes, cwd=str(game_dir))

		print('getting all vtfs from', (tmp_path / 'materials' / 'maps' / bsp_path.stem))

		return (
			[mat for mat in (tmp_path / 'materials' / 'maps' / bsp_path.stem).glob('*.vtf')],
			[allf for allf in (tmp_path / 'materials' / 'maps' / bsp_path.stem).rglob('*')]
		)


	# modify the bsp WITHOUT unpacking it or anything
	def mod_bsp_binary(self, bsp_path, add_flags=[], remove_flags=[]):
		with open(str(bsp_path), 'rb') as bsp:
			# read the contents of the bsp
			# todo: ram-efficient mode where it reads the file in chunks
			bsp_content = bsp.read()

			# lookup VTF offsets
			vtf_offs = 0
			# store tuples where:
			# 0 = Flag offset of the VTF
			# 1 = current flags as bytes
			vtf_matches = []
			while True:
				try:
					found = bsp_content.index('VTF\0'.encode(), vtf_offs, len(bsp_content))
					# vtf_matches.append((found + 20, bsp_content[found+20:found+20+4]))
					vtf_matches.append(found)
					vtf_offs = found + 4
				except:
					break

		# actually modify the file
		with open(str(bsp_path), 'r+b') as mod_bsp:
			lstruct_ref = lightstruct(
				mod_bsp,
				signature =            (str, 4),
				version =              (int, 2),
				headerSize =           (int, 1),
				width =                ('short', 1),
				height =               ('short', 1),
				flags =                (int, 1),
				frames =               ('short', 1),
				firstFrame =           ('short', 1),
				padding0 =             (str, 4),
				reflectivity =         (float, 3),
				padding1 =             (str, 4),
				bumpmapScale =         (float, 1),
				highResImageFormat =   (int, 1)
			)
			for vtf_offs in vtf_matches:
				# mod_bsp.seek(vtf_offs[0], 0)
				# cur_flags = mod_bsp.read(4)
				# mod_bsp.seek(vtf_offs[0], 0)
				# mod_bsp.write(self.eval_flags(cur_flags, add_flags, remove_flags))
				lstruct_ref.global_offs(vtf_offs)
				cur_flags = lstruct_ref['flags'][0]
				# only apply this to HDR vtfs which are also cubemaps
				if lstruct_ref['highResImageFormat'][0] == 24 and self.eval_flags(cur_flags, [0x4000], []) == cur_flags or self.vtf_force.get() == 'yes':
					# print('do apply')
					lstruct_ref['flags'] = (self.eval_flags(cur_flags, add_flags, remove_flags),)




	# the thing which does sex, basically
	def exec_sex_old(self):
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



	# the thing which does sex, basically
	async def exec_sex_ass(self):
		# lock the button
		self.button.configure(state='disabled')
		print('bsp directory val:', self.bsp_files.get())

		# grab .bsp files from here
		tgt_dir = Path(self.bsp_files.get().strip().strip('"').strip())
		# this is required, because bspzip relies on this...
		game_folder = Path(self.game_folder.get().strip().strip('"').strip())
		# bspzip executable
		bspzip_exe = Path(self.bspzip_folder.get().strip().strip('"').strip()) / 'bspzip.exe'

		# ensure that the temp dir exists
		# for now just silently create it as a sibling
		# tmpdir = (game_folder / 'temp_delete_me')
		# tmpdir.mkdir(exist_ok=True)

		# collapse flag pool in gui
		# if self.flagpool_expanded:
		# 	self.cbframe.pack_forget()
		# 	self.flagpool_expanded = False

		# create an array of flags to add/subtract
		add_flags = [flag_dict.get(fl.get()) for fl in self.cb_flags_add if flag_dict.get(fl.get()) != None]
		rm_flags = [flag_dict.get(rmfl.get()) for rmfl in self.cb_flags_remove if flag_dict.get(rmfl.get()) != None]

		# process every map
		if tgt_dir.is_dir():
			all_maps = [mp for mp in tgt_dir.glob('*.bsp') if mp.is_file()]
		else:
			all_maps = [tgt_dir]
		for bsp_idx, bsp in enumerate(all_maps):
			self.progressbar.set((bsp_idx+1) / len(all_maps))
			self.mod_bsp_binary(bsp, add_flags, rm_flags)


		self.button.configure(state='normal')




	def thread_tgt(self, ascloop):
		ascloop.run_until_complete(self.exec_sex_ass())


	def exec_sex(self, loop):
		threading.Thread(target=self.thread_tgt, args=(loop,)).start()



async_loop = asyncio.get_event_loop()

# launch app
app = sex(async_loop)