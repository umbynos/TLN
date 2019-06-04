# Appunti
Es 2 su *WSD* (Word Sense Disambiguation)
Algo di Lesk usato per questo

## Testo es2
- Implementare l’algoritmo di Lesk (!= usare implementazione esistente, e.g., in nltk...).
- Disambiguare i termini polisemici all’interno delle frasi del file `sentences.txt`; oltre a restituire i synset ID del senso (appropriato per il contesto), il programma deve riscrivere ciascuna frase in input sostituendo il termine polisemico con l’elenco dei sinonimi eventualmente presenti nel synset.
- Estrarre 50 frasi dal corpus SemCor (corpus annotato con i synset di WN) e disambiguare almeno un sostantivo per frase. Calcolare l’accuratezza del sistema implementato sulla base dei sensi annotati in SemCor.
- SemCor è disponibile all’URL (http://web.eecs.umich.edu/~mihalcea/downloads.html)

## Requisiti
Installare pip3 `sudo apt install python3-pip`
Installare nltk `pip3 install nltk`

## Come eseguire
Lanciare *wsd.py* `python3 wsd.py`

## Utils
https://www.nltk.org/_modules/nltk/wsd.html

## Test
Il file `lesk_nltk.py` è l'implementazione di lesk standard dentro a nltk -> utile per prendere spunto.
Per far funzionare è necessario fare: `import nltk` e poi `nltk.download('wordnet')`

Per provare: `lesk_nltk.lesk(['I', 'went', 'to', 'the', 'bank', 'to', 'deposit', 'money', '.'], 'bank', 'n')` (importare prima lesk_nltk)