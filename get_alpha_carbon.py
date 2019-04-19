from operator import attrgetter
from itertools import chain

class AC(object):
	def __init__(self, position, aa, x=0, y=0, z=0):
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

def get_alpha_carbon(pdb_fn, top_b_factor):  
	"""Input is pdb filename and B-factor cut off returns list of AC objects that have a B-factor above the cutoff normalized value."""
	
	pd_lines = [l.split() for l in open(pdb_fn, "r").read().splitlines()]
	pdb_alpha = [AC(l[5],l[3],l[6],l[7],l[8],l[-2]) for l in pd_lines if l[0] == 'ATOM' and l[2] == 'CA']
	# print(len(pdb_alpha))
	# for ac in pdb_alpha:
		# print(ac)
	b_max = max([ac.b for ac in pdb_alpha])
	b_cutoff = bmax - bmax*top_b_factor
	
	return [a for a in pdb_alpha if a.b >= b_cutoff]
	
def build_grid_1D(alpha_list, block, grid_rad):
	"""prototype for build grid 3d"""
	
	block_rad = block/2
	grid_size = (grid_rad*2)+1
	for target in alpha_list:
		print(f"Target = {target}")
		center = target.x
		adj_acs = [AC(a.position,a.aa, (grid_rad + ((a.x - center)+block_rad)//block)) for a in alpha_list]
		# for a in adj_acs:
			# if a.x == grid_rad +1:
				# print(a)
		map = []
		for i in range(grid_size):
			a_here = 'o'
			for a in adj_acs:
				if i == a.x:
					a_here = (a.aa)
			map.append(a_here)
					
		print(map)
	
	
	
# my_pdb = sys.argv[1]
##for no cut off make b_factor cutoff 'inf'
# my_bf = float(sys.argv[2])


def split_dim(ac_list, d, dim, min, max):
	"""returns a list of list of ACs split at d in the dimesion (x,y,z)"""
	
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
	
def draw_grid(ac_list, d):
	"""returns 3d list of alpha carbons (or blank space) arragned in cubes"""
	
	min_x, max_x = get_min_max(ac_list, 'x')
	min_y, max_y = get_min_max(ac_list, 'y')
	min_z, max_z = get_min_max(ac_list, 'z')
	# x split
	x_split = split_dim(ac_list, d, 'x', min_x, max_x)
	# y split
	xy_split = []
	for x_slice in x_split:
		xy_split.append(split_dim(x_slice,d,'y',min_y,max_y))
	# z split
	xyz_split = []
	for xy_slice in xy_split:
		z_list = []
		for y_slice in xy_slice:
			z_list.append(split_dim(y_slice, d, 'z', min_z, max_z))
		xyz_split.append(z_list)
	#print dimensions
	# print(f"x = {len(xyz_split)}, y = {len(xyz_split[0])}, z = {len(xyz_split[0][0])}")
	return xyz_split
	
def grid_info(grid):
	"""returns number of cubes, max number of alpha carbons per cube, and total number of alpha carbons in grid"""
	
	grid_list = list(chain.from_iterable(list(chain.from_iterable(grid))))
	n_aa = [len(cube) for cube in grid_list]
	return len(grid_list), max(n_aa), sum(n_aa)

def file_to_grid(filename, dim):
	"""returns grid from pdb file with specified dim"""
	
	filetype = filename.split('.')[-1]
	acs = []
	if filetype == "cif":
		acs = get_alpha_carbon_cif(filename)
	elif filetype == 'pdb':
		acs = get_alpha_carbon_pdb(filename)
	else:
		print("Error worng file type")
		return None
	grid = draw_grid(acs, dim)
	n_cubes, max_aa, n_ac_inGrid = grid_info(grid)
	print(f"{filename} with AC dim {dim} produced a grid with {n_cubes} cubes with {max_aa} per cube")
	return grid
