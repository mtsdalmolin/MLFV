import rpyc
from MLFV_Hosts import get_host
from util import compress


def send_function(con, obj):
    run = rpyc.utils.classic.teleport_function(con, obj.run)(obj)
    con.close
    return run

def install_lib(lib):
    #subpr...
    pass

def install_lib_rem(con, lib):
    run = rpyc.utils.classic.teleport_function(con, install_lib)(lib)
    con.close
    return run


def exec_chain_function(c, p, ret, obj, pp):
        exec("import " + obj.split('.')[0])  # import the object
        exec('cc=' + obj + '(' + pp + ')')  # create the object with given parameters
        h = get_host(cc)
        print "connecting: ", h[0], h[1]
        con = rpyc.classic.connect(h[0], int(h[1]))
        r=send_function(con, cc)

        if ret != "cla": # cannot compress the classifier
            p[ret]=r
        else: 
            p[ret]=compress(r)



