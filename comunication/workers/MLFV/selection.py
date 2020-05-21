from mlfv_constraints import *

class Selection(object):
    constr = MLFVConstraits("timeit,numpy",1000,1,10)
    
    def __init__(self,par): # init must receive a list
        dataset, inputs, class_name = par
        self.dataset = dataset
        self.inputs = inputs
        self.class_name = class_name
        self.name = 'Selection step'

    def run(s):
        print(s.name)
        for i in s.constr.imports.split(','):
            try:
                print ("IMPORTS: ",i)
                exec("import "+i)
            except:
                print("bug")
                return None

        #tempo
        inicio = timeit.default_timer()
        #df
        df = numpy.array(s.dataset)

        # inputs = 'qT','fS','u2','u0'
        inputs = numpy.array(s.inputs)
        inputs = numpy.append(s.class_name, s.inputs)

        # class/ qt / fs / u2 / u0
        data_selected = df[:, inputs]

        # tempo fim
        fim = timeit.default_timer()
        tempo = fim - inicio
        print("-- [Select F.] > Tempo (dentro da funcao) =", tempo)

        return data_selected

        #dataset = pandas.read_json(pickle.loads(zl.decompress(b64.b64decode(s.dataset))), orient='split')
        #dataset = pandas.read_json(s.dataset,orient='split')
        #max = 2000000
        #df = dataset[(dataset['qT'] > 0) & (dataset['fS'] > 0) & (dataset['u2'] > 0) & (dataset['u0'] > 0)]
        #df = dataset[(dataset['qT'] < max) & (dataset['fS'] < max) & (dataset['u2'] < max) & (dataset['u0'] < max)]
        #inputs = numpy.array(s.inputs)
        #inputs = numpy.append(s.class_name,inputs)
        # qt / fs / sv0 / s1v0 / u2 / u0        
        #x = df[inputs]

        #x = x.to_json(orient='split')
        #tempo fim
        #fim = timeit.default_timer()
        #tempo = fim - inicio
        #print("Tempo SELECTION =",tempo)
        
        #return x #tempo, x
