
new = list()
for i in range(len(random_transformed)):
    col = []
    for j in range(len(random_transformed[1,:])):
        if type(i) != int:
            print(i)
        Fk, n_freq = random_transformed[i,j]
        # try:
        #     dom = get_dom_freq(Fk, n_freq)
        #     col.append(list(dom))
        #     np.hstack([new, col])
        # except:
        #     print(i,j)
