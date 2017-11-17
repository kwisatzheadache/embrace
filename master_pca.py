import sys

execfile('functions.py')

# csv_directory = sys.argv[1]
window = 100
num_freqs = 33

# masterset = []
# for filename in os.listdir(csv_directory):
#     features = generate_features(filename, window, doms)
#     masterset.append(features)

# pca = run_pca(masterset)

def generate_features(filename):
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
    X_data = np.array(data)
    for i in doms.columns[9:]:
        arrays = np.array([np.array(x) for x in doms[i]])
        X_data = np.hstack([X_data, arrays])
    return X_data

walk = generate_features('./data/walk.csv')
