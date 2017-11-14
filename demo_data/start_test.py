import os
import sys
import embrace_metrics as em
import embrace_setup as es

if __name__ == "__main__":
    filename = sys.argv[1]    
    os.system("listen 7011 > " + filename)

    os.system("head -$(wc -l " + filename + " | cut -d' ' -f1) " + filename + " > step_tmp.csv")

    os.system("cp step_tmp.csv " + filename)
    vals = es.get_lists(filename)
    em.calc_step_var(vals)
    os.system("rm step_tmp.csv")
