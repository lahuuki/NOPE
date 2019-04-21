from operator import attrgetter
from itertools import chain

#read in Epitope annotation file
ea_lines = open("Epitope_anno.tsv",'r').read().splitlines()
epi_anno = {}
for e in ea_lines:
	protein = e.split("\t")[0]
	epi_list = [int(p) for p in e.split("\t")[1][1:-1].split(',')]
	epi_anno[protein] = epi_list


class AC(object):
	def __init__(self, position, aa, x=0, y=0, z=0, epi= False):
		self.position = int(position)
		self.aa = aa
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)
		self.epi = epi

	def __str__(self):
		return f"{self.position}:{self.aa} {self.epi}\t({self.x},{self.y},{self.z})"

def get_base_fn(fn):
	return fn.split('\\')[-1].split('.')[0].upper()

def get_alpha_carbon_pdb(fn):
	"""Input is pdb filename returns list of AC objects"""

	epi_list = epi_anno[get_base_fn(fn)]
	pd_lines = [l.split() for l in open(pdb_fn, "r").read().splitlines()if len(l.split()) > 3]
	pdb_alpha = [AC(l[5],l[3],l[6],l[7],l[8],(int(l[5]) in epi_list)) for l in pd_lines if l[0] == 'ATOM' and l[2] == 'CA']
	return pdb_alpha

def get_alpha_carbon_cif(fn):
	"""Input is cif filename returns list of AC objects"""

	epi_list = epi_anno[get_base_fn(fn)]
	pd_lines = [l.split() for l in open(fn, "r").read().splitlines()if len(l.split()) > 3]
	pdb_alpha = [AC(l[8],l[5],l[10],l[11],l[12],(int(l[8]) in epi_list)) for l in pd_lines if l[0] == 'ATOM' and l[3] == 'CA']
	return pdb_alpha

def get_min_max(ac_list, dim):
	"""return min max points for the dimension"""

	return getattr(min(ac_list, key = attrgetter(dim)),dim), getattr(max(ac_list, key = attrgetter(dim)),dim)

def split_dim(ac_list, cd, dim, min, max):
	"""returns a list of list of ACs split at cd in the dimesion (x,y,z)"""

	split_list = []
	back_edge = min
	s = 0
	while back_edge < max:
		front_edge = back_edge + cd
		n_ac = 0
		slice_list = []
		for ac in ac_list:
			p = getattr(ac, dim)
			if p >= back_edge and p < front_edge:
				n_ac += 1
				slice_list.append(ac)
		back_edge = front_edge
		split_list.append(slice_list)
		s += 1
	return split_list

def draw_grid(ac_list, cd):
	"""returns 3d list of alpha carbons (or blank space) arragned in cubes"""

	min_x, max_x = get_min_max(ac_list, 'x')
	min_y, max_y = get_min_max(ac_list, 'y')
	min_z, max_z = get_min_max(ac_list, 'z')
	# x split
	x_split = split_dim(ac_list, cd, 'x', min_x, max_x)
	# y split
	xy_split = []
	for x_slice in x_split:
		xy_split.append(split_dim(x_slice,cd,'y',min_y,max_y))
	# z split
	xyz_split = []
	for xy_slice in xy_split:
		z_list = []
		for y_slice in xy_slice:
			z_list.append(split_dim(y_slice, cd, 'z', min_z, max_z))
		xyz_split.append(z_list)
	#print dimensions
	# print(f"x = {len(xyz_split)}, y = {len(xyz_split[0])}, z = {len(xyz_split[0][0])}")
	return xyz_split

def grid_info(grid):
	"""returns number of cubes, max number of alpha carbons per cube, and total number of alpha carbons in grid"""

	grid_list = list(chain.from_iterable(list(chain.from_iterable(grid))))
	n_aa = [len(cube) for cube in grid_list]
	return len(grid_list), max(n_aa), sum(n_aa)

def file_to_grid(filename, cd):
	"""returns grid from pdb file with specified cube dimension"""

	filetype = filename.split('.')[-1]
	acs = []
	if filetype == "cif":
		acs = get_alpha_carbon_cif(filename)
	elif filetype == 'pdb':
		acs = get_alpha_carbon_pdb(filename)
	else:
		print("Error worng file type")
		return None
	grid = draw_grid(acs, cd)
	n_cubes, max_aa, n_ac_inGrid = grid_info(grid)
	print(f"{filename} with AC dim {cd} produced a grid with {n_cubes} cubes with {max_aa} per cube")
	return grid

def file_to_tfin(filename,gps,anno):
    """from file, return subgrids for each AA and its epitope annotation. gps = grids per side of cube """
    
    pro = file_to_grid(filename.upper(),3)

cubelist = []
for x in range(len(pro)):
    for y in range(len(pro[x])):
        for z in range(len(pro[x][y])):
            for cube in pro[x][y][z]:
                if any(isinstance(cube,AC) for cube in pro[x][y][z]):
                    cubel = []
                    for l in pro[(x-3):(x+3)]:
                        cubeh = []
                        for h in l[(y-3):(y+3)]:
                            cubew = []
                            for w in h[(z-3):(z+3)]:
                                for obj in w:
                                    if any(isinstance(obj,AC) for obj in w):
                                        w = obj.aa
                                cubew.append(w)
                            cubeh.append(cubew)
                        cubel.append(cubeh)
                    cubelist.append(cubel)
