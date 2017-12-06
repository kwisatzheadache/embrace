def autocorr(walk):
    norm = walk - np.mean(walk)
    result = np.correlate(norm, norm, mode='full')
    acorr = result[result.size/2:]
    acorr /= ( walk.var() * np.arange(walk.size, 0, -1))
    return acorr
