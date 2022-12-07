


class writeable_as_file:
	def __init__(self, ref, global_offs=0):
		self.ref = ref
		self.gl_offs = global_offs

	def write(self, *args):
		return self.ref.write(*args)

	def read(self, *args):
		return self.ref.read(*args)

	def seek(self, offset, from_what):
		# args[0] += self.gl_offs
		if from_what == 0:
			offset += self.gl_offs
		# print('seeking from', offset)
		return self.ref.seek(offset, from_what)

	@property
	def cursor(self):
		return self.pointer + global_offs



class writeable_as_ram:
	def __init__(self, ref, global_offs=0):
		self.ref = ref
		self.pointer = 0
		self.gl_offs = 0

	def write(self, data):
		write_len = len(data)
		for wr in write_len:
			if self.pointer > write_len:
				self.ref[0] += wr
			else:
				self.ref[0][self.pointer] = wr
				self.pointer += 1

	def read(self, amt):
		# print('reading from', self.pointer, 'to', amt)
		return self.ref[0][self.pointer:self.pointer + amt]

	def seek(self, amt, offs=None):
		if offs == 0:
			self.pointer += amt + self.gl_offs
		else:
			self.pointer = amt


class lightstruct:
	"""
	A class to easily get file headers, like in C.
	Except this is all lies compared to C
	"""

	# def __new__(cls, ref, **args):
	# 	return super().__new__(cls, ref, args) 

	def __init__(self, ref, **args):
		import sys, io
		from pathlib import Path
		self.Path = Path

		self.io = io

		self.sys = sys
		self.struct = args
		self.is_template = False
		self.inram = False
		for arg in args:
			if len(args[arg]) < 2:
				self.struct[arg] = (args[arg][0], 1)
			else:
				self.struct[arg] = args[arg]

		# print(args)
		# isinstance(['sex'], list)


		if isinstance(ref, list):
			self.inram = True
			self.fl_path = None
			self.fl_ref = writeable_as_ram(ref)
			if ref[0] == None:
				ref[0] = b''
				self.is_template = True

			return

		if isinstance(ref, io.BufferedIOBase):
			self.fl_path = None
			self.fl_ref = writeable_as_file(ref)
			return

		if ref != None:
			self.fl_path = ref
			self.fl_ref = writeable_as_file(open(str(ref), 'r+b'))
		else:
			self.is_template = True



	def __getitem__(self, gt):
		return self.read_rule_from_offs_file(gt)

	def __setitem__(self, rname, nv):
		return self.upd_chunk(rname, nv)

	def dump_header(self):
		allhead = {}
		for hd in self.struct:
			allhead[hd] = self[hd]

		return allhead

	def read_rule_from_offs_file(self, rname):
		import struct

		offs = self.eval_offs(rname)

		self.fl_ref.seek(offs, 0)

		rule = self.struct[rname]

		if len(rule) < 2:
			amt = 1
		else:
			amt = rule[1]

		result = []

		for one in range(amt):
			if rule[0] == str:
				result.append(self.fl_ref.read(1).decode())
				# result.append(self.fl_ref.read(1))

			if rule[0] == int:
				result.append(int.from_bytes(self.fl_ref.read(4), self.sys.byteorder))

			if rule[0] == 'short':
				result.append(int.from_bytes(self.fl_ref.read(2), self.sys.byteorder))

			if rule[0] == 'long':
				result.append(int.from_bytes(self.fl_ref.read(8), self.sys.byteorder))

			if rule[0] == float:
				result.append(struct.unpack('f', self.fl_ref.read(4))[0])

		return tuple(result)

	# eval the amount of bytes taken by a single rule
	def eval_amount(self, rule):
		total_offs = 0
		if rule[0] == str:
			total_offs += rule[1]

		if rule[0] == float or rule[0] == int:
			total_offs += rule[1] * 4

		if rule[0] == 'short':
			total_offs += rule[1] * 2

		if rule[0] == 'long':
			total_offs += rule[1] * 8

		return total_offs

	def eval_offs(self, rulename):
		total_offs = 0
		for rl in self.struct:
			if rulename == rl:
				break
			rule = self.struct[rl]
			total_offs += self.eval_amount(rule)

		return total_offs

	def upd_chunk(self, rname, newval):
		import struct as enc

		rule = self.struct[rname]

		if len(newval) != rule[1]:
			return False

		tgt_offs = self.eval_offs(rname)

		self.fl_ref.seek(tgt_offs, 0)

		if rule[0] == str:
			for st in newval:
				val = st
				if not isinstance(st, bytes):
					val = st.encode()
				self.fl_ref.write(val)

		if rule[0] == float:
			for fl in newval:
				self.fl_ref.write(enc.pack('f', fl))

		if rule[0] == int:
			for intg in newval:
				self.fl_ref.write(intg.to_bytes(4, self.sys.byteorder))

		if rule[0] == 'short':
			for intg in newval:
				self.fl_ref.write(intg.to_bytes(2, self.sys.byteorder))

		if rule[0] == 'long':
			for intg in newval:
				self.fl_ref.write(intg.to_bytes(8, self.sys.byteorder))



	# basically overwrite the header struct with default values
	def flush(self):
		for rule in self.struct:
			self.fl_ref.write(bytes(self.eval_amount(self.struct[rule])))

	# reserve bytes in a file OR apply this pattern to an existing file
	def apply_to_file(self, flref):
		if not self.is_template == True:
			return None

		if isinstance(flref, self.io.BufferedIOBase):
			return lightstruct(flref, **self.struct)

		# return super().__new__(lightstruct, flref, self.struct)
		pth = self.Path(flref)
		doflush = False
		if not pth.is_file():
			pth.write_bytes(b'')
			doflush = True

		created = lightstruct(pth, **self.struct)

		if doflush == True:
			created.flush()

		return created


	def global_offs(self, offs=0):
		self.fl_ref.gl_offs = offs
		# self.fl_ref.seek(offs, 0)








if __name__ == '__main__':
	from pathlib import Path
	import json, os
	from random import random

	os.system('cls')

	generic = lightstruct(
		r'E:\!webdesign\cbtool\proto\map\single_texture_sex.vtf',
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
		highResImageFormat =   (int, 1),
		mipmapCount =          (str, 1),
		lowResImageFormat =    (int, 1),
		lowResImageWidth =     (str, 1),
		lowResImageHeight =    (str, 1),
		depth =                ('short', 1),
		padding2 =             (str, 3),
		numResources =         (int, 1),
		# padding3 =             (str, 8),

		tag =                  (str, 3),
		flagz =                (str, 1),
		offset =               (int, 1),

		tag2 =                  (str, 3),
		flagz2 =                (str, 1),
		offset2 =               (int, 1),

		tag3 =                  (str, 3),
		flagz3 =                (str, 1),
		offset3 =               (int, 1),
	)
	generic.global_offs(10)

	print(generic.fl_ref)

	print('')
	print('')
	print('')

	print('generic triple float', generic['reflectivity'][1])
	generic['reflectivity'] = (0.325, random(), 0.347)
	print('generic NEW triple float',generic['reflectivity'][1])

	generic_dump_head = generic.dump_header()

	for generic_h in generic_dump_head:
		print(generic_h, generic_dump_head[generic_h])

	print('')
	print('')
	print('')

	# sefdggh

	generic_new_path = Path(r'E:\!webdesign\cbtool\proto\map\generic_new.lol')
	generic_new_path.write_bytes(b'')

	generic_new = lightstruct(
		generic_new_path,
		signature =      (str, 4),
		version =        (int, 2),
		headerSize =     (int, 1),
		width =          ('short', 1),
		height =         ('short', 1),
		flags =          (int, 1),
		frames =         ('short', 1),
		firstFrame =     ('short', 1),
		padding0 =       (str, 4),
		reflectivity =   (float, 3),
		padding1 =       (str, 4),
		bumpmapScale =   (float, 1)
	)

	generic_new.flush()

	generic_new_headers = generic_new.dump_header()

	for generic_new_h in generic_new_headers:
		print(generic_new_h, generic_new_headers[generic_new_h])


	# template
	templ = lightstruct(
		None,
		signature =      (str, 4),
		version =        (int, 2),
		headerSize =     (int, 1),
		width =          ('short', 1),
		height =         ('short', 1),
		flags =          (int, 1),
		frames =         ('short', 1),
		firstFrame =     ('short', 1),
		padding0 =       (str, 4),
		reflectivity =   (float, 3),
		padding1 =       (str, 4),
		bumpmapScale =   (float, 1)
	)

	Path('E:/!webdesign/cbtool/proto/map/generic_new1.lol').unlink(missing_ok=True)
	Path('E:/!webdesign/cbtool/proto/map/generic_new2.lol').unlink(missing_ok=True)

	templ1 = Path('E:/!webdesign/cbtool/proto/map/generic_new1.lol')
	templ1_ref = templ.apply_to_file(templ1)
	print('')
	print(templ1_ref['width'])
	templ1_ref['width'] = (64,)
	print(templ1_ref['width'])

	templ2 = Path('E:/!webdesign/cbtool/proto/map/generic_new2.lol')
	templ2_ref = templ.apply_to_file(templ2)
	print('')
	print(templ2_ref['width'])
	templ2_ref['width'] = (128,)
	print(templ2_ref['width'])

	print(templ1_ref['width'])

	# INRAM OPERATIONS
	tomod = [Path(r"E:\!webdesign\cbtool\proto\map\single_texture_sex.vtf").read_bytes()]
	# tomod = [b'']
	ram_ops = lightstruct(
		tomod,
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
		highResImageFormat =   (int, 1),
		mipmapCount =          (str, 1),
		lowResImageFormat =    (int, 1),
		lowResImageWidth =     (str, 1),
		lowResImageHeight =    (str, 1),
		depth =                ('short', 1),
		padding2 =             (str, 3),
		numResources =         (int, 1),
		# padding3 =             (str, 8),

		tag =                  (str, 3),
		flagz =                (str, 1),
		offset =               (int, 1),

		tag2 =                  (str, 3),
		flagz2 =                (str, 1),
		offset2 =               (int, 1),

		tag3 =                  (str, 3),
		flagz3 =                (str, 1),
		offset3 =               (int, 1),
	)
	ram_ops.global_offs(10)

	print('')
	print('RAM OPS')
	print('')
	print(ram_ops['width'])


	print('apply template to an open file object')
	manysex = open(r"E:\!webdesign\cbtool\proto\map\single_texture_sex_2.vtf", 'r+b')
	multisex = templ.apply_to_file(manysex)
	multisex.global_offs(10)
	print(multisex['reflectivity'])
	multisex['reflectivity'] = (0.325, random(), 0.347)
	# multisex['reflectivity'] = (0.325, 0.911, 0.347)
	print(multisex['reflectivity'])


	print('')
	print('MDL')
	print('')
	# test mdl
	mdl_file = lightstruct(
		r"C:\Program Files (x86)\Steam\steamapps\common\GarrysMod\garrysmod\models\atm\bank_hydra.mdl",
		fid =                   (int,1),
		version =               (int,1),
		checksum =              (int,1),
		name =                  (str,64),
		dataLength =            (int,1),

		# Vector
		eyeposition =           (float,3),
		illumposition =         (float,3),
		hull_min =              (float,3),
		hull_max =              (float,3),
		view_bbmin =            (float,3),
		view_bbmax =            (float,3),

		flags =                 (int,1),

		bone_count =            (int,1),
		bone_offset =           (int,1),

		bonecontroller_count =  (int,1),
		bonecontroller_offset = (int,1),

		hitbox_count =          (int,1),
		hitbox_offset =         (int,1),

		localanim_count =       (int,1),
		localanim_offset =      (int,1),

		localseq_count =        (int,1),
		localseq_offset =       (int,1),

		activitylistversion =   (int,1),
		eventsindexed =         (int,1),

		texture_count =         (int,1),
		texture_offset =        (int,1),

		texturedir_count =      (int,1),
		texturedir_offset =     (int,1),

		skinreference_count =   (int,1),
		skinrfamily_count =     (int,1),
		skinreference_index =   (int,1),
	)

	mdlf_dumph = mdl_file.dump_header()

	for mdlf in mdlf_dumph:
		print(mdlf, mdlf_dumph[mdlf])

	print('mdl_name', ''.join(mdl_file['name']))


	texture_struct(
		None,

	)