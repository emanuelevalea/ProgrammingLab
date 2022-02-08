#importo "re" per estrarre dei valori in caso di linea errata
import re 

class ExamException(Exception): 
    pass

class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name
    
    def get_data(self):
        
        #controllo che il file si possa aprire e leggere
        try:
            openedfile = open(self.name, 'r')
            openedfile.readline()
        except:
            raise ExamException ("Errore in apertura del file")
            return None
            

        #creo una lista per salvare il risultato
        result = []
        #creo una lista per salvare le date, per poi poter controllarle
        dates = []
        for line in openedfile:
            #creo una lista "new" che sarà l'elemento della lista "result"
            new = []
            datas = line.split(',',1)
            if (datas[0] != 'date'):
                new.append(datas[0])
                dates.append(datas[0])
                
                #controllo che il dato sia un numero intero positivo, altrimenti lo salto
                if (datas[1].strip().isnumeric() == True and int(datas[1]) > 0):
                    new.append(int(datas[1]))
                else:
                    print ("Errore in conversione del valore: {}".format(datas[1])) 
                    #se vi è un numero accompagnato da altre cose uso "re" per estrarre il numero
                    numbers = re.findall(r'\d+', str(datas[1]))
                    if (len(numbers) == 1 and int(numbers[0]) > 0):
                        new.append(int(numbers[0]))

                result.append(new)
        
        openedfile.close()

        #controllo che il file non sia vuoto
        if (len(dates) == 0):
            raise ExamException ("Il file inserito è vuoto")
            
        #controllo che il totale delle date sia un multiplo di 12
        if (len(dates)%12 != 0 or len(dates) == 0):
            raise ExamException ("Il totale di date non è divisibile per 12")
            
        #controllo che la stessa data non si ripeta
        for item in dates:
            if (dates.count(item) > 1):
                raise ExamException ("La data seguente è ripetuta:{}".format(item))

        #controllo che mesi e anni siano scritti correttamente
        years = []
        months = []
        for item in dates:
            dates1 = item.split("-")
            #controllo che vi sia mese e anno soltanto
            if (len(dates1) != 2):
                raise ExamException ("La seguente linea è scritta erroneamente: {}".format(item))
            #controllo che vi siano numeri
            if (dates1[0].isnumeric() == False or dates1[1].isnumeric() == False ):
                raise ExamException ("L'anno seguente non è corretto: {}".format(item))
            #controllo che i mesi inseriti siano corretti
            if (int(dates1[1]) > 12 or int(dates1[1]) < 1):
                raise ExamException ("Il mese seguente non è corretto: {}".format(item.split("-")[1]))

            years.append(int(dates1[0]))
            months.append(int(dates1[1]))

        #controllo che i mesi e gli anni siano in ordine attraverso un iteratore 
        previous_month = 0
        previous_year = years[0]-1
        i = 0
        for item in dates:
            if (i%12 == 0):
                if (months[i] != 1 or years[i] != previous_year + 1):
                    raise ExamException ("Vi è una incongruenza nella data: {}".format(dates[i]))
                else:
                    previous_year = years[i]
            elif (months[i] != previous_month + 1 or years[i] != previous_year):
                    raise ExamException ("Vi è una incongruenza nella data: {}".format(dates[i]))
            previous_month = months[i]
            i = i + 1
    
        return result

def compute_avg_monthly_difference(time_series, first_year, last_year):
    
    #controllo l'input: "first_year" e "last_year"
    if (isinstance(first_year, str) == False or isinstance(last_year, str) == False):
        raise ExamException ("Una delle due date inserite non è una stringa")

    if (first_year.isnumeric() == False or last_year.isnumeric() == False):
        raise ExamException ("Una delle due date inserite non è corretta")

    if (int(first_year) > int(last_year)):
        raise ExamException("il primo anno è maggiore dell'ultimo")
    
    #vedo se gli anni inseriti sono nel file
    first_year_found = False
    last_year_found = False

    for item in time_series:
        if (first_year == (item[0].split("-"))[0]):
            first_year_found = True
        if (last_year ==  (item[0].split("-"))[0]):
            last_year_found = True
        if (first_year_found == True and last_year_found == True):
            break

    if (first_year_found ==  False or last_year_found == False):
        raise ExamException("Uno dei due anni inseriti non appartiene al file")

    #calcolo il risultato salvandolo su una lista
    result = []
    year_index = 0
    year_found = False
    while(year_found == False):
        #controllo se mi trovo o no sul "first_year"
        year_searching = time_series[year_index][0].split("-")
        if (first_year == year_searching[0]):
            for x in range(0,12):
                result.append(0.0)
                #creo un indice per iterare sui diversi mesi
                month_index = x + year_index
                #creo una lista per aggiungere ogni valore di un mese per gli anni considerati
                month_values = []
                for i in range (int(first_year) , int(last_year) + 1):
                    if (len(time_series[month_index]) > 1):
                        month_values.append(time_series[month_index][1])
                    month_index = month_index + 12
                    
                #controllo che i valori per un singolo mese siano più di uno
                if (len(month_values) > 1):
                    previous_month_value = None
                    #trovo la somma delle differenze
                    for item in month_values:
                        
                        if (previous_month_value != None):
                            result[x] = result[x] + (item - previous_month_value)
                        previous_month_value = item
                    #faccio la media delle differenze
                    result[x] = result[x] / (len(month_values) - 1)
                #avendo trovato l'anno interrompo il while
            year_found = True
        #in caso in cui non lo abbia trovato vado all'anno successivo
        else:
            year_index = year_index + 12   
            
    return result
