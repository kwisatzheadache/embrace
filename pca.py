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


for i in components:
    sorted = list(reversed(np.argsort(i)))
    weights = {}
    for j in range(10):
        weights[sorted[j]] = i[sorted[j]] 
    # print (i[sorted[:10]], sorted[:10])
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(weights)
