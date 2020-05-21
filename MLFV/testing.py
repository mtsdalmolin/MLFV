from mlfv_constraints import *


class Testing(object):        

    constr = MLFVConstraits("timeit,numpy,sklearn.ensemble",1000,2,10)  #sklearn.metrics

    def __init__(self, pars):
        dataset, classificator = pars
        self.dataset = dataset        
        self.classificator = classificator
        #self.size = sys.getsizeof(dataset)+sys.getsizeof(classificator)+sys.getsizeof(epochs)
        self.name = 'Testing step'
    
    def run(s):
        for i in s.constr.imports.split(','):
            #print("IMPORT:",i)
            try:
                exec("import "+i)
            except:
                print("bug")
                return None

        df = numpy.array(s.dataset) #pandas.read_json(s.dataset,orient='split')
        #tempo
        inicio = timeit.default_timer()        

        print(s.name)

        #c = decompress(s.classificator)
        #e = s + "=" * (-len(s.classificator) % 4)

        pk_time = timeit.default_timer()
        import cPickle as pickle, zlib as zl, base64 as b64

        c = pickle.loads(zl.decompress(b64.b64decode(s.classificator)))
        #print(c)
        #c = pickle.loads(s.classificator)

        fim = timeit.default_timer()
        tempo = fim - pk_time
        print(">>>DESCOMPRESS =", tempo)

        #atribui os valores ja separados
        my_X = df[:, 1:]  # dataset[dataset.columns[1:]].values
        my_Y = df[:, 0]  # dataset[dataset.columns[0]].values

        #classif= sklearn.ensemble.RandomForestClassifier(n_estimators=20)
        
        #print "  Fitting classifier..."
        #c = classif.fit(my_X, my_Y)
        
        y_pred = c.predict(my_X)
        precision,recall,fscore,support = sklearn.metrics.precision_recall_fscore_support(my_Y,y_pred)

        fim = timeit.default_timer()
        tempo = fim - inicio
        print("--[Testing F.]=",tempo)
        print(precision,recall,fscore,support)
        return [precision,recall,fscore,support]
    

