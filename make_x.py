
"""
X_walk is a 2d input vector with shape (30081, 605). It comprises the raw motion data, 33 dominant freqs and coeffs for each axis, and magnitude data.

To be included in the future:
moving average
binned average
bin reduced, recreated signal
"""
df = DataFrame(doms[coords])

for i in df.columns:
    Fks = []
    n_freqs = []
    for j in range(len(df[i])):
        Fk, n_freq = df[i][j]
        Fk = abs(Fk)
        Fks.append(Fk)
        n_freqs.append(n_freq)

    df[i+'coeffs'] = Fks
    df[i+'n_freqs'] = n_freqs


X_walk = DataFrame()
# X_walk[coords] = df[coords]
X_walk['acc_mag'] = doms['acc_mag']
X_walk['mag_mag'] = doms['mag_mag']

expandable = df.drop(coords, axis=1)

columns = X_walk.columns
X_walk = np.array(X_walk)
array_lengths = []
for i in expandable.columns:
    arrays = np.array([np.array(x) for x in expandable[i]])
    array_lengths.append(len(arrays))
    X_walk = np.hstack([X_walk, arrays])
