# TLN
In questa repo potrete trovare i vari progetti realizzati per il corso di Tecnologie del Linguaggio Naturale.

# Testo Esercizio 3 (Mazzei)
## Traduzione intelingua En -> It
1. Scrivere una CFG per l'Inglese (G1), dotata di semantica, che parsifichi (almeno) le frasi:
- (1) *You are imagining things*
- (2) *There is a price on my head*
- (3) *Your big opportunity is flying out of here*
- **HINT**: ispirarsi alla grammatica [“simple-sem.fcfg”](https://github.com/nltk/nltk_teach/blob/master/examples/grammars/book_grammars/simple-sem.fcfg)
2. Provare G1 in NLTK (http://www.nltk.org/book/ch10.html)
3. Costruire un sentence planner che per ogni formula prodotta dalla grammatica G1 produca un sentence-plan (proto-albero a dipendenze) valido. (**HINT**: È possibile usare un semplice approccio basato su espressioni regolari e sentence-plan precompilati)
4. Usando la librerie SimpleNLG-IT (eventualmente come server attraverso socket o via pipe) implementare un semplice realizer che trasformi i sentence plans in frasi italiane (**HINT**: usare una lessicalizzazione EN->IT 1-1)

## Consegna
Bisogna consegnare il codice e una breve relazione (max 10 pagine) almeno **due giorni prima** della data dell'esame dell'orale concordata.
Attenzione: gli esercizi si possono fare in gruppi da 2.

## How to
per eseguire `python3 test.py <grammatica> "<frase da parsificare>"`.


Es: `python3 test.py simple-sem.fcfg "every dog bites a bone"`.

## Elenco dei POS tags usati
[qui](https://universaldependencies.org/u/pos/)

## Appunti
`SEM` all'interno delle regole lessicali regola la semantica dei simpboli terminali definite secondo le regole del lambda calcolo. (Vedi pacco 7 slide 41 Ro)

Non stampa un cazzo in output, c'è qualcosa che non va
