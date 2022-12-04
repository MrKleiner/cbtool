import sys, os
from pathlib import Path

# bros never forget bros

if len(sys.argv) <= 1:
	print('Missing a required argument: Path to the folder containing BSP files')
	print('Usage:')
	print('Open windows cmd in the same directory and then type')
	print('bdsm.exe "PATH TO THE FOLDER WITH BSP FILES OR A SINGLE BSP FILE"')
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


class flagger:
	"""Mass flag vtfs inside a bsp"""
	def __init__(self):
		self.tgt_path = Path(sys.argv[1].strip('"'))

		maps = []

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
				self.mod_bsp_binary(bsp)
				self.set_progress(bsp_idx+1, len(maps))
			except Exception as e:
				print('An error occured...')
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
		return current_flags.to_bytes(4, sys.byteorder)


	def mod_bsp_binary(self, bsp_path):
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
					vtf_matches.append((found + 20, bsp_content[found+20:found+20+4]))
					vtf_offs = found + 4
				except:
					break


		# actually modify the file
		with open(str(bsp_path), 'r+b') as mod_bsp:
			for vtf_offs in vtf_matches:
				mod_bsp.seek(vtf_offs[0], 0)
				cur_flags = mod_bsp.read(4)
				mod_bsp.seek(vtf_offs[0], 0)
				mod_bsp.write(self.eval_flags(cur_flags, [flag_dict['No Minimum Mipmap']], []))


	def set_progress(self, current, total):

		gui = 50

		os.system('cls')
		progress = current / total

		filled = int(gui * progress)
		empty = int(gui - filled)
		print('')
		print(f""" ►[{'█'*filled}{' '*empty}]◄ {current}/{total}""")
		print('')




do_sex = flagger()

