from operator import itemgetter

def test_window(top, increment):
    acc_score = []
    for i in range(top/increment):
        window = i * increment + 1
        to_lag = cols[1:-1]
        lagged_walk = lag_set(df_walk, to_lag, window)
        lagged_stand_sit = lag_set(df_stand_sit, to_lag, window)
        lagged_complete = concat([lagged_walk, lagged_stand_sit])
        walk_bin = DataFrame(lagged_complete)
        execfile('binary.py')
        print("Window: %f" % window)
        acc_score.append({'window': window, 'accuracy': [results.mean(), results.std()]})
    return np.array(acc_score)

def test_means(top, increment):
    for i in range(top/increment):
        window = i * increment + 1
        to_lag = cols[1:-1]
        lagged_stand_sit = lag_set(df_stand_sit, to_lag, window)
        kmeans = KMeans()
        kmeans.fit(lagged_stand_sit)
        print(kmeans.labels_.mean())
        print(DataFrame(kmeans.labels_).describe())

# Can't get dbscan to output anything but -1's.

def test_dbscan(top, increment):
    for i in range(top/increment):
        window = i * increment + 1
        x_es = [1,4,7]
        to_lag = itemgetter(*x_es)(cols)
        lagged_stand_sit = lag_set(df_stand_sit, to_lag, window)
        dbscan = DBSCAN()
        dbscan.fit(lagged_stand_sit)
        print(dbscan.labels_.mean())
        print(DataFrame(dbscan.labels_).describe())
