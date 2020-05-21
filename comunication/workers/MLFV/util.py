import cPickle as pickle
import zlib as zl
import base64 as b64
import rpyc.core.brine as br

def deep_getsizeof(o):
    from sys import getsizeof
    from collections import OrderedDict, Mapping, Container
    """Find the memory footprint of a Python object
    This is a recursive function that rills down a Python object graph
    like a dictionary holding nested ditionaries with lists of lists
    and tuples and sets.
    The sys.getsizeof function does a shallow size of only. It counts each
    object inside a container as pointer only regardless of how big it
    really is.
    :param o: the object
    :param ids:
    :return:
    """
    ids=set()
    d = deep_getsizeof
    if id(o) in ids:
        return 0

    r = getsizeof(o)
    ids.add(id(o))

    if isinstance(o, str) or isinstance(0, unicode):
        return r

    if isinstance(o, Mapping):
        return r + sum(d(k, ids) + d(v, ids) for k, v in o.iteritems())

    if isinstance(o, Container):
        return r + sum(d(x, ids) for x in o)

    return r





def compress(o):
    p = pickle.dumps(o)#, pickle.HIGHEST_PROTOCOL)
    z = zl.compress(p, zl.Z_BEST_COMPRESSION)
    e = b64.b64encode(z)
    return e

def decompress(s):
    z = b64.b64decode(e)
    p = zl.decompress(z)
    o = pickle.loads(p)
    return o


def append_dic_par(pars):
    ''' parsers the parameters to a list with par_dictionary '''
    pp = pars.split(',')
    ret = '['
    for i in pp:
        ret+='p[\''+i+'\'],'
    ret = ret[:len(ret)-1]+']'
    return ret



