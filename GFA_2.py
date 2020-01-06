# validator per file GFA 2.0
# questo programma dato un file in formato .gfa (o .txt) deve controllare se il file rispetta gli standard GFA 2.0
# il formato GFA 2.0 è una generalizzazione del formato GFA 1.0, quindi questo validatore deve essere in grado di controllare
# senza problemi entrambi i formati.

# il validatore NON deve controllare se le istruzioni sono logicamente correte,
# deve SOLO controllare che siano sintatticamente corrette 

import os 
import re 
import json


dictionaryError = {}
errorMex = ''

def main():
    try:
        # GFACompleteFilePath = sys.argv[1] # per ora non lo uso MA credo che sarebbe preferibile utilizzarlo poi
        GFACompleteFilePath = input('Inserire il path completo del file da voler controllare: ')
        # controllo che il path sia valido
        os.path.isfile(GFACompleteFilePath)
        readGFAFileLines(GFACompleteFilePath)
        print(json.dumps(dictionaryError, indent=4, sorted_keys=False))
        print('Programma terminato correttamente')
    except Exception as e: #catcho le eccezzioni e le stampo per capire cos'è andato storto
        print('Qualcosa è andato storto: {}'.format(e))
        os._exit(1)
    
def readGFAFileLines(GFAFilePath):
    with open(GFAFilePath,'r') as GFAFileToCheck:
        lineToCheck = GFAFileToCheck.readline()
        linePointer = 1
        while lineToCheck:
            LineErrorFlag = False
            #stampe di controllo utilizzando il formato json per rendere 
            # tutto piu' leggibile possibile
            print(json.dumps(lineToCheck, indent=4, sort_keys=False))
            rigaSenzaTab = re.split('\t', re.sub('\n','', lineToCheck))            
            print(json.dumps(rigaSenzaTab, indent=4, sort_keys=False))
            headToken = lineToCheck[0]
            if headToken == 'H':
                # la regex dovrebbe essere questa ma non funziona
                regexH = r"H\t([A-Za-z0-9][A-Za-z0-9]:[ABHJZif]:[ -~]*)\w?\t([A-Za-z0-9][A-Za-z0-9]:[ABHJZif]:{-}[0-9]+(,{-}[0-9]+)\w*)\w?\t([A-Za-z0-9][A-Za-z0-9]:[ABHJZif]:[ -~]*)\w*"
                matchH = re.search(regexH, lineToCheck)  
                if not matchH:
                    LineErrorFlag = True
                    errorMex = 'Gli HEADER TAG non sono corretti!' 
            elif headToken == 'S':
                 # la regex dovrebbe essere questa ma non funziona
                regexS = r"S\t[!-~]+\t{-}[0-9]+(*)|[!-~]+\t([A-Za-z0-9][A-Za-z0-9]:[ABHJZif]:[ -~]*)\w*"
                matchS = re.search(regexS, lineToCheck)
                if not matchS:
                    LineErrorFlag = True
                    errorMex = 'I SEGMENT TAG non sono corretti'
            elif headToken == 'F':
                pass
            elif headToken == 'E':
                pass
            elif headToken == 'G':
                pass
            elif headToken == 'O' or headToken == 'U':
                pass
            else:
                pass 
            # gfaErrorHandling o circa
            if LineErrorFlag:
                GFAFileError(dictionaryError, linePointer, lineToCheck, errorMex)
                LineErrorFlag = False
            lineToCheck = GFAFileToCheck.readline()
            linePointer += 1


def GFAFileError(errorDictionary, NRiga, TestoRiga, MessaggioErrore):
    # si potrebbe pure creare una funzione che si occupa di accorpare le righe adiacenti di errore
    # ad esempio se vi e' un errore nella riga 2,3,4,5 accorpare i 4 casi nel dizionario in uno che
    # ha come key riga 2-5 errore
    # pensavo ad una struttura del dizionario come: (key) RIGA: [numero riga], (value) ERRORE
    errorDictionary = dict(Line=NRiga, TextLine=TestoRiga, ErrorMex=MessaggioErrore)

if __name__ == '__main__':
    main()

    



