X_walk = []

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

X_walk = np.array(X_walk)

acc_mag, mag_mag = get_mags(dom_walk)
df['acc_mag'] = acc_mag
df['mag_mag'] = mag_mag
