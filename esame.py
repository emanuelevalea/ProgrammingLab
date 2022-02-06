#importo "re" per estrarre dei numeri
import re
#creo la classe per i vari errori
class ExamException(Exception):
    pass

#creo la classe CSVTimeSeriesFlies
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

        #creo una lista dove salvare le date, per poi controllarle, e una per salvare il risultato
        result=[]
        dates=[]
        for line in openedfile:
            #creo una lista "new" che sarà l'elemento della lista "result"
            new=[]
            datas=line.split(',')
            if (datas[0]!='date'):
                new.append(datas[0])
                dates.append(datas[0])
                #controllo che il valore sia un numero positivo, altrimenti lo salto
                try: 
                    x=int(datas[1])
                except:
                    print("Errore in conversione del valore: {}".format(datas[1])) 
                    #se vi è un numero accompagnato da altre cose uso "re" per estrarre il numero
                    numbers=re.findall(r'\d+',str(datas[1]))
                    if (len(numbers)==1):
                        new.append(int(numbers[0]))
                #controllo che il numero sia positivo
                if (x>0):
                    new.append(x)
                else:
                    print("il valore seguente non è un numero positivo: {}".format(datas[1]))
                result.append(new)

        #controllo che il totale delle date sia un multiplo di 12
        if (len(dates)%12!=0):
            raise ExamException("Il totale di date non è divisibile per 12")
        #controllo che la stessa data (anno e mese) non sia stata inserita più volte
        for item in dates:
            if (dates.count(item)>1):
                raise ExamException("La data seguente è ripetuta:{}".format(item))

        years=[]
        months=[]
        #controllo che mesi e anni siano scritti correttamente
        for item in dates:
            try:
                dates1=item.split("-",1)
            except:
                raise ExamException("La seguente linea è scritta erroneamente: {}".format(item))
            try:
                years.append(int(dates1[0]))
            except:
                raise ExamException("L'anno seguente non è corretto: {}".format(dates1[0]))              
            try:
                months.append(int(dates1[1]))
            except:
                raise ExamException("Il mese seguente non è corretto:{}".format(dates1[1]))
            #controllo che i mesi inseriti siano corretti
            if (int(dates1[1])>12 or int(dates1[1])<1):
                raise ExamException("Il mese seguente non è corretto: {}".format(dates1[1]))
        #controllo che il totale dei mesi sia un multiplo di 12
        if (len(dates)%12!=0):
            raise ExamException("Il totale di mesi non è divisibile per 12")

        #controllo che i mesi e gli anni siano in ordine attraverso un iteratore 
        previous_month=0
        previous_year=years[0]-1
        i=0
        for item in dates:
            if(i%12==0):
                if(months[i]!=1 or years[i]!=previous_year+1):
                    raise ExamException("Vi è una incongruenza nella data: {}".format(dates[i]))
                else:
                    previous_year=years[i]
            elif(months[i]!=previous_month+1 or years[i]!=previous_year):
                    raise ExamException("Vi è una incongruenza nella data: {}".format(dates[i]))
            previous_month=months[i]
            i=i+1
 
        return result

def compute_avg_monthly_difference(time_series, first_year, last_year):

    #controllo l'input: "first_year" e "last_year"
    if (isinstance(first_year, str)==False or isinstance(last_year, str)==False):
        raise ExamException ("Una delle due date inserite non è una stringa")
    try:
        firstyear=int(first_year)
    except:
        raise ExamException("La seguente data inserita è errata: {}".format(first_year))
    try:
        lastyear=int(last_year)
    except:
        raise ExamException("La seguente data inserita è errata: {}".format(last_year))
    if (firstyear>=lastyear):
        raise ExamException("le due date inserite sono uguali o la prima è maggiore dell'ultima")
    

    #trovo tutti gli anni disponibili
    years=[]
    while (firstyear<=lastyear):
        years.append(str(firstyear))
        firstyear=firstyear+1
    
    #creo due liste, in una salvo i valori, nell'altra gli anni
    data=[]
    values=[]
    for y in range (0, len(time_series)):
        data1=time_series[y][0].split('-')
        data.append(str(data1[0]))
        #se un valore non è esistente inserisco -1 per riconoscerlo in futuro
        if (len(time_series[y])>1):
            values.append(float(time_series[y][1]))
        else:
            values.append(-1)
    
    #controllo che gli anni inseriti siano nel file
    for item in years:
        if (data.count(item)==0):
            raise ExamException ("l'anno {} non è compreso nel file".format(item))
    
    result=[]
    #creo un for per immettere i risultati
    for x in range(0,12):
        #inizializzo ogni risultato a 0
        result.append(0.0)
        #creo un indice per iterare sui vari anni
        year_index=x
        year_found=False
        while(year_found==False):
            if (years.count(data[year_index])!=0):
                #creo un indice per iterare sui diversi mesi
                month_index=year_index
                #salvo su una lista i valori di quel mese
                month_values=[]
                for item in years:
                    if (values[month_index]!=-1):
                        month_values.append(values[month_index])
                    month_index=month_index+12
                #controllo che i valori per un singolo mese siano più di uno, altrimenti ritorno 0
                if (len(month_values)>1):
                    previous_month_value=None
                    #trovo la somma delle differenze
                    for item in month_values:
                        if (previous_month_value!=None):
                            result[x]=result[x]+(item-previous_month_value)
                        previous_month_value=item
                    #faccio la media delle differenze
                    result[x]=result[x]/(len(month_values)-1)
                #avendo trovato l'anno interrompo il while
                year_found=True
            #in caso in cui non lo abbia trovato vado all'anno successivo
            else:
                year_index=year_index+12
            
    return result