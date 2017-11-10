execfile('import.py')

"""
X_walk is a 2d input vector with shape (30081, 605). It comprises the raw motion data, 33 dominant freqs and coeffs for each axis, and magnitude data.

To be included in the future:
moving average
binned average
bin reduced, recreated signal
"""
df = DataFrame(dom_walk[coords])

for i in df.columns:
    Fks = []
    n_freqs = []
    for j in range(len(df[i])):
        Fk, n_freq = df[i][j]
        Fks.append(Fk)
        n_freqs.append(n_freq)

    df[i+'coeffs'] = Fks
    df[i+'n_freqs'] = n_freqs

acc_mag, mag_mag = get_mags(dom_walk)

X_walk = DataFrame()
X_walk[coords] = df[coords]
X_walk['acc_mag'] = acc_mag
X_walk['mag_mag'] = mag_mag

expandable = df.drop(coords, axis=1)

X_walk = np.array(X_walk)
for i in expandable.columns:
    arrays = np.array([np.array(x) for x in expandable[i]])
    X_walk = np.hstack([X_walk, arrays])
