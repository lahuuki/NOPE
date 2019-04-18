from operator import attrgetter
from itertools import chain

class AC(object):
	def __init__(self, position, aa, x=0, y=0, z=0, b=0):
		self.position = int(position)
		self.aa = aa
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)
	
	def __str__(self):
		return f"{self.position}:{self.aa}\t({self.x},{self.y},{self.z})"
		

def get_alpha_carbon_pdb(pdb_fn):  
	"""Input is pdb filename returns list of AC objects"""
	pd_lines = [l.split() for l in open(pdb_fn, "r").read().splitlines()if len(l.split()) > 3]
	pdb_alpha = [AC(l[5],l[3],l[6],l[7],l[8]) for l in pd_lines if l[0] == 'ATOM' and l[2] == 'CA']
	return pdb_alpha

def get_alpha_carbon_cif(cif_fn):  
	"""Input is cif filename returns list of AC objects"""
	pd_lines = [l.split() for l in open(cif_fn, "r").read().splitlines()if len(l.split()) > 3]
	pdb_alpha = [AC(l[8],l[5],l[10],l[11],l[12]) for l in pd_lines if l[0] == 'ATOM' and l[3] == 'CA']
	return pdb_alpha	
		
def get_min_max(ac_list, dim):
	return getattr(min(ac_list, key = attrgetter(dim)),dim), getattr(max(ac_list, key = attrgetter(dim)),dim)

def split_dim(ac_list, d, dim, min, max):
	split_list = []
	back_edge = min
	s = 0
	total_ac = 0
	while back_edge < max:
		front_edge = back_edge + d
		n_ac = 0
		slice_list = []
		for ac in ac_list:
			p = getattr(ac, dim)
			if p >= back_edge and p < front_edge:
				n_ac += 1
				slice_list.append(ac)
		total_ac += n_ac
		#print(f"{s}\t{back_edge:}\t{front_edge}\t{n_ac}\t{len(slice_list)}\t{len(ac_list)}")
		back_edge = front_edge
		split_list.append(slice_list)
		s += 1
	#print(f"ACS {len(ac_list)} split {dim} = {[len(slice) for slice in split_list]}")
	return split_list
	
def draw_grid(ac_list, d = 3):
	min_x, max_x = get_min_max(ac_list, 'x')
	min_y, max_y = get_min_max(ac_list, 'y')
	min_z, max_z = get_min_max(ac_list, 'z')
	x_split = split_dim(ac_list, d, 'x', min_x, max_x)
	xy_split = []
	for x_slice in x_split:
		xy_split.append(split_dim(x_slice,d,'y',min_y,max_y))
	xyz_split = []
	for xy_slice in xy_split:
		for y_slice in xy_slice:
			xyz_split.append(split_dim(y_slice, d, 'z', min_z, max_z))
	
	return xyz_split
	
def grid_info(grid):
	grid_list = list(chain.from_iterable(grid))
	n_aa = [len(cube) for cube in grid_list]
	return len(grid_list), max(n_aa), sum(n_aa)

#test test
		
