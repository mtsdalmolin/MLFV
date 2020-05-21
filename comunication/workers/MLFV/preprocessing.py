from mlfv_constraints import *


class Preprocessing(object):
    constr = MLFVConstraits("timeit,numpy,sklearn.preprocessing",1000,2,10)

    def __init__(self, par):
        dataset, scaler = par
        self.dataset = dataset
        self.scaler = scaler
        #self.size = sys.getsizeof(dataset) + sys.getsizeof(scaler)
        self.name = 'Preprocessing step'

    def run(s):
        for i in s.constr.imports.split(','):
            try:
                exec("import "+i)
            except:
                print("bug")
                return None

        print(s.name)

        # tempo
        inicio = timeit.default_timer()
        df = numpy.array(s.dataset) #pandas.read_json(s.dataset, orient='split')
        x = df[:,1:]
        y = df[:,0]

        if s.scaler == 'Standard':
            sc = sklearn.preprocessing.StandardScaler()
        elif s.scaler == 'MinMax':
            sc = sklearn.preprocessing.MinMaxScaler()

        x_scaled = sc.fit_transform(x)
        x_norm = x_scaled
        #x_norm.columns = x.columns

        new_df = numpy.column_stack((y,x_norm))#pandas.concat([y, x_norm], axis=1)

        # tempo fim
        fim = timeit.default_timer()
        tempo = fim - inicio
        print("--[Preproc. F.]=", tempo)

        return new_df
