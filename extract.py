
# new = list()
# for i in range(len(random_transformed)):
#     col = []
#     for j in range(len(random_transformed[1,:])):
#         if type(i) != int:
#             print(i)
#         Fk, n_freq = random_transformed[i,j]
#         try:
#             dom = get_dom_freq(Fk, n_freq)
#             col.append(list(dom))
#             # print col
#         except:
#             print(i,j)
#             break
#     print(len(col))
#     # np.hstack([new, col])

df = DataFrame()
for i in range(len(random_transformed)):
    new = []
    for j in range(len(random_transformed[i])):
        fk, nf = random_transformed[i,j]
        dom = get_dom_freq(fk, nf)
        new.append(dom)
    df = pandas.concat([df, DataFrame(new)])
    # except:
    #     print ('length new', len(new))
    #     print i
    #     break

# list = []
# for i in range(len(random_transformed[1])):
#     fk, nf = random_transformed[1,i]
#     list.append(get_dom_freq(fk,nf))


# new = list()
# for i in range(len(sit_tr)):
#     col = []
#     for j in range(len(sit_tr[1,:])):
#         if type(i) != int:
#             print(i)
#         Fk, n_freq = sit_tr[i,j]
#         # try:
#         dom = get_dom_freq(Fk, n_freq)
#         col.append(list(dom))
#     np.hstack([new, col])
        # except:
        # print(i,j)
