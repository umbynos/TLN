# Testo Esercizio 2 (Mazzei)
SVX -> XSV
- Scrivere a una CFG per l'italiano (G1) che parsifichi (almeno) le frasi di esempio.
- HINT: ispirarsi alla [grammatica “simple-sem.fcfg”](https://github.com/nltk/nltk_teach/blob/master/examples/grammars/book_grammars/simple-sem.fcfg) e costruirla direttamente in CNF
- Implementare l'algoritmo CKY e provare la grammatica G1 su questo programma per le frasi di esempio.
- Costruire un algoritmo di traduzione che riscriva l'abero di derivazione per Italiano in un albero Italiano-Yodish e stamparne
le foglie.
- Attenzione: ignorare l'ambiguità e prendere il primo albero ottenuto
Frasi di esempio esercizio 2
- Tu avrai novecento anni di età -> Novecento anni di età tu avrai
- Tu hai amici lì-> Amici hai tu lì
- Noi siamo illuminati-> Illuminati noi siamo

## Consegna
Bisogna consegnare il codice e una breve relazione (max 10 pagine) almeno **due giorni prima** della data dell'esame dell'orale concordata.
Attenzione: gli esercizi si possono fare in gruppi da 2.

## How to
Per eseguire `python3 cky_algorithm.py g1.fcfg "<frase da parsificare>"`.