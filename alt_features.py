execfile('functions.py')
execfile('pca_functions.py')


# Check the explained variance ratios with acc_mag and without

csv_dir = 'demo_data/sample_data'
stacked = stack(csv_dir)
dropped = stacked[:,1:]

all_pca = PCA(n_components=10)
all_pca.fit(stacked)
all_variance = all_pca.explained_variance_ratio_

drop_pca = PCA(n_components=10)
drop_pca.fit(dropped)
drop_variance = drop_pca.explained_variance_ratio_
