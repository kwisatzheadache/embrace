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
    return acc_score
