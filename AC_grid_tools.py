from operator import attrgetter
from itertools import chain

#read in Epitope annotation file
ea_lines = open("searchable_2.tsv",'r').read().splitlines()
epi_anno = {}
for e in ea_lines:
	protein = e.split("\t")[0]
	epi_list = [int(p) for p in e.split("\t")[1][1:-1].split(',')]
	epi_anno[protein] = epi_list



class AC(object):
	def __init__(self, position, aa, x=0, y=0, z=0, epi= False, pi = 5.97):
		self.position = int(position)
		self.aa = aa
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)
		self.epi = epi
		if self.aa == 'GLY':
			pi = 5.97
		if self.aa == 'ALA':
			pi = 6
		if self.aa == 'VAL':
			pi = 5.96
		if self.aa == 'LEU':
			pi = 5.98
		if self.aa == 'ILE':
			pi = 6.02
		if self.aa == 'MET':
			pi = 5.74
		if self.aa == 'PRO':
			pi = 6.30
		if self.aa == 'PHE':
			pi = 5.48
		if self.aa == 'TRP':
			pi = 5.89
		if self.aa == 'ASN':
			pi = 5.41
		if self.aa == 'GLN':
			pi = 5.65
		if self.aa == 'SER':
			pi = 5.68
		if self.aa == 'THR':
			pi = 5.60
		if self.aa == 'TYR':
			pi = 5.66
		if self.aa == 'CYS':
			pi = 5.07
		if self.aa == 'ASP':
			pi = 2.77
		if self.aa == 'GLU':
			pi = 3.22
		if self.aa == 'LYS':
			pi = 9.74
		if self.aa == 'ARG':
			pi = 10.76
		if self.aa == 'HIS':
			pi = 7.59
		self.pi = pi
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
	# print(f"{filename} with AC dim {cd} produced a grid with {n_cubes} cubes with {max_aa} per cube")
	return grid

# def subgrid(grid):
# 	for ix,x in enumerate(grid):
# 		for iy,y in enumerate(x):
# 			for iz,z in enumerate(y):
# 				if z: #if cube is not empty
# 					print(f"({ix},{iy},{iz})\t{z[0]}")
#

def file_to_tfin(filename,griddim,gps):
    """from file, return subgrids for each AA and its epitope annotation. gps = grids per side of cube """
    """should probably get optimal grid dimensions and then run this on every protein"""
    pro = file_to_grid(filename,griddim)
    struc = get_base_fn(filename)
    cubelist = []
    toycube = []
    for ver in range(gps):
        sheet = []
        for hor in range(gps):
            line = []
            for cell in range(gps):
                line.append("empty")
            sheet.append(line)
        toycube.append(sheet)

    for x in range(len(pro)):
        for y in range(len(pro[x])):
            for z in range(len(pro[x][y])):
                for cube in pro[x][y][z]:
                    if any(isinstance(cube,AC) for cube in pro[x][y][z]):
                        tempcube = toycube[:]
                        if cube.position in epi_anno[struc]:
                                call = 1
                        else:
                                call = 0
                        xs = x-int((gps-1)/2)
                        if xs < 0:
                            xs = 0
                        xf = x+int((gps-1)/2)+1
                        if xf > len(pro):
                            xf = len(pro)
                        for xcount,l in enumerate(pro[xs:xf]):
                            ys = y-int((gps-1)/2)
                            if ys < 0:
                                ys = 0
                            yf = y+int((gps-1)/2)+1
                            if yf > len(l):
                                yf = len(l)
                            for ycount,h in enumerate(l[ys:yf]):
                                zs = z-int((gps-1)/2)
                                if zs < 0:
                                    zs = 0
                                zf = z+int((gps-1)/2)+1
                                if zf > len(h):
                                    zf = len(h)
                                for zcount,w in enumerate(h[zs:zf]):
                                    for obj in w:
                                        if any(isinstance(obj,AC) for obj in w):
                                            tempcube[xcount][ycount][zcount] = obj.aa
                        flatcube = []
                        for leng in range(len(tempcube)):
                            for hei in range(len(tempcube[leng])):
                                for wid in tempcube[leng][hei]:
                                    flatcube.append(wid)
                        cubelist.append([struc,cube.position,flatcube,call])
    return cubelist
