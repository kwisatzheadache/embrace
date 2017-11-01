from sklearn.neighbors import KNeighborsClassifier
joined = pd.concat([walk, sit, stand])
X = joined.drop(walk.columns[[0,10]], axis=1)
Y = joined['y']

neigh = KNeighborsClassifier()
neigh.fit(X,Y)

unlabeled = random.drop(['id'], axis=1)
predicted = neigh.predict(unlabeled)

