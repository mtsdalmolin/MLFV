import multiprocessing
from util import *
from MLFV_Manager import exec_chain_function

def parse_chain(c, p, s=0):
    if s==0: #transform p in a multiprocessing dictionary
        p = multiprocessing.Manager().dict(p)
        #p = manager.dict(p)
    s+=1

    if isinstance(c,tuple):
        parse_seq(c,p)
    elif isinstance(c,list):
        parse_par(c,p)
    else:
        print("we got a bug here:", c)


def parse_seq(c, p):
    if isinstance(c,tuple) and len(c) > 1: # a sequential chain with more than one function
        for i in c:
            parse_seq(i,p)
    elif isinstance(c,list):
        parse_par(c,p)
    else:
        ret, obj, pp = parse_chain_obj(c)
        exec_chain_function(c, p, ret, obj, pp)


def parse_par(c, p):
    jobs=[]
    if isinstance(c,list) and len(c) > 1: # a sequential chain with more than one function
        for i in c:
            proc = multiprocessing.Process(target=parse_par,args=(i,p))
            jobs.append(proc)
            proc.start()
        for j in jobs:
            # WAITING Jobs
            j.join()
    elif isinstance(c,tuple):
        parse_seq(c,p)
    else: 
        ret, obj, pp = parse_chain_obj(c)
        exec_chain_function(c, p, ret, obj, pp)


def parse_chain_obj(c):
    ''' Receives a string with the return, object, and parameters, parses it and 
        returns the return variable, the object, and the list with parameters collected from par_dictionary
        Ex.:
          sel = selection.Selection(dataset, columns, class_name)
          returns (  'sel', 'selection.Selection', [p['dataset'],p['columns'],p['class_name']]  ) '''
    if not isinstance(c,str): # is a unary list
        c = c[0]
    c=c.replace(' ','')
    ret,f=c.split('=')
    obj,par=f.split('(')
    par=par.split(')')[0]
    pp = append_dic_par(par)
    return ret, obj, pp

