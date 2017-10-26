cols = ['acc_x', 'acc_y', 'acc_z', 'gy_x', 'gy_y', 'gy_z', 'mag_x', 'mag_y', 'mag_z'] 

df = DataFrame()
for i in range(len(random_transformed)):
    col = []
    for j in range(len(random_transformed[1,:])):
        if type(i) != int:
            print(i)
        Fk, n_freq = random_transformed[i,j]
        dom = get_dom_freq(Fk, 8)
        freqs = Fk[[dom]]
        col.append(freqs)
    df[cols[i]] = col

