X_walk = []

# walk_array = np.array(dom_walk[coords])
# for i in range(len(walk_array)):
#     freqs = []
#     coeffs = []
#     for j in range(len(walk_array[i])):
#         Fk, n_freq = walk_array[i,j]
#         for l in range(len(Fk)):
#             coeffs.append(Fk[l])
#             freqs.append(n_freq[l])
#     X_walk.append(inp)
#     X_walk.append(dom_walk['id'][i])

walk_array = np.array(dom_walk[coords])
Fks = []
n_freqs = []
for i in range(len(walk_array)):
    for j in range(len(walk_array[i])):
        Fk, n_freq = walk_array[i,j]
        Fks.append(Fk)
        n_freqs.append(n_freq)

X_walk = np.array(X_walk)

acc_mag, mag_mag = get_mags(walk)
# X_walk['acc_mag'] = acc_mag
# X_walk['mag_mag'] = mag_mag
# X_walk = np.hstack([X_walk, acc_mag, mag_mag])
