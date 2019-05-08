# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 21:58:49 2019

@author: Adam
"""

import Bio
from Bio.PDB import PDBList
pdbl = PDBList()

with open('searchable.tsv','r') as read:
    readfile = read.readlines()
    PDBlist2 = []
    for line in readfile:
        line = line.split('\t')
        PDBlist2.append(line[0])
        
for i in PDBlist2:
    pdbl.retrieve_pdb_file(i,pdir='PDB')