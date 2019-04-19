ea_lines = open("Epitope_anno.tsv",'r').read().splitlines()
epi_anno = {}
for e in ea_lines:
	protein = e.split("\t")[0]
	epi_list = [int(p) for p in e.split("\t")[1][1:-1].split(',')]
	epi_anno[protein] = epi_list
