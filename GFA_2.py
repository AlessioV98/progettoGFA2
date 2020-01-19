import os           # per controllare l'esistenza di un dato file 
                    # e per raccogliere informazioni a riguardo
import re           # per poter utilizzare le regex 
import json         # per la formattazione json dell'output
                    # esteticamente gradevole e di piu' facile comprensione
import webbrowser   # per il reindirizzamento web 
                    # totalmente just for fun

def main():
    try:
        # rapida descrizione del programma
        print('\n' + 'Questo programma si occupa di controllare se un determinato '
                    + 'file rispetti o meno la grammatica e semantica di un determinato ' 
                    + 'linguaggio (o formato).' + '\n'
                    + 'Il formato in questione è il Graphical Fragment Assembly (GFA) 2.0.' 
                    + '\n')

        # rapida descrizione del formato GFA 2.0
        print('Il formato GFA 2.0 è una generalizzazione del formato GFA 1.0, '
                    + 'permette infatti di specificare un grafo di assemblaggio in '
                    + 'maniera meno dettagliata.' + '\n' 
                    + 'Questo non significa che un file in formato GFA 1.0 sia sempre valido '
                    + 'e corretto per il formato GFA 2.0.' + '\n')

        # acquisisco la risposta dell'utente
        risposta = input('Vuoi conoscere tutti i cambiamenti che sono '
                        + 'stati apportati da GFA 1.0 a GFA 2.0?' 
                        + '[Y/N]\n')
        if risposta.upper() == 'Y':
            webbrowser.open('https://bit.ly/2FsZXrM')
            # indirizzamento (1) verso risorsa github 
            # https://bit.ly/2FsZXrM = https://github.com/GFA-spec/GFA-spec/blob/
                                    # master/GFA2.md#backward-compatibility-with-gfa-1
            
        GFAFile = input('Inserire il nome del file da voler controllare: ')
        # controllo che il path del file sia valido
        if not os.path.isfile(GFAFile):
            print('Errore: {} File inesistente'.format(GFAFile))
            print('\nChiusura programma...')
            os._exit(1)

        # array per tenere traccia degli errori presenti nel file
        errorsArray = []
        # chiamata funzione per controllo conformita' file
        readGFAFileLines(os.path.abspath(GFAFile), errorsArray)

        # controllo se vi sono errori da visualizzare      
        if not errorsArray:
            print('IL FILE RISPETTA IL FORMATO GFA 2.0')
        else:
            # stampa errori
            print('IL FILE NON RISPETTA IL FORMATO GFA 2.0: ')
            print(json.dumps(errorsArray, indent=4))
            risposta = input('Vuoi conoscere la grammatica '
                            + 'del formato GFA 2.0? [Y/N]\n')
            if risposta.upper() == 'Y':
                webbrowser.open('https://bit.ly/36DGXmq')     
                # indirizzamento (2) verso risorsa github
                # https://bit.ly/36DGXmq = https://github.com/GFA-spec/GFA-spec/
                                        # blob/master/GFA2.md#grammar
                       
        print('Programma terminato correttamente.'
                + '\nChiusura programma...')

    # gestione eccezioni 
    except Exception as e: 
        print('Errore: {}\nChiusura programma...'.format(e))
    # direttiva dell' OS per la chiusura dell'applicazione
    os._exit(1)

# funzione per il controllo della conformita' di un file
# al formato GFA 2.0    
def readGFAFileLines(GFAFilePath, errorsArray):
    with open(GFAFilePath,'r') as GFAFileToCheck:
        # puntatore alla linea corrente
        lineToCheck = GFAFileToCheck.readline()
        linePointer = 1

        # inizializzo le variabili regex utili per il controllo dei differenti elementi
        # appartenenti al formato GFA 2.0
        regexH = r"H(\t\w{2}:[ABHJZif]:[ -~]*)?(\t\w{2}:[ABHJZif]:\-?\d+(\,\-?\d+)*)?(\w{2}:[ABHJZif]:[ -~]*)*"
        regexS = r"S(\t[!-~]+)(\t\-?\d+)(\t(\*|[!-~]+))(\t\w{2}:[ABHJZif]:[ -~]*)*"
        regexF = r"F(\t[!-~]+)(\t[!-~]+[+-])(\t\-?\d+\$?){4}(\t((\*)|(\d+[MDIP])+|(\-?\d+(\,\-?\d+)*)))(\t\w{2}:[ABHJZif]:[ -~]*)*" 
        regexE = r"E(\t([!-~]+|\*))(\t[!-~]+[+-]){2}(\t\-?\d+\$?){4}(\t((\*)|(\d+[MDIP])+|(\-?\d+(\,\-?\d+)*)))(\t\w{2}:[ABHJZif]:[ -~]*)*"
        regexG = r"G(\t([!-~]+|\*))(\t[!-~]+[+-]){2}(\t\-?\d+)(\t(\*|\-?\d+))(\t\w{2}:[ABHJZif]:[ -~]*)*" 
        regexOU = r"[OU](\t([!-~]+|\*))(((\t[!-~]+[+-])([ ][!-~]+[+-])*)|((\t[!-~]+)([ ][!-~]+)*))(\t\w{2}:[ABHJZif]:[ -~]*)*"
        
        # ciclo per il controllo delle regex su ogni riga del file
        while lineToCheck:
            match = True
            headToken = lineToCheck[0]

            # per essere una linea valida, l'headToken deve essere uno tra i seguenti
            # [H, S, F, E, G, O, U], altrimenti viene ignorata e considerata una riga 
            # commento oppure una riga custom dell'utente per particolari procedure
            if headToken == 'H':                
                match = re.search(regexH, lineToCheck)  
            elif headToken == 'S':               
                match = re.search(regexS, lineToCheck)
            elif headToken == 'F':
                match = re.search(regexF, lineToCheck)
            elif headToken == 'E':
                match = re.search(regexE, lineToCheck)
            elif headToken == 'G':
                match = re.search(regexG, lineToCheck)
            elif headToken == 'O' or headToken == 'U':
                match = re.search(regexOU, lineToCheck)
            else:
                pass 

            # controllo eventuali righe con non conformi 
            if not match:
                errorsArray.append('RIGA(' + str(linePointer) + '), ' 
                                + 'ISTRUZIONE[' + lineToCheck + ']')
                LineErrorFlag = False
                
            lineToCheck = GFAFileToCheck.readline()
            linePointer += 1

if __name__ == '__main__':
    main()