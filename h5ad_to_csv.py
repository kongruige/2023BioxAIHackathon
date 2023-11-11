import anndata
import pandas as pd
#import numpy as np
# Load the .h5ad file

index=12
for i in range(11):
	adata = anndata.read_h5ad('W{0}.h5ad'.format(index))
	# Create an empty DataFrame
	df = pd.DataFrame(index=adata.var_names)
	# Get the data as a dense matrix
	data_matrix = adata.X.toarray()
	# Transpose the matrix
	data_transposed = data_matrix.T
	# Create DataFrame by providing the transposed data directly
	df = pd.DataFrame(data_transposed, index=adata.var_names, columns=adata.obs_names)
	df.to_csv('Lung_w{0}.csv'.format(index))
	index+=1