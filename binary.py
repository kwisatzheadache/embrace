from sklearn.cluster import KMeans

y_all = concat([y_walk, y_sit, y_stand], axis=0)

kmeans = KMeans(n_clusters=3)
X = y_all[coords]
X = np.array(X)

kmeans.fit(X)
predicts = kmeans.predict(X)
