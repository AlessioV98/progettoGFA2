# validator per file GFA 2.0
# questo programma dato un file in formato .gfa (o .txt) deve controllare se il file rispetta gli standard GFA 2.0
# il formato GFA 2.0 è una generalizzazione del formato GFA 1.0, quindi questo validatore deve essere in grado di controllare
# senza problemi entrambi i formati.

# il validatore NON deve controllare se le istruzioni sono logicamente correte,
# deve SOLO controllare che siano sintatticamente corrette 

from collections import Counter
import sys 
import os 
import re 
import json

# assegno alla variabile il nome del file che si vuole controllare 
# il nome del file e' letto da riga di comando
# GFACompleteFilePath = sys.argv[1] # per ora non lo uso MA 
GFACompleteFilePath = input('Inserire il path completo del file da voler controllare: ')
# controllo che il path sia valido
if not os.path.isfile(GFACompleteFilePath):
    print("File path {} inesistente. Chiusura scrupt .py... ".format(GFACompleteFilePath))
    sys.exit()
#apro il file e lo leggo
with open(GFACompleteFilePath,'r') as GFAFileToCheck:
    lineToCheck = GFAFileToCheck.readline()
    linePointer = 1
    while lineToCheck:
        #stampe di controllo utilizzando il formato json per rendere 
        # tutto piu' leggibile possibile
        print(json.dumps(lineToCheck, indent=4, sort_keys=False))
        lineToCheck = GFAFileToCheck.readline()
        linePointer += 1
    # rigaSenzaTab = re.split(r'\t+', rigaConTab)
    # per leggere riga per riga dalla variabile GFAFileToCheck si puo' utilizzare un ciclo for

    # funzione che legge tutto il file riga per riga
    # in base al primo elemento della riga (che identifica che tipo di riga e') 
    # reindirizza alla sottofunzione adatta la riga da che deve essere analizzata
    # le sottofunzioni prendono in input una riga (con o senza tab bisogna vedere come e' comodo)
    # e il numero di riga, ritorna TRUE se non vi sono problemi, FALSE altrimenti
    # dopo ogni chiamata a sottofunzione si controlla se la variabile flagNoErrors e' false
    # se e' cosi' si aggiunge ad un dizionario la riga (come key) e il fatto che vi sia stato riscontrato un errore
    # altrimenti non si fa nulla, poi si incrementa il contatore riga, si passa a quella dopo e si va avanti cosi'
    # una volta letta l'ultima riga del file, si mostra a display il risultato, stampando il
    # errorDictionary se non fosse vuoto (quindi contenente errori) oppure un messaggio tipo 
    # 'File corretto'

    # si potrebbe pure creare una funzione che si occupa di accorpare le righe adiacenti di errore
    # ad esempio se vi e' un errore nella riga 2,3,4,5 accorpare i 4 casi nel dizionario in uno che
    # ha come key riga 2-5 errore
    # pensavo ad una struttura del dizionario come: (key) RIGA: [numero riga], (value) ERRORE

    



