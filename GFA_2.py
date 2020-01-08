import os           # per controllare l'esistenza di un dato file 
import re           # per poter utilizzare le regex 
import json         # per la formattazione json dell'output
                    # esteticamente gradevole e di piu' facile comprensione
import webbrowser   # per il reindirizzamento web 
                    # totalmente just for fun

# array globale per tenere traccia degli errori presenti nel file
errorsArray = []
# rapida descrizione del programma
disclaimerString = ('\n' + 'Questo programma si occupa di controllare se un determinato '
                    + 'file rispetti o meno la grammatica e semantica di un determinato ' 
                    + 'linguaggio (o formato).' + '\n'
                    + 'Il formato in questione è il Graphical Fragment Assembly (GFA) 2.0.' 
                    + '\n' 
                    + 'Il formato GFA 2.0 è una generalizzazione del formato GFA 1.0, '
                    + 'permette infatti di specificare un grafo di assemblaggio in '
                    + 'maniera meno dettagliata.' + '\n' 
                    + 'Questo non significa che un file in formato GFA 1.0 sia sempre valido '
                    + 'e corretto per il formato GFA 2.0.' + '\n' 
                    + 'Il motivo è che sono state apportate delle modifiche sostanziali '
                    + 'alla struttura del formato come ad esempio:' + '\n' 
                    + '1) aggiunta e rimozione elementi ' + '\n'
                    + '2) aggiunta e rimozione grammatiche ' + '\n'
                    + 'rendendo così un file GFA 1.0 (senza previo adattamento) '
                    + 'non sempre conforme al formato GFA 2.0')

def main():
    try:
        # GFACompleteFilePath = sys.argv[1] # per ora non lo uso MA credo che sarebbe preferibile utilizzarlo poi
        print(disclaimerString)
        risposta = input('Vuoi conoscere tutti i cambiamenti che sono '
                        + 'stati apportati da GFA 1.0 a GFA 2.0?' 
                        + '[Y/N]\n')
        if risposta.upper() == 'Y':
            # indirizzamento (1) verso risorsa github 
            # https://bit.ly/2FsZXrM = https://github.com/GFA-spec/GFA-spec/blob/
                                    # master/GFA2.md#backward-compatibility-with-gfa-1
            webbrowser.open('https://bit.ly/2FsZXrM')
        GFACompleteFilePath = input('\nInserire il path completo del '
                                    + 'file da voler controllare: ')
        # controllo che il path del file sia valido
        os.path.isfile(GFACompleteFilePath)
        # chiamo la funzione che si occupera' di 
        # verificare la conformita' o meno del file
        readGFAFileLines(GFACompleteFilePath)
        # controllo se vi sono errori da visualizzare      
        if not errorsArray:
            print('Il file rispetta il formato GFA 2.0')
        else:
            print('Il file non rispetta il formato GFA 2.0: ')
            print(json.dumps(errorsArray, indent=4))
            risposta = input('\nVuoi conoscere la grammatica GFA 2.0? [Y/N]\n')
            if risposta.upper() == 'Y':
                # indirizzamento (2) verso risorsa github
                # https://bit.ly/36DGXmq = https://github.com/GFA-spec/GFA-spec/
                                        # blob/master/GFA2.md#grammar
                webbrowser.open('https://bit.ly/36DGXmq')            
        print('\nProgramma terminato correttamente.'
                + '\nChiusura programma...')
        os._exit(1)
    # catcho le eccezzioni e le stampo per capire cos'è andato storto
    except Exception as e: 
        print('Errore: {}\nChiusura programma...'.format(e))
        os._exit(1)

# funzione per il controllo della conformita' di un file
# al formato GFA 2.0    
def readGFAFileLines(GFAFilePath):
    # apro il file in modalita' lettura
    with open(GFAFilePath,'r') as GFAFileToCheck:
        lineToCheck = GFAFileToCheck.readline()
        linePointer = 1
        # ciclo su tutte le righe che lo compongono e le analizzo una alla volta
        while lineToCheck:
            LineErrorFlag = False
            headToken = lineToCheck[0]
            # controllo la prima posizione della riga che DEVE essere una tra i seguenti
            # caratteri per essere considerata valida, altrimenti viene ignorata
            # poiche' da progetto, questo permetterebbe all'utente di creare 
            # custom record lines per specifici processi
            if headToken == 'H':
                # regex per il controllo dell' header 
                regexH = r"H(\t\w{2}:[ABHJZif]:[ -~]*)?(\t\w{2}:[ABHJZif]:\d+(\,\d+)*)?(\w{2}:[ABHJZif]:[ -~]*)*"
                matchH = re.search(regexH, lineToCheck)  
                if not matchH:
                    LineErrorFlag = True
            elif headToken == 'S':
                # regex per il controllo del segment
                regexS = r"S(\t[!-~]+)(\t\d+)(\t(\*|[!-~]+))(\t\w{2}:[ABHJZif]:[ -~]*)*"
                matchS = re.search(regexS, lineToCheck)
                if not matchS:
                    LineErrorFlag = True
            elif headToken == 'F':
                # regex per il controllo del fragment 
                regexF = r"F(\t[!-~]+)(\t[!-~]+[+-])(\t\d+\$?){4}(\t((\*)|(\d+[MDIP])+|(\d+(\,\d+)*)))(\t\w{2}:[ABHJZif]:[ -~]*)*"
                matchF = re.search(regexF, lineToCheck)
                if not matchF:
                    LineErrorFlag = True
            elif headToken == 'E':
                # regex per il controllo dell' edge 
                regexE = r"E(\t([!-~]+|\*))(\t[!-~]+[+-]){2}(\t\d+\$?){4}(\t((\*)|(\d+[MDIP])+|(\d+(\,\d+)*)))(\t\w{2}:[ABHJZif]:[ -~]*)*"
                matchE = re.search(regexE, lineToCheck)
                if not matchE:
                    LineErrorFlag = True
            elif headToken == 'G':
                # regex per il controllo del gap
                regexG = r"G(\t([!-~]+|\*))(\t[!-~]+[+-]){2}(\t\d+)(\t(\*|\d+))(\t\w{2}:[ABHJZif]:[ -~]*)*"
                matchG = re.search(regexG, lineToCheck)
                if not matchG:
                    LineErrorFlag = True
            elif headToken == 'O' or headToken == 'U':
                # regex per il controllo dei gruops 
                regexOU = r"(O(\t([!-~]+|\*))((\t[!-~]+[+-])([ ][!-~]+[+-])*)(\t\w{2}:[ABHJZif]:[ -~]*)*)|(U(\t([!-~]+|\*))((\t[!-~]+)([ ][!-~]+)*)(\t\w{2}:[ABHJZif]:[ -~]*)*)"
                matchOU = re.search(regexOU, lineToCheck)
                if not matchOU:
                    LineErrorFlag = True
            else:
                # caso in cui vi sia una riga con un headToken differente da quelli riservati
                # il caso viene ignorato
                pass 
            # gfaErrorHandling o circa
            if LineErrorFlag:
                # inserimento informazioni riguardo l'errore nell' errorsArray
                # printableLine = re.split(r'\t+', lineToCheck.rstrip('\n'))
                errorLine = ('Riga: ' + str(linePointer) + ' Istruzione: ' + lineToCheck) 
                errorsArray.append(errorLine)
                # errorsArray.append(printableLine)
                LineErrorFlag = False
            lineToCheck = GFAFileToCheck.readline()
            linePointer += 1

if __name__ == '__main__':
    main()