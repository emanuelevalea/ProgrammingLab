class ExamException(Exception):
    pass

class Diff:
    def __init__(self, ratio=1):
        #controllo che, se l'argormento opzionale "ratio" viene inserito, sia un numero
        if (isinstance(ratio,(float,int))==False):
            raise ExamException("il ratio inserito non è un numero".format(ratio))
        #controllo che il ratio inserito non sia un numero negativo o uguale a 0
        if (ratio<=0):
            raise ExamException ("il ratio inserito non è maggiore di 0")
        self.ratio=ratio

    def compute(self, lista):
       #controllo che la lista non sia vuota
        if not lista:
            raise ExamException ("errore, la lista inserita è vuota")  
        #controllo che la lista non sia un numero o una stringa
        if (isinstance(lista,(float,int,str))==True):
            raise ExamException ("la lista inserita è un numero")
        #controllo che la lista non abbia solo un elemento
        if (len(lista)==1):
            raise ExamException ("errore, la lista ha solamente un elemento, è quindi impossibile calcolare diff") 
        #controllo che la lista contenga solo numeri
        for item in lista:
            if (isinstance(item,(float,int))==False):
                raise ExamException("l'elemento {} non è un numero".format(item))
        result=[]
        for i in range (0,len(lista)-1):
            result.append((lista[i+1]-lista[i])/self.ratio)
            #ritorno una lista con i risultati
        return result
