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

class flagger:
	"""Mass flag vtfs inside a bsp"""
	def __init__(self):
		self.force_mod = False

		if '-force' in sys.argv:
			self.force_mod = True
			del sys.argv[sys.argv.index('-force')]

		try:
			self.tgt_path = Path(sys.argv[1].strip('"'))
		except Exception as e:
			usage_example()

		maps = []

		if sys.argv[1].strip('"').lower() == '-show_flags':
			# print(sys.argv)
			for flg in flag_dict:
				# ljust 43
				print(flg.ljust(43), flag_dict[flg])
			sys.exit()

		try:
			add_f = [int(adf) for adf in sys.argv[2].strip('"').strip(',').lower().split(',')]
		except Exception as e:
			if len(sys.argv) > 2:
				if not sys.argv[2].strip('"').strip() == ',':
					add_f = [flag_dict['No Minimum Mipmap']]
				else:
					add_f=[]
			else:
				add_f = [flag_dict['No Minimum Mipmap']]

		try:
			del_f = [int(rmf) for rmf in sys.argv[3].strip('"').strip(',').lower().split(',')]
		except Exception as e:
			del_f = []

		if self.tgt_path.is_dir():
			# print('The specified path is either not a directory or does not exist at all')
			# sys.exit()
			maps = [mp for mp in self.tgt_path.glob('*.bsp')]

		if self.tgt_path.is_file():
			maps = [self.tgt_path]

		if len(maps) <= 0:
			print('There are no maps to process...')
			print('Make sure that the path is wrapped in quotation marks ("")')
		

		for bsp_idx, bsp in enumerate(maps):
			try:
				self.mod_bsp_binary(bsp, add_f, del_f)
				self.set_progress(bsp_idx+1, len(maps))
			except Exception as e:
				print('A BDSM error occured...')
				print('Are you sure that the bsp is alright?')
				print('Are you sure that the bsp is NOT compressed?')



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


	def mod_bsp_binary(self, bsp_path, add_flags=[flag_dict['No Minimum Mipmap']], remove_flags=[]):
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
				if lstruct_ref['highResImageFormat'][0] == 24 and self.eval_flags(cur_flags, [0x4000], []) == cur_flags or self.force_mod == True:
					lstruct_ref['flags'] = (self.eval_flags(cur_flags, add_flags, remove_flags),)


	def set_progress(self, current, total):

		gui = 50

		os.system('cls')
		print(sys.version)
		progress = current / total

		filled = int(gui * progress)
		empty = int(gui - filled)
		print('')
		print(' BDSM Progress:')
		print(f""" ???[{'???'*filled}{' '*empty}]??? {current}/{total}""")
		print('')





do_sex = flagger()

