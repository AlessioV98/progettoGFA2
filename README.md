# VALIDATORE PER FILE GFA 2.0
Questo e' un progetto universitario, sviluppato da:

1. Morlacchi Giorgia     matricola 797741
2. Stievano Matteo       matricola 829535
3. Villani Alessio       matricola 830075

in cui si cerca di sviluppare un validatore per file in formato **G**raphical **F**ragment **A**ssembly (**GFA**) versione 2.0.
Questo significa che dato un file, si controlla se il suo contenuto e' conforme alle regole grammaticali del formato GFA 2.0 mediante l'uso di **REGEXP**.

## GRAMMATICA GFA 2.0
La grammatica di un file GFA 2.0 e' la seguente: 

```
<file>     <- ( <header> | <segment> | <fragment> | <edge> | <gap> | <group> )+

<header>   <- H {VN:Z:2.0} {TS:i:<trace spacing>} <tag>*

<segment>  <- S <sid:id> <slen:int> <sequence> <tag>*

<fragment> <- F <sid:id> <external:ref>
                  <sbeg:pos> <send:pos> <fbeg:pos> <fend:pos> <alignment> <tag>*

<edge>     <- E <eid:opt_id> <sid1:ref> <sid2:ref>
                          <beg1:pos> <end1:pos> <beg2:pos> <end2:pos> <alignment> <tag>*

<gap>      <- G <gid:opt_id> <sid1:ref> <sid2:ref> <dist:int> (* | <var:int>) <tag>*

<group>    <- <o_group> | <u_group>

  <o_group>  <- O <oid:opt_id> <ref>([ ]<ref>)* <tag>*
  <u_group>  <- U <uid:opt_id>  <id>([ ]<id>)*  <tag>*

    <id>        <- [!-~]+
    <ref>       <- <id>[+-]
    <opt_id>    <- <id> | *

    <tag>       <- [A-Za-z0-9][A-Za-z0-9]:[ABHJZif]:[ -~]*

    <pos>       <- <int>{$}
    <int>       <- {-}[0-9]+

    <sequence>  <- * | [!-~]+
    <alignment> <- * | <trace> | <CIGAR>

      <CIGAR> <- ([0-9]+[MDIP])+
      <trace> <- <int>(,<int>)*
```

Dove i simboli **<>** indicano dei **token** mentre il simbolo **<-** indica una **derivazione** ovvero che l'elemento a **sinistra** del simbolo **<-** viene derivato come cio' che e' a **destra**.

Esempio di derivazione:
```
<header> <- H {VN:Z:2.0} {TS:i:<trace spacing>} <tag>*
Il tag <header> e' composto (si deriva) dagli elementi:
    + H simbolo all'inizio della stringa
    + {VN:Z:2.0} elemento opzionale
    + {TS:i:<trace spacing>} elemento composto opzionale contenente
        + <trace spacing> token 
    + <tag>* token che puo' ripetersi 0 oppure N volte 
```

Gli altri simboli presenti nella grammatica indicano rispettivamente:

- **{}** denota un elemento opzionale
- **|** denota un'alternativa tra elementi
- **\*** denota un elemento che puo' ripetersi **0** o **N** volte
- **\+** denota un elemento che puo' rieptersi **1** o **N** volte
- **[]** denota un insieme di caratteri che rappresentano un alternativa
- **()** denota un gruppo di elementi

## SINTASSI GFA 2.0
La sintassi di un file GFA 2.0 deve rispettare le seguenti regole per essere valida:

1. Ogni *token lessicale* **DEVE** essere separato dal suo successivo con un solo **TAB** (**\t**) 
2. Ogni *record-line* **DEVE** iniziare con una lettera e **DEVE** stare su una singola riga per essere considerata valida. Righe con un delimitatore *NEWLINE* (**\n**) "fuori posto" **non** saranno considerate **valide**
3. Prima del primo simbolo caratterizzante ogni riga, **non** ci possono essere **spazi vuoti** (**\s**)
4. Il simbolo **#** permette all'utente di specificare delle righe *commento* e quindi **ignorate** in fase di analisi

```
A differenza del progetto originale, in cui ogni riga non iniziante con il simbolo [H, S, F, E, G, O, U] 
viene ignorata in quanto riga utente  utile per permettere a quest'ultimo di creare record-line speciali,
In questo progetto ogni riga NON iniziante con i simboli [H, S, F, E, G, O, U oppure #] viene considerata errata.
```

# DESCRIZIONE PROGETTO
Il progetto e' stato sviluppato in **python 3.7.6** con il supporto dell'environment **Anaconda3** in ambiente **Windows 10**.
L'editor utilizzato sia per lo sviluppo che per il debug dello script python e' **Visual Studio Code**.
Il progetto è stato anche testato in ambiente **Linux** su un computer con **ElementaryOS**, una distribuzione di *Ubuntu*, risultando funzionante.

## FUNZIONE PRINCIPALE PROGETTO
La funzione principale del progetto e' la funzione **readGFAFileLines** che prende come argomenti

1. Il percorso di un file (**GFAFilePath**)
2. Una lista dove dove verranno salvati eventuali righe errate del file (**errorsArray**)

Questa funzione consiste principalmente in: 

1. Controllo per assicurarsi che il percorso passato in input sia associato ad un file non vuoto
2. Apertura del file in modalita' *lettura* (**r**) ed inizializzazione di 3 importanti variabili
    
    1. **lineToCheck**: variabile in cui viene salvata la prima riga del file
    2. **linePointer**: variabil in cui viene salvato il numero della riga che si sta analizzando (banalmente e' un contatore che parte da 1 e si incrementa ogni volta)
    3. **regex**: variabile core della funzione; la regex al suo interno viene compilata in un *oggetto pattern* utile per controllare la conformita' del file al formato GFA 2.0

```python
regex = re.compile(
    '^H(\t\w{2}:[ABHJZif]:[ -~]*)?(\t\w{2}:[ABHJZif]:\-?\d+(\,\-?\d+)*)?(\t\w{2}:[ABHJZif]:[ -~]*)*'                               # regex per il controllo dell' HEADER
    '|^S(\t[!-~]+)(\t\-?\d+)(\t(\*|[!-~]+))(\t\w{2}:[ABHJZif]:[ -~]*)*'                                                            # regex per il controllo dei SEGMENT        
    '|^F(\t[!-~]+){2}[+-](\t\-?\d+\$?){4}\t((\*)|(\d+[MDIP])+|(\-?\d+(\,\-?\d+)*))(\t\w{2}:[ABHJZif]:[ -~]*)*'                     # regex per il controllo dei FRAGMENT
    '|^E(\t([!-~]+|\*))(\t[!-~]+[+-]){2}(\t\-?\d+\$?){4}(\t((\*)|(\d+[MDIP])+|(\-?\d+(\,\-?\d+)*)))(\t\w{2}:[ABHJZif]:[ -~]*)*'    # regex per il controllo degli EDGE
    '|^G(\t([!-~]+|\*))(\t[!-~]+[+-]){2}(\t\-?\d+)(\t(\*|\-?\d+))(\t\w{2}:[ABHJZif]:[ -~]*)*'                                      # regex per il controllo dei GAP
    '|^[OU]\t([!-~]+|\*)(\t([!-~]+[+-]?)([ ][!-~]+[+-]?)*)(\t\w{2}:[ABHJZif]:[ -~]*)*'                                             # regex per il controllo dei GROUP               
    '|^#[\s\w]*')                                                                                                                  # regex per il controllo dei COMMENTI
```

3. Ciclo che controlla finche la variabile *lineToCheck* non e' vuota se vi e' un **match** tra *regex* e *lineToCheck*, altrimenti viene inserita *lineToCheck* nella lista *errorsArray* insieme al suo rispettivo *linePointer* 

## FUNZIONI AL CONTORNO
Le funzioni al contorno di questo progetto, ovvero tutte quelle che permettono il corretto funzionamento di quest'ultimo sono:

1. Funzione **main**
2. Funzione **PrintInfo**
3. Funzione **FileInput**
4. Funzione **CreateFile**

la funzione piu' interessante delle 4 e' sicuramente **FileInput** la quale si preoccupa di:

1. Chiedere in input un **file** (preferibilmente un percorso relativo o assoluto verso tale file)
2. Controllare che tale file esista sul computer grazie alla funzione importata dalla libreria **pathlib2**

```python
exist = Path(File).resolve().is_file()   # True se esiste, False altrimenti
```

3. Chiamo la funzione **readGFAFileLines**
4. Controllo se la lista **errorsArray** e' vuota, altrimenti la stampo a video

    1. Se è vuota non stampo nulla
    2. Se **non** è vuota e la dimensione di **errorsArray** è < 145 allora la stampo a video (questo a causa di una limitazione sul numero di caratteri che possono venir stampati a video dalla *console **Windows*** (**8192**))
    3. Altrimenti chiedo all'utente se vuole salvare in un file la lista **errorsArray** e in caso affermativo, chiamo la funzione **CreateFile** che si occuperà di creare nella stessa *directory* di **GFAFile** un file chiamato **errors_(nomeFile.gfa).txt** dove saranno salvati tutti gli errori presenti in **errorsArray**

5. Chiedo infine, se si vuole analizzare un altro file, altrimenti termino lo script


