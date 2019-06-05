
# Da Moodle
Il materiale in questa directory è disponibile all'URL http://www.cs.technion.ac.il/~gabr/resources/data/wordsim353/

# Conceptual similarity with WordNet

### INPUT
Usare WordSim353 (tsv o csv): 2 termini con valore numerico per similarita [0,10]

### OUTPUT
Punteggio numerico di similarita che indica la vicinanza semantica dei termini in input

### SCALA PUNTEGGI
Compreso nell'intervallo [0,1]: 0 completamente dissimile; 1 identita

### SVOLGIMENTO
#### Trovare la vicinanza semantica con 3 diverse misure:
- Wu & Palmer
- Shortest Path
- Leakcock & Chodorow
#### Per ciascuna misura di similarita calcolare:
- gli indici di correlazioine di Spearman
- gli indici di correlazioine di Pearson confrontando il risultato ottenuto con quello presente all'interno del file

### NOTE
- L' input è dato come coppia di termini, mentre nelle formule vengono richiesti i sensi. Per disambiguare si prendano i sensi con la massima similarita
- Sfruttare la struttura ad albero di WordNet per calcolare la vicinanza semantica
- Documentazione WordNet: https://wordnet.princeton.edu/documentation
