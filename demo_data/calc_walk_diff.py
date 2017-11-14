#!/usr/bin/python
import embrace_setup as es
import embrace_metrics as em
import sys
vars = es.get_lists(sys.argv[1])
em.calc_step_var(vars)
