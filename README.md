# NOPE
Neural net Optimized for Predicting Epitopes 
Huuki, L. and Karami, A.

A neural network approach to predicting amino acids in a protein that are likely to be epitopes.

allgrids_data/allgrids_AA_charge13_test.zip contains a sample of the input data used to build the model. The other files are too large

How to run:
1. Get PDB structures using getall_data.py, with a file with a list of protein structures and their epitope annotations. An example of this file is searchable_2.tsv
2. From a list of protein structures and their annotations, run get_cd.py and subsequently get_cd_refined.py to get optimal dimension parameters for the run 
3. Run make_allgrids_charged.py on the file resulting from #2 to create matrices for each protein structure and submatrices for each of their amino acids. Results will be pickled into 'allgrids_AA_charge{radius}.p'
4. Run create_models.py, this will create a 2 layer nueral net for each dataset, training data will be excluded as saved as pickle file
5. Run test_models.py to evaluate the accuracy of each model on the training data, results are ouput to a csv file
6. Using NOPE.py with a pdb filnme input, individual proteins can be run thorugh the most accurate model we developed annotating each individual amino acid. 
