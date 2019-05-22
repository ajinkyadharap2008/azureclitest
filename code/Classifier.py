import pickle
class Classifier:
    def saveModel(classifier,name):
        f = open( name+'.pickle', 'wb')
        pickle.dump(classifier, f)
        f.close()
       
        
    def loadModel(name):
        f = open(name+'.pickle', 'rb')
        model = pickle.load(f)
        f.close()
        return model
