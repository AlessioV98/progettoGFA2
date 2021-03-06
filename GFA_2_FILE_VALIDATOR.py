#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib2 import Path       # per controllare l'esistenza di un dato file 
                                # e per raccogliere informazioni a riguardo
import re                       # per poter utilizzare le regex 
import json                     # per la formattazione json dell'output
                                # esteticamente gradevole e di piu' facile comprensione
import webbrowser               # per il reindirizzamento web 
                                # totalmente just for fun

# funzione main 'contenitore' il cui unico scopo e'
# stampare delle info generali durante l'avvio e 
# chiamare successivamente le funzioni adibite al corretto
# funzionamento del programma
def main():
    try:
        # rapida descrizione del programma
        print('\nQuesto programma si occupa di controllare se un determinato '
                + 'file rispetti o meno la grammatica di un determinato ' 
                + 'linguaggio (o formato).' + '\n'
                + 'Il formato in questione è il Graphical Fragment Assembly (GFA) 2.0.')
        # rapida descrizione del formato GFA 2.0
        print('Il formato GFA 2.0 è una generalizzazione del formato GFA 1.0, '
                + 'permette infatti di specificare un grafo di assemblaggio in '
                + 'maniera meno dettagliata.' + '\n') 
        # stampa informazioni riguardo il programma
        PrintInfo()
        # funzione per l'acquisizione di un file
        FileInput()        
    # gestione eccezioni 
    except Exception as e: 
        print('Si è verificato un errore durante l esecuzione del programma: {}'.format(e))
    # termine del programma
    # direttiva dell' OS per la chiusura dell'applicazione
    # la traduzione in ita non mi piace 
    risposta = input('Press ENTER to terminate the program...')
    if risposta:
        raise SystemExit

# funzione per la stampa delle informazioni e redirezione
# verso pagina GitHub del progetto
def PrintInfo():
    # acquisisco la risposta dell'utente
    risposta = input('Vuoi conoscere tutti i cambiamenti che sono '
                    + 'stati apportati da GFA 1.0 a GFA 2.0?' 
                    + '[Y/N]' + '\n')
    if risposta.upper() == 'Y':
        webbrowser.open('https://bit.ly/2FsZXrM')
        # indirizzamento (1) verso risorsa github 
        # https://bit.ly/2FsZXrM = https://github.com/GFA-spec/GFA-spec/blob/
                                # master/GFA2.md#backward-compatibility-with-gfa-1
    risposta = input('Vuoi conoscere la grammatica '
                    + 'del formato GFA 2.0? [Y/N]' + '\n')
    if risposta.upper() == 'Y':
        webbrowser.open('https://bit.ly/36DGXmq')     
        # indirizzamento (2) verso risorsa github
        # https://bit.ly/36DGXmq = https://github.com/GFA-spec/GFA-spec/
                                # blob/master/GFA2.md#grammar

# funzione per l'acquisizione di un file e il controllo della sua esistenza
def FileInput():
    GFAFile = input('\n' + 'Inserire il file da voler controllare: ')
    GFAFilePath = Path(GFAFile).resolve()
    # controllo che il path del file sia valido
    if not GFAFilePath.is_file():
        print('Errore: {} file inesistente'.format(GFAFile))
        risposta = input('Controllare un nuovo file? [Y/N]' + '\n')
        if risposta.upper() == 'Y':
            FileInput()
        return           
    # array per tenere traccia degli errori presenti nel file
    errorsArray = []
    # chiamata funzione per controllo conformita' file
    readGFAFileLines(GFAFilePath, errorsArray)
    # controllo se vi sono errori da visualizzare      
    if not errorsArray:
        print('IL FILE RISPETTA IL FORMATO GFA 2.0')
    elif len(errorsArray) <= 145:
        # stampa errori
        print('IL FILE NON RISPETTA IL FORMATO GFA 2.0: ')
        print(json.dumps(errorsArray, indent=4))
        #print(errorsArray)
    else:
        print('IL FILE NON RISPETTA IL FORMATO GFA 2.0: ' + '\n'
            + 'Essendo un file molto grande, non è possibile visualizzare tutti gli errori '
            + 'per via di una limitazione del CMD sulla lunghezza delle stringhe.')
        risposta = input('Desideri che venga creato un file contenente la lista degli errori? [Y/N]' + '\n')
        if risposta.upper() == 'Y':
            CreateFile(errorsArray, GFAFilePath)    
    # termino il programma correttamente                 
    print('\n' + 'Analisi file terminata correttamente.')
    risposta = input('Controllare un nuovo file? [Y/N]' + '\n')
    if risposta.upper() == 'Y':
        FileInput()
    return

# funzione per la gestione e creazione di file d'errore di grandi dimensioni
def CreateFile(errorsArray, GFAFilePath):
    pathToSave = Path(GFAFilePath).parent
    errorsFile = 'errors_' + Path(GFAFilePath).name + '.txt'
    # creo un nuovo file e ci scrivo dentro
    with open(Path(pathToSave).joinpath(errorsFile), 'w') as tempFile:
        tempFile.writelines(errorsArray)
    print('File creato correttamente nella directory: {} '.format(pathToSave))

# funzione per il controllo della conformita' di un file al formato GFA 2.0    
def readGFAFileLines(GFAFilePath, errorsArray): 
    # controllo che il file non sia vuoto 
    if GFAFilePath.stat().st_size == 0:
        errorsArray.append('FILE VUOTO')
    else:             
        with open(GFAFilePath,'r') as GFAFileToCheck:
            # puntatore alla linea corrente
            lineToCheck = GFAFileToCheck.readline()
            linePointer = 1
            # regex completa
            regex = re.compile(
                '^H(\t\w{2}:[ABHJZif]:[ -~]*)?(\t\w{2}:[ABHJZif]:\-?\d+(\,\-?\d+)*)?(\t\w{2}:[ABHJZif]:[ -~]*)*'                               # regex per il controllo dell' HEADER
                '|^S(\t[!-~]+)(\t\-?\d+)(\t(\*|[!-~]+))(\t\w{2}:[ABHJZif]:[ -~]*)*'                                                            # regex per il controllo dei SEGMENT        
                '|^F(\t[!-~]+){2}[+-](\t\-?\d+\$?){4}\t((\*)|(\d+[MDIP])+|(\-?\d+(\,\-?\d+)*))(\t\w{2}:[ABHJZif]:[ -~]*)*'                     # regex per il controllo dei FRAGMENT
                '|^E(\t([!-~]+|\*))(\t[!-~]+[+-]){2}(\t\-?\d+\$?){4}(\t((\*)|(\d+[MDIP])+|(\-?\d+(\,\-?\d+)*)))(\t\w{2}:[ABHJZif]:[ -~]*)*'    # regex per il controllo degli EDGE
                '|^G(\t([!-~]+|\*))(\t[!-~]+[+-]){2}(\t\-?\d+)(\t(\*|\-?\d+))(\t\w{2}:[ABHJZif]:[ -~]*)*'                                      # regex per il controllo dei GAP
                '|^[OU]\t([!-~]+|\*)(\t([!-~]+[+-]?)([ ][!-~]+[+-]?)*)(\t\w{2}:[ABHJZif]:[ -~]*)*'                                             # regex per il controllo dei GROUP               
                '|^#[\s\w]*')                                                                                                                  # regex per il controllo dei COMMENTI           
            # ciclo per il controllo delle regex su ogni riga del file
            while lineToCheck:
                #match = False               
                match = regex.search(lineToCheck)
                # controllo eventuali righe non conformi 
                if not match:
                    errorsArray.append('RIGA(' + str(linePointer) + '), ' 
                                    + 'ISTRUZIONE[' + lineToCheck + ']')                    
                lineToCheck = GFAFileToCheck.readline()
                linePointer += 1

# inizializzazione main e avvio
if __name__ == "__main__":
    main()