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
        # acquisisco la risposta dell'utente
        risposta = input('Vuoi conoscere tutti i cambiamenti che sono '
                        + 'stati apportati da GFA 1.0 a GFA 2.0?' 
                        + '[Y/N]\n')
        if risposta.upper() == 'Y':
            # indirizzamento (1) verso risorsa github 
            # https://bit.ly/2FsZXrM = https://github.com/GFA-spec/GFA-spec/blob/
                                    # master/GFA2.md#backward-compatibility-with-gfa-1
            webbrowser.open('https://bit.ly/2FsZXrM')
        GFAFile = input('Inserire il nome del file da voler controllare: ')
        # controllo che il path del file sia valido
        if not os.path.isfile(GFAFile):
            print('Errore: {} File inesistente'.format(GFAFile))
            print('\nChiusura programma...')
            os._exit(1)
        # array per tenere traccia degli errori presenti nel file
        errorsArray = []
        # chiamo la funzione che si occupera' di 
        # verificare la conformita' o meno del file
        # passo l'absolute path del file cosi' da tenere conto
        # anche della possibilita' di gestire non solo path assoluti
        # ma anche relativi o soltanto nomi di file
        readGFAFileLines(os.path.abspath(GFAFile), errorsArray)
        # controllo se vi sono errori da visualizzare      
        if not errorsArray:
            print('IL FILE RISPETTA IL FORMATO GFA 2.0')
        else:
            print('IL FILE NON RISPETTA IL FORMATO GFA 2.0: ')
            print(json.dumps(errorsArray, indent=4))
            risposta = input('Vuoi conoscere la grammatica '
                            + 'del formato GFA 2.0? [Y/N]\n')
            if risposta.upper() == 'Y':
                # indirizzamento (2) verso risorsa github
                # https://bit.ly/36DGXmq = https://github.com/GFA-spec/GFA-spec/
                                        # blob/master/GFA2.md#grammar
                webbrowser.open('https://bit.ly/36DGXmq')            
        print('Programma terminato correttamente.'
                + '\nChiusura programma...')
    # catcho le eccezzioni e le stampo per capire cos'è andato storto
    except Exception as e: 
        print('Errore: {}\nChiusura programma...'.format(e))
    # direttiva dell' OS per la chiusura dell'applicazione
    os._exit(1)

# funzione per il controllo della conformita' di un file
# al formato GFA 2.0    
def readGFAFileLines(GFAFilePath, errorsArray):
    # apro il file in modalita' lettura
    with open(GFAFilePath,'r') as GFAFileToCheck:
        lineToCheck = GFAFileToCheck.readline()
        linePointer = 1
        # inizializzo le variabili regex prima di entrare nel ciclo, 
        # altrimenti farei degli assegnamenti aggiuntivi totalmente inutili
        # all'interno del ciclo di controllo
        # regex per il controllo dell' header 
        regexH = r"H(\t\w{2}:[ABHJZif]:[ -~]*)?(\t\w{2}:[ABHJZif]:\-?\d+(\,\-?\d+)*)?(\w{2}:[ABHJZif]:[ -~]*)*"
        # regex per il controllo del segment
        regexS = r"S(\t[!-~]+)(\t\-?\d+)(\t(\*|[!-~]+))(\t\w{2}:[ABHJZif]:[ -~]*)*"
        # regex per il controllo del fragment 
        regexF = r"F(\t[!-~]+)(\t[!-~]+[+-])(\t\-?\d+\$?){4}(\t((\*)|(\d+[MDIP])+|(\-?\d+(\,\-?\d+)*)))(\t\w{2}:[ABHJZif]:[ -~]*)*"
        # regex per il controllo dell' edge 
        regexE = r"E(\t([!-~]+|\*))(\t[!-~]+[+-]){2}(\t\-?\d+\$?){4}(\t((\*)|(\d+[MDIP])+|(\-?\d+(\,\-?\d+)*)))(\t\w{2}:[ABHJZif]:[ -~]*)*"
        # regex per il controllo del gap
        regexG = r"G(\t([!-~]+|\*))(\t[!-~]+[+-]){2}(\t\-?\d+)(\t(\*|\-?\d+))(\t\w{2}:[ABHJZif]:[ -~]*)*"
        # regex per il controllo dei gruops 
        regexOU = r"[OU](\t([!-~]+|\*))(((\t[!-~]+[+-])([ ][!-~]+[+-])*)|((\t[!-~]+)([ ][!-~]+)*))(\t\w{2}:[ABHJZif]:[ -~]*)*"
        # ciclo su tutte le righe che lo compongono e le analizzo una alla volta
        while lineToCheck:
            # variabile match impostata a true, serve per controllare se non vi sono 
            # match con le regex (quindi errori)
            # impostata inizialmente a true cosi' che se si arriva nel caso della riga da
            # ignorare non venga preso come errore dal controllo successivo
            match = True
            headToken = lineToCheck[0]
            # controllo la prima posizione della riga che DEVE essere una tra i seguenti
            # caratteri per essere considerata valida, altrimenti viene ignorata
            # poiche' da progetto, questo permetterebbe all'utente di creare 
            # custom record lines per specifici processi
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
                # caso in cui vi sia una riga con un headToken differente da quelli riservati
                # il caso viene ignorato e quindi si passa alla riga successiva
                pass 
            # gfaErrorHandling o circa
            if not match:
                # inserimento informazioni riguardo l'errore nell' errorsArray
                errorsArray.append('RIGA(' + str(linePointer) + '), ' 
                                + 'ISTRUZIONE[' + lineToCheck + ']')
                LineErrorFlag = False
            # leggo la riga successiva del file ed incremento 
            # il corrispettivo linePointer
            lineToCheck = GFAFileToCheck.readline()
            linePointer += 1

if __name__ == '__main__':
    main()