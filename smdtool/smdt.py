from pathlib import Path
import os, sys

os.system('cls')

# thisdir = Path(__file__).parent

class smd:
	def __init__(self, smdpath):
		# raw smd lines
		self.smdl = tuple(Path(smdpath).read_text().split('\n'))
		
		# data that comes before the triangles array
		self.prefix = self.get_prefix()

		# tris offset
		# everything before the start of the tris = head
		# everything after that = leading data
		data_offs = self.get_tris_offs()

		# triangles
		self.tris = self.parse_tris(self.smdl[data_offs[0]:data_offs[1]])

		# leading data
		self.postfix = '\n'.join(self.smdl[data_offs[1]:])


	def get_prefix(self):
		head = ''
		for ln in self.smdl:
			if ln.strip() == 'triangles':
				break
			head += ln + '\n'

		return head

	# get start and end offset of the tris string from the lines array
	def get_tris_offs(self):
		tri_start_index = None
		for li, ln in enumerate(self.smdl):
			if ln.strip() == 'triangles':
				tri_start_index = li+1
			# todo: this a VERY stupid assumption
			if tri_start_index and ln.strip() == 'end':
				return (tri_start_index, li+1)

	# parse the triangles string
	def parse_tris(self, tris_lines):
		parsed_tris = {}
		t_i = 0
		while True:
			if tris_lines[t_i].strip() == 'end':
				break

			v1_raw = list(filter(None, tris_lines[t_i+1].strip().split(' ')))
			v2_raw = list(filter(None, tris_lines[t_i+2].strip().split(' ')))
			v3_raw = list(filter(None, tris_lines[t_i+3].strip().split(' ')))

			# position of each vertex
			v3 = (
				tuple([str(vf1) for vf1 in v1_raw[1:4]]),
				tuple([str(vf2) for vf2 in v2_raw[1:4]]),
				tuple([str(vf3) for vf3 in v3_raw[1:4]]),
			)

			# 'v': (pos3, nrm3, uv2, lead)
			# lead = leading data
			curent_tri = {
				# material
				'mat': tris_lines[t_i],

				# verts
				'v1': (v3[0], tuple([str(nrm1) for nrm1 in v1_raw[4:7]]), list([str(uv1) for uv1 in v1_raw[7:9]]), v1_raw[9:]),
				'v2': (v3[1], tuple([str(nrm2) for nrm2 in v2_raw[4:7]]), list([str(uv2) for uv2 in v2_raw[7:9]]), v2_raw[9:]),
				'v3': (v3[2], tuple([str(nrm3) for nrm3 in v3_raw[4:7]]), list([str(uv3) for uv3 in v3_raw[7:9]]), v3_raw[9:]),
			}

			parsed_tris[v3] = curent_tri

			t_i += 4


		return parsed_tris


def fix_val(src, lmap):
		# if src.startswith('1.0') or lmap.startswith('1.0'):
		# 	return src
		if src.startswith('1.0') and lmap.startswith('1.0'):
			return '1.00009999'

		src_num = src[0:6]
		lmap_num = lmap[2:7]
		lmap_end = int(lmap_num[-1])

		if lmap_end >= 5 and lmap_num.startswith('0000'):
			lmap_num = '0001'
		else:
			lmap_num = lmap_num[:-1]

		return src_num + lmap_num


def antivirus(tgt_smd):

	tgt_smd = Path(tgt_smd).absolute()

	tris_reverse = smd(tgt_smd)

	new_smd = ''
	lmap_smd = ''

	# 'v': (pos3, nrm3, uv2, lead)
	new_tris = ''
	lmap_tris = ''
	for tri in tris_reverse.tris:
		this_tri = tris_reverse.tris[tri]
		# lmap_tri = tris_lmap.tris[tri]
		new_tris += this_tri['mat'] + '\n'; lmap_tris += this_tri['mat'] + '\n'

		# fix verts
		for vert in ('v1','v2','v3',):
			this_vert = this_tri[vert]
			# lmap_vert = lmap_tri[vert]

			# write a zero
			new_tris += '0'; lmap_tris += '0'
			new_tris += '  '; lmap_tris += '  '
			# write pos
			new_tris += ' '.join(this_vert[0]); lmap_tris += ' '.join(this_vert[0])
			new_tris += '  '; lmap_tris += '  '
			# write normal
			new_tris += ' '.join(this_vert[1]); lmap_tris += ' '.join(this_vert[1])
			new_tris += '  '; lmap_tris += '  '
			# write reversed UV
			new_tris += this_vert[2][0][0:6]
			lmap_tris += '0.' + this_vert[2][0][6:10]
			new_tris += ' '; lmap_tris += ' '
			new_tris += this_vert[2][1][0:6]
			lmap_tris += '0.' + this_vert[2][1][6:10]
			new_tris += ' '; lmap_tris += ' '
			# leading bone data
			# todo: stupid assumption that the entirety of leading data is separated with singular space ' '
			new_tris += ' '.join(this_vert[3]); lmap_tris += ' '.join(this_vert[3])
			new_tris += '\n'; lmap_tris += '\n'

	new_smd += tris_reverse.prefix; lmap_smd += tris_reverse.prefix
	new_smd += 'triangles\n'; lmap_smd += 'triangles\n'
	new_smd += new_tris.strip(); lmap_smd += lmap_tris.strip()
	new_smd += '\nend\n'; lmap_smd += '\nend\n'
	new_smd += tris_reverse.postfix; lmap_smd += tris_reverse.postfix

	(tgt_smd.parent / f'{tgt_smd.stem}_src_reversed.smd').write_text(new_smd)
	(tgt_smd.parent / f'{tgt_smd.stem}_lightmap_reversed.smd').write_text(lmap_smd)






def exec():

	if len(sys.argv) < 3:
		print('Usage:')
		print('smdt.exe SRC_SMD LIGHTMAP_SMD RESULT_NAME')
		print('smdt.exe "E:/sex/sphere_normal.smd" "E:/sex/sphere_lightmap.smd" pootis')
		print("""(Don't forget the quotes " ")""")
		print('Converted smd is saved to the same dir the SRC_SMD is in.')
		print('If no RESULT_NAME specified - a default suffix _conv is added:')
		print('Blue for the virus. Green for the antivirus')
		print("""There's a cure""")
		print('The process can be reversed:')
		print('Type -reverse instead of the LIGHTMAP_SMD to split the SMD back')
		print('smdt.exe "E:/sex/sphere.smd" -reverse')
		print('Get it? Get the reference? Let me know...')
		return

	inp1 = sys.argv[1].strip('"')
	inp2 = sys.argv[2].strip('"')

	if inp2 == '-reverse':
		if not Path(inp1).is_file():
			print("""The target SMD does not exist. Aborting (I support abortion and everyone who doesn't agree can go fuck themselves)""")
			return
		antivirus(inp1)
		print('Finished reversing')
		return

	smd_src = Path(inp1)
	smd_lmap = Path(inp2)

	if False in (smd_src.is_file(), smd_lmap.is_file()):
		print('One of the smd files does not exist. Aborting')
		return

	tris_src = smd(smd_src)
	tris_lmap = smd(smd_lmap)

	if len(tris_src.tris) != len(tris_lmap.tris):
		print('Models have different triangle count. Wtf. Aborting...')
		return

	new_smd = ''

	# 'v': (pos3, nrm3, uv2, lead)
	new_tris = ''
	for tri in tris_src.tris:
		this_tri = tris_src.tris[tri]
		lmap_tri = tris_lmap.tris[tri]
		new_tris += this_tri['mat'] + '\n'

		# fix verts
		for vert in ('v1','v2','v3',):
			this_vert = this_tri[vert]
			lmap_vert = lmap_tri[vert]

			# write a zero
			new_tris += '0'
			new_tris += '  '
			# write pos
			new_tris += ' '.join(this_vert[0])
			new_tris += '  '
			# write normal
			new_tris += ' '.join(this_vert[1])
			new_tris += '  '
			# write fixed UV
			new_tris += fix_val(this_vert[2][0], lmap_vert[2][0])
			new_tris += ' '
			new_tris += fix_val(this_vert[2][1], lmap_vert[2][1])
			new_tris += ' '
			# leading bone data
			# todo: stupid assumption that the entirety of leading data is separated with singular space ' '
			new_tris += ' '.join(this_vert[3])
			new_tris += '\n'

	new_smd += tris_src.prefix
	new_smd += 'triangles\n'
	new_smd += new_tris.strip()
	new_smd += '\nend\n'
	new_smd += tris_src.postfix

	if len(sys.argv) > 3:
		(smd_src.parent / f'{sys.argv[3]}.smd').write_text(new_smd)
	else:
		(smd_src.parent / f'{smd_src.stem}_conv.smd').write_text(new_smd)

	print('Finished.')



exec()