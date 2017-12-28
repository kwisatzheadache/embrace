def find_steps(walk):
    cols = ['id', 'acc_x', 'acc_y', 'acc_z', 'gy_x', 'gy_y', 'gy_z', 'mag_x', 'mag_y', 'mag_z'] 
    df = DataFrame(walk)
    df.columns = cols
    acc_mag, mag_mag, mag_gy = get_mags(df)
    reduced_gy = reduce_signal(mag_gy)
    gy = [make_auto(mag_gy), make_auto(reduced_gy)]
    maxtab, mintab = peakdet(gy[1], .02)
    ind = maxtab[:, 0]
    ind = ind.astype(int)
    len_btw_steps = [j-i for i, j in zip(ind[:-1], ind[1:])]
    return ind, len_btw_steps
