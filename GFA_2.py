import os 
import re 
import json
import webbrowser # totalmente just for fun


errorsArray = []
disclaimerString = ('\n' + 'Questo programma si occupa di controllare se un determinato file rispetti o meno' +
                    ' la sintassi di un determinato linguaggio.' + '\n' +
                    'Il linguaggio (o formato) in questione è il Graphical Fragment Assembly (GFA) 2.0.' + '\n' +
                    'Il formato GFA 2.0 è una generalizzazione del formato GFA 1.0, permette infatti di specificare un' +
                    ' grafo di assemblaggio in maniera meno dettagliata.' + '\n' +
                    'Questo non significa che un file GFA 1.0 sia sintatticamente valido e corretto per GFA 2.0.' + '\n' +
                    'Il motivo è che sono state apportate delle modifiche alla struttura del formato come:' + '\n' +
                    'aggiunta e rimozione di elementi e regole ' + 
                    'rendendo così un file GFA 1.0 (senza adattamento) non sempre conforme a GFA 2.0')

def main():
    try:
        # GFACompleteFilePath = sys.argv[1] # per ora non lo uso MA credo che sarebbe preferibile utilizzarlo poi
        print(disclaimerString)
        risposta = input('Vuoi conoscere i cambiamenti effettuati da GFA 1.0 a GFA 2.0? [Y/N] ')
        if risposta.upper() == 'Y':
            webbrowser.open('https://github.com/GFA-spec/GFA-spec/blob/master/GFA2.md#backward-compatibility-with-gfa-1')
        GFACompleteFilePath = input('\nInserire il path completo del file da voler controllare: ')
        # controllo che il path sia valido
        os.path.isfile(GFACompleteFilePath)
        readGFAFileLines(GFACompleteFilePath)
        #controllo se vi sono errori da visualizzare      
        if not errorsArray:
            print('Il file rispetta il formato GFA 2.0')
        else:
            print('Il file non rispetta il formato GFA 2.0')
            risposta = input('Vuoi conoscere la grammatica GFA 2.0? [Y/N] ')
            if risposta.upper() == 'Y':
                webbrowser.open('https://github.com/GFA-spec/GFA-spec/blob/master/GFA2.md#grammar')
            print(json.dumps(errorsArray, indent=4))
        print('\nProgramma terminato correttamente.\nChiusura programma...')
        os._exit(1)
    except Exception as e: #catcho le eccezzioni e le stampo per capire cos'è andato storto
        print('Errore: {}\nChiusura programma...'.format(e))
        os._exit(1)
    
def readGFAFileLines(GFAFilePath):
    with open(GFAFilePath,'r') as GFAFileToCheck:
        lineToCheck = GFAFileToCheck.readline()
        linePointer = 1
        while lineToCheck:
            LineErrorFlag = False
            headToken = lineToCheck[0]
            if headToken == 'H':
                # la regex dovrebbe essere questa 
                regexH = r"H(\t\w{2}:[ABHJZif]:[ -~]*)?(\t\w{2}:[ABHJZif]:\d+(\,\d+)*)?(\w{2}:[ABHJZif]:[ -~]*)*"
                matchH = re.search(regexH, lineToCheck)  
                if not matchH:
                    LineErrorFlag = True
            elif headToken == 'S':
                # la regex dovrebbe essere questa 
                regexS = r"S(\t[!-~]+)(\t\d+)(\t(\*|[!-~]+))(\t\w{2}:[ABHJZif]:[ -~]*)*"
                matchS = re.search(regexS, lineToCheck)
                if not matchS:
                    LineErrorFlag = True
            elif headToken == 'F':
                # la regex dovrebbe essere questa 
                regexF = r"F(\t[!-~]+)(\t[!-~]+[+-])(\t\d+\$?){4}(\t((\*)|(\d+[MDIP])+|(\d+(\,\d+)*)))(\t\w{2}:[ABHJZif]:[ -~]*)*"
                matchF = re.search(regexF, lineToCheck)
                if not matchF:
                    LineErrorFlag = True
            elif headToken == 'E':
                # la regex dovrebbe essere questa 
                regexE = r"E(\t([!-~]+|\*))(\t[!-~]+[+-]){2}(\t\d+\$?){4}(\t((\*)|(\d+[MDIP])+|(\d+(\,\d+)*)))(\t\w{2}:[ABHJZif]:[ -~]*)*"
                matchE = re.search(regexE, lineToCheck)
                if not matchE:
                    LineErrorFlag = True
            elif headToken == 'G':
                # la regex dovrebbe essere questa 
                regexG = r"G(\t([!-~]+|\*))(\t[!-~]+[+-]){2}(\t\d+)(\t(\*|\d+))(\t\w{2}:[ABHJZif]:[ -~]*)*"
                matchG = re.search(regexG, lineToCheck)
                if not matchG:
                    LineErrorFlag = True
            elif headToken == 'O' or headToken == 'U':
                # la regex dovrebbe essere questa 
                regexOU = r"(O(\t([!-~]+|\*))((\t[!-~]+[+-])([ ][!-~]+[+-])*)(\t\w{2}:[ABHJZif]:[ -~]*)*)|(U(\t([!-~]+|\*))((\t[!-~]+)([ ][!-~]+)*)(\t\w{2}:[ABHJZif]:[ -~]*)*)"
                matchOU = re.search(regexOU, lineToCheck)
                if not matchOU:
                    LineErrorFlag = True
            else:
                pass 
            # gfaErrorHandling o circa
            if LineErrorFlag:
                error = ('Linea: ' + str(linePointer) 
                        + ' Istruzione: ' + lineToCheck 
                        + ' Non conforme al formato GFA2.')
                errorsArray.append(error)
                LineErrorFlag = False
            lineToCheck = GFAFileToCheck.readline()
            linePointer += 1

if __name__ == '__main__':
    main()

    



