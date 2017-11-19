import os
import sys
import pprint
from sklearn.decomposition import PCA

execfile('functions.py')

csv_directory = sys.argv[1]
window = 100
num_freqs = 33

def generate_features(filename, window=100):
    ''' Receives nx10 csv file.
    Transforms data into windows according to pre-declared window size, performs fourier transform, keeps only the dominant frequencies, and creates magnitude values for the acc and mag.

    Output is array shape (x, 409). 

    '''
    print('generating features for ' + filename)
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
    print('features generated for ' + filename)
    print(X_data.shape)
    return X_data

def stack(dir):
    ''' Receives directory of csv files. Generates features on all of them, then stacks the output in shape (x, 409), in preparation for global PCA.
    '''
    files = os.listdir(dir)
    csvs = []
    for x in files:
        if '.csv' in x:
            csvs.append(x)
    complete = np.vstack([generate_features(dir+'/'+x) for x in csvs])
    return complete

def run_pca(data): 
    ''' Runs PCA analysis on dataset. Prints top ten weights for ten components.'''
    print(data.shape)
    pca = PCA(n_components = 10)
    pca.fit(data)
    variance_ratio = pca.explained_variance_ratio_
    components = pca.components_
    highest = components[0]
    for i in components:
        sorted = list(reversed(np.argsort(i)))
        weights = {}
        for j in range(10):
            weights[sorted[j]] = round(i[sorted[j]], 5)
        # print (i[sorted[:10]], sorted[:10])
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(weights)

stacked = stack(csv_directory)
run_pca(stacked)

