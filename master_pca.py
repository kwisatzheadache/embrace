import sys
from sklearn.decomposition import PCA
import pprint

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
    X_data = np.array(data[:][window:])
    for i in doms.columns[9:]:
        arrays = np.array([np.array(x) for x in doms[i]])
        X_data = np.hstack([X_data, arrays])
    return X_data



def run_pca(data):
    pca = PCA(n_components = 10)
    pca.fit(data)
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
