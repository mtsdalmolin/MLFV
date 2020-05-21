import sys
import timeit
import numpy as np
import pandas as pd


def get_chain(ds):
    p = {}
    #training parameters
    p['ds_train'] = np.asarray(pd.read_csv("./treino.csv"))
    p['classifier']='RF'
    p['cla_opts']=20

    #selection parameters
    p['dataset'] = np.asarray(pd.read_csv(ds).dropna()) #dropNan
    p['columns']=np.array([1, 2, 3, 6])
    p['class_name']=11
    #preprocessing parameters
    p['scaler']='Standard'

    s0 = "cla = training.Training(ds_train,classifier,cla_opts)"
    s1 = "ret_sel = selection.Selection(dataset, columns, class_name)"
    s2 = "preproc = preprocessing.Preprocessing(ret_sel, scaler)"
    s3 = "pred = testing.Testing(preproc,cla)"
    c=([s0,(s1,s2)],s3)
    return c, p


def send_chain(c,p):
    import timeit
    start = timeit.default_timer()
    import rpyc
    rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

    con = rpyc.connect("localhost", 8888, config = rpyc.core.protocol.DEFAULT_CONFIG)

    con.root.exec_chain(c,p)
    end = timeit.default_timer()
    time = end - start
    print("Total execution time: "+str(time))


def single(ds):
    c,p=get_chain(ds)
    send_chain(c,p)


def multiple(ds,num_par):
    import multiprocessing
    jobs=[]
    c,p=get_chain(ds)
    for i in range(num_par):
        print "Sending",i
        proc = multiprocessing.Process(target=send_chain, args=(c, p))
        jobs.append(proc)
        proc.start()
    for j in jobs:
        print "Waiting for jobs"
        j.join()
        print '%s.exitcode = %s' % (j.name, j.exitcode)


if __name__ == "__main__":
    print sys.argv
    if len(sys.argv) != 3:
        print "Use:", sys.argv[0], "<num_par> for executing multiple chains in parallel"
        single(sys.argv[1])
    else:
        multiple(sys.argv[1],int(sys.argv[2]))

