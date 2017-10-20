def test_window(top, increment):
    for i in range(top/increment):
        win = i * increment + 1
        to_lag = cols[1:-1]
        lagged_walk = lag_set(df_walk, to_lag, win)
        lagged_stand_sit = lag_set(df_stand_sit, to_lag, win)
        lagged_complete = concat([lagged_walk, lagged_stand_sit])
        walk_bin = DataFrame(lagged_complete)
        execfile('binary.py')
        print("Window: %f" % win)
