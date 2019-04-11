import sys

class AC(object):
	def __init__(self, position, aa, x, y, z, b):
		self.position = int(position)
		self.aa = aa
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)
		self.b = float(b)
	
	def __str__(self):
		return f"{self.position}:{self.aa}\t({self.x},{self.y},{self.z})\tb={self.b}"
		

def get_alpha_carbon(pdb_fn, b_factor):  
	"""Input is pdb filename and B-factor cut off returns list of AC objects that have a B-factor below the cutoff value."""
	pd_lines = [l.split() for l in open(pdb_fn, "r").read().splitlines()]
	pdb_alpha = [AC(l[5],l[3],l[6],l[7],l[8],l[-2]) for l in pd_lines if l[0] == 'ATOM' and l[2] == 'CA']
	# print(len(pdb_alpha))
	# for ac in pdb_alpha:
		# print(ac)
	
	return [a for a in pdb_alpha if a.b <= b_factor]
	
my_pdb = sys.argv[1]
my_bf = float(sys.argv[2])

my_acs = get_alpha_carbon(my_pdb, my_bf)
for a in my_acs:
	print(a)