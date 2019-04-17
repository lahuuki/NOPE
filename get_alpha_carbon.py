import sys
import pandas as pd

class AC(object):
	def __init__(self, position, aa, x=0, y=0, z=0, b=0):
		self.position = int(position)
		self.aa = aa
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)
		self.b = float(b)
	
	def __str__(self):
		return f"{self.position}:{self.aa}\t({self.x},{self.y},{self.z})\tb={self.b}"
		

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

# my_acs = get_alpha_carbon(my_pdb, my_bf)
# for a in my_acs:
	# print(a)
	
test_aa = ['A', 'R', 'N', 'D', 'C', 'E', 'Q']	
test_alphas_1D = []
for i,aa in enumerate(test_aa):
	test_alphas_1D.append(AC(i,aa,i))
	
for a in test_alphas_1D:
	print(a)

build_grid_1D(test_alphas_1D,1,2)
