from mlfv_constraints import *

class Training(object):        
    constr = MLFVConstraits("timeit,numpy,sklearn.ensemble",1000,2,10)
        
    def __init__(self, pars):
        dataset, classificator, cla_opts = pars
        self.dataset = dataset        
        self.classificator = classificator
        self.cla_opts = cla_opts       
        #self.size = sys.getsizeof(dataset)+sys.getsizeof(classificator)+sys.getsizeof(epochs)
        self.name = 'Training step'
    
    def run(s):
        for i in s.constr.imports.split(','):
            #print(i)
            try:
                exec("import "+i)
            except:
                print("bug")
                return None


        #import cPickle as pickle, zlib as zl, base64 as b64

        #tempo
        inicio = timeit.default_timer()

        df = numpy.array(s.dataset)  # pandas.read_json(s.dataset, orient='split')

        print(s.name)

        c = s.classificator
        #n_repeats = 10

        ####TODO: Allow other classifiers
        if s.classificator == "RF":
            #classif= sklearn.ensemble.RandomForestClassifier(n_estimators=s.cla_opts)
            import sklearn.neural_network
            classif = sklearn.neural_network.MLPClassifier(solver='lbfgs', activation='tanh', alpha=1e-5, hidden_layer_sizes=(150, 15),
                                    max_iter=200, random_state=1)
        
        #atribui os valores ja separados
        my_X = df[:,1:]#dataset[dataset.columns[1:]].values
        my_Y = df[:,0]#dataset[dataset.columns[0]].values

        #print "  Fitting classifier..."
        c = classif.fit(my_X, my_Y)
        fim = timeit.default_timer()
        tempo = fim - inicio
        print("--[Training F.]=",tempo)

        return c
    

