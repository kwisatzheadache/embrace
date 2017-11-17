window = 100
num_freqs = 33

filename = ('./data/walk.csv')

data = get_nx10(filename)
doms = data_transform(data, window, num_freqs)
coords = doms.columns[:9]
for i in coords:
    Fks = []
    n_freqs = []
    for j in range(len(doms[i])):
        Fk, n_freq = doms[i][j]
        Fk = abs(Fk)
        Fks.append(Fk)
        n_freqs.append(n_freq)

    doms[i+'coeffs'] = Fks
    doms[i+'n_freqs'] = n_freqs
doms = doms.drop(coords, axis=1)
columns = data.columns
X_data = np.array(data[:][100:])
for i in doms.columns[9:]:
    arrays = np.array([np.array(x) for x in doms[i]])
    X_data = np.hstack([X_data, arrays])


# expandable = df.drop(coords, axis=1)

# columns = X_walk.columns
# X_walk = np.array(X_walk)
# array_lengths = []
# for i in expandable.columns:
#     arrays = np.array([np.array(x) for x in expandable[i]])
#     array_lengths.append(len(arrays))
#     X_walk = np.hstack([X_walk, arrays])
