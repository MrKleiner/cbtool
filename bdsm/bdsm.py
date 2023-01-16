import sys, os
from pathlib import Path
from lightstruct import lightstruct

# bros never forget bros


def usage_example():
	print('Usage:')
	print('bdsm.exe <-show_flags | -force | path to the folder containing bsp files | path to a single bsp file> <flag array to ADD : Default to 0x0400> <flag array to SUBTRACT : Default to NONE>')
	print('-show_flags : Print available flags that can be added/removed')
	print('-force: Process every single VTF in the .bsp regardless of its type')
	print('\tbdsm.exe -show_flags')
	print('Flag arrays have to be comma separated with NO WHITESPACES:')
	print('\tbdsm.exe "C:\\Team Fortress 2\\tf\\maps" 16777216,1024 4,8,16')
	print('\tbdsm.exe "C:\\Team Fortress 2\\tf\\maps\\pl_pisswater.bsp" 16777216,1024 4,8,16')
	print('\tbdsm.exe "C:\\Team Fortress 2\\tf\\maps\\pl_pisswater.bsp" -force 16777216,1024 4,8,16')
	print("""It's possible to skip flag addition, just put comma (,) instead of the flags""")
	print('\tbdsm.exe "C:\\Team Fortress 2\\tf\\maps\\pl_pisswater.bsp" , 16777216,8')


if len(sys.argv) <= 1:
	usage_example()
	sys.exit()



flag_dict = {
	'Point Sampling':                               0x0001,
	'Trilinear Sampling':                           0x0002,
	'Clamp S':                                      0x0004,
	'Clamp T':                                      0x0008,
	'Anisotropic Sampling':                         0x0010,
	'Hint DXT5':                                    0x0020,
	# PWL correction was removed, because its purpose is unknown and it had the same value as No Compress
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

format_dict = [
	'A8',
	'ABGR8888',
	'ARGB8888',
	'BGR565',
	'BGR888',
	'BGR888_BLUESCREEN',
	'BGRA4444',
	'BGRA5551',
	'BGRA8888',
	'BGRX5551',
	'BGRX8888',
	'DXT1',
	'DXT1_ONEBITALPHA',
	'DXT3',
	'DXT5',
	'I8',
	'IA88',
	'P8',
	'RGB565',
	'RGB888',
	'RGB888_BLUESCREEN',
	'RGBA16161616',
	'RGBA16161616F',
	'RGBA8888',
	'UV88',
	'UVLX8888',
	'UVWQ8888'
]

class flagger:
	"""Mass flag vtfs inside a bsp"""
	def __init__(self):
		self.force_mod = False

		# bros never forget bros:
		# the init is huge, only because this script uses a legacy python version compatible with windows 7
		# which doesn't has the match keyword


		# the -force argument could be present anywhere
		# because it's then deleted from the argument array and therefore does not interfere
		# with further argument evaluation
		if '-force' in sys.argv:
			self.force_mod = True
			del sys.argv[sys.argv.index('-force')]

		# if the first argument is not a valid path (aka not present)
		# then quit and print usage example
		# this allows printing the usage example when the script is called raw with no arguments
		try:
			self.tgt_path = Path(sys.argv[1].strip('"'))
		except Exception as e:
			usage_example()

		# if the first argument is -show_flags
		# then quit and pring the flags dict
		if sys.argv[1].strip('"').lower() == '-show_flags':
			# print(sys.argv)
			for flg in flag_dict:
				print(flg.ljust(43), flag_dict[flg])
			sys.exit()


		# at this point, the first argument should be the path to the file/folder
		# and following two arguments (second and third) have to be the flag arrays
		# (this section is responsible for evaluating the addition flags aka the second argument)
		# (the second argument is always the addition array, a comma has to be passed to skip the addition)
		try:
			# get rid of rubbish, split the argument by comma and try evaluating each element as an int
			add_f = [int(adf) for adf in sys.argv[2].strip('"').strip(',').lower().split(',')]
		except Exception as e:
			# exception = nothing is present / invalid argument. 
			# Fall back to the default action (adding 'No Minimum Mipmap' flag)

			# exception also occurs if the second element is just a comma
			# in this case, check if it's actually a comma or something invalid
			# ALSO, if it's a comma without the thrid argument - fall back to default (add 'No Minimum Mipmap' flag)
			if len(sys.argv) > 2:
				# at this point, if the second argument is present, but it's neither a valid flag array or a comma - 
				# fall back to default (add 'No Minimum Mipmap')
				if sys.argv[2].strip('"').strip() != ',':
					add_f = [flag_dict['No Minimum Mipmap']]
				else:
					# but if it's a comma, then nothing should be added
					add_f = []
			else:
				# whatever the second argument is, the third argument (subtraction) is not present.
				# Fall back to default (add 'No Minimum Mipmap' flag)
				add_f = [flag_dict['No Minimum Mipmap']]

		# The third argument (the subtraction array) is either valid or skipped
		try:
			del_f = [int(rmf) for rmf in sys.argv[3].strip('"').strip(',').lower().split(',')]
		except Exception as e:
			del_f = []


		#
		# Now get all the paths to the maps
		#

		# all the paths are put into the maps array
		# even if it's a path to a single file
		maps = []

		# if the first argument is a path to a folder - glob all .bsp files
		if self.tgt_path.is_dir():
			maps = [mp for mp in self.tgt_path.glob('*.bsp')]

		# if the first argument is a path to a single file - put this map into the map paths array
		if self.tgt_path.is_file():
			maps = [self.tgt_path]

		# this happens when the first argument either points to a folder with no .bsp files,
		# or to a non-existent file
		# in this case display an error and quit
		if len(maps) <= 0:
			print('There are no maps to process...')
			print('Make sure that the path is wrapped in quotation marks ("")')
			sys.exit()


		# go through every map path and do stuff with it
		for bsp_idx, bsp in enumerate(maps):
			try:
				self.mod_bsp_binary(bsp, add_f, del_f)
				self.set_progress(bsp_idx+1, len(maps))
			except Exception as e:
				print('A BDSM error occured...')
				print('Are you sure that the bsp is alright?')
				print('Are you sure that the bsp is NOT compressed?')
				# raise e



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

		return current_flags


	def mod_bsp_binary(self, bsp_path, add_flags=[flag_dict['No Minimum Mipmap']], remove_flags=[]):
		# get all the VTF file offsets
		with open(str(bsp_path), 'rb') as bsp:
			# read the contents of the bsp
			bsp_content = bsp.read()

			# lookup VTF offsets
			vtf_offs = 0

			# store offsets of each VTF file
			vtf_matches = []
			while True:
				try:
					found = bsp_content.index('VTF\0'.encode(), vtf_offs, len(bsp_content))
					vtf_matches.append(found)
					vtf_offs = found + 4
				except:
					break


		# define the vtf structure to the required extent (hires format, everything after that is not needed)
		vtf_struct = lightstruct(
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
		vtf_struct.smart = True

		# apply modifications
		with open(str(bsp_path), 'r+b') as mod_bsp:
			# apply the vtf structure to the current file
			mod_vtf,_ = vtf_struct.apply(mod_bsp)

			# go through every VTF offset and do stuff with the VTF
			for vtf_offs in vtf_matches:

				mod_vtf.set_offset(vtf_offs)
				cur_flags = mod_vtf['flags']

				# Only apply this to HDR vtfs which are also cubemaps.

				# The image format for HDR is RGBA16161616F and has an index of 24
				# And the cubemap check is performed by checking whether the flag value changes when 0x4000 (Environment Map) flag is added
				if (mod_vtf['highResImageFormat'] == 24 and self.eval_flags(cur_flags, [0x4000], []) == cur_flags) or self.force_mod == True:
					# print('Modifying a VTF at offset', vtf_offs)
					mod_vtf['flags'] = self.eval_flags(cur_flags, add_flags, remove_flags)


	def set_progress(self, current, total):
		# return
		gui = 50

		os.system('cls')
		print(sys.version)
		progress = current / total

		filled = int(gui * progress)
		empty = int(gui - filled)
		print(' Note: Modifying compressed bsp files may lead to data corruption!')
		print('')
		print(' BDSM Progress:')
		print(f""" ►[{'█'*filled}{' '*empty}]◄ {current}/{total}""")
		print('')





do_sex = flagger()

