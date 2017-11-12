from sklearn.decomposition import PCA

# for i in range(10):
#     pca = PCA(n_components = i)
#     pca.fit(X_walk)
#     print pca.explained_variance_ratio_

pca = PCA(n_components = 10)
pca.fit(X_walk)
variance_ratio = pca.explained_variance_ratio_
components = pca.components_

highest = components[0]

sorted = list(reversed(np.argsort(highest))) 
