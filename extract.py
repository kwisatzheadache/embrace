
new = list()
for i in range(len(random_transformed)):
    col = []
    for j in range(len(random_transformed[1,:])):
        Fk, n_freq = random_transformed[i,j]
        dom = get_dom_freq(Fk, n_freq)
        col.append(dom)
        print(dom)
    np.hstack([new, col])
