# validator per file GFA 2.0
# questo programma dato un file in formato .gfa (o .txt) deve controllare se il file rispetta gli standard GFA 2.0
# il formato GFA 2.0 è una generalizzazione del formato GFA 1.0, quindi questo validatore deve essere in grado di controllare
# senza problemi entrambi i formati.

# il validatore NON deve controllare se le istruzioni sono logicamente correte,
# deve SOLO controllare che siano sintatticamente corrette 

import os 
import re 
import json

#global variable per controllo errori
LineErrorFlag = False
dictionaryError = {}

def main():
    try:
        # assegno alla variabile il nome del file che si vuole controllare 
        # il nome del file e' letto da riga di comando
        # GFACompleteFilePath = sys.argv[1] # per ora non lo uso MA credo che sarebbe preferibile utilizzarlo poi
        GFACompleteFilePath = input('Inserire il path completo del file da voler controllare: ')
        # controllo che il path sia valido
        os.path.isfile(GFACompleteFilePath)
        readGFAFileLines(GFACompleteFilePath)
    except Exception as e: #catcho le eccezzioni e le stampo per capire cos'è andato storto
        print('Qualcosa è andato storto: {}'.format(e))
        os._exit(1)
    
def readGFAFileLines(GFAFilePath):
    # funzione che legge tutto il file riga per riga
    # in base al primo elemento della riga (che identifica che tipo di riga e') 
    # reindirizza alla sottofunzione adatta la riga da che deve essere analizzata
    # le sottofunzioni prendono in input una riga (con o senza tab bisogna vedere come e' comodo)
    # e il numero di riga
    # apro il file e lo leggo
    with open(GFAFilePath,'r') as GFAFileToCheck:
        lineToCheck = GFAFileToCheck.readline()
        linePointer = 1
        while lineToCheck:
            #stampe di controllo utilizzando il formato json per rendere 
            # tutto piu' leggibile possibile
            print(json.dumps(lineToCheck, indent=4, sort_keys=False))
            # rigaSenzaTab = re.split('\t+', rigaConTab)
            rigaSenzaTab = re.split('\t+|\n+', lineToCheck)
            print(json.dumps(rigaSenzaTab, indent=4, sort_keys=False))
            headToken = rigaSenzaTab[0]
            print(headToken)
            # chiamo lo switcher che gestirà poi le sottochiamate a funzione
            findFunction(headToken)
            # errorHandling o circa
            if LineErrorFlag:
                GFAFileError(dictionaryError, linePointer, lineToCheck, errorMex)
                print(json.dumps(dictionaryError, indent=4, sort_keys=False))
            lineToCheck = GFAFileToCheck.readline()
            print(linePointer)
            linePointer += 1

def findFunction(token):
    # non esiste il costrutto switch in python quindi o si usa un if annidato (if... elif... elif.... else)
    # oppure si una un dictionary mapping (questo)
    # o in alternativa si può usare un dispatch method for classes
    switcher = {
        'H': HeaderFunction,
        'S': SegmentFunction,
        'F': FragmentFunction,
        'E': EdgeFunction,
        'G': GapFunction,
        'O': GroupFunction,
        'U': GroupFunction,
    }
    # ottengo la funzione relativa dallo switcher dictionary 
    func = switcher.get(token)
    return func()

def GFAFileError(errorDictionary, NRiga, TestoRiga, MessaggioErrore):
    # si potrebbe pure creare una funzione che si occupa di accorpare le righe adiacenti di errore
    # ad esempio se vi e' un errore nella riga 2,3,4,5 accorpare i 4 casi nel dizionario in uno che
    # ha come key riga 2-5 errore
    # pensavo ad una struttura del dizionario come: (key) RIGA: [numero riga], (value) ERRORE
    errorDictionary = dict(Line=NRiga, TextLine=TestoRiga, ErrorMex=MessaggioErrore)

if __name__ == '__main__':
    main()

    



