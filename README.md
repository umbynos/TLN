# TLN
In questa repo potrete trovare i vari progetti realizzati per il corso di Tecnologie del Linguaggio Naturale.

# Testo Esercizio 3 (Mazzei)
## Traduzione intelingua En -> It
1. Scrivere una CFG per l'Inglese (G1), dotata di semantica, che parsifichi (almeno) le frasi:
- (1) *You are imagining things*
- (2) *There is a price on my head*
- (3) *Your big opportunity is flying out of here*
- **HINT**: ispirarsi alla grammatica [â€œsimple-sem.fcfgâ€](https://github.com/nltk/nltk_teach/blob/master/examples/grammars/book_grammars/simple-sem.fcfg)
2. Provare G1 in NLTK (http://www.nltk.org/book/ch10.html)
3. Costruire un sentence planner che per ogni formula prodotta dalla grammatica G1 produca un sentence-plan (proto-albero a dipendenze) valido. (**HINT**: Ãˆ possibile usare un semplice approccio basato su espressioni regolari e sentence-plan precompilati)
4. Usando la librerie SimpleNLG-IT (eventualmente come server attraverso socket o via pipe) implementare un semplice realizer che trasformi i sentence plans in frasi italiane (**HINT**: usare una lessicalizzazione EN->IT 1-1)

# Testo Esercizio 2 (Mazzei)
SVX -> XSV
- Scrivere a una CFG per l'italiano (G1) che parsifchi (almeno) le frasi di esempio.
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
per eseguire `python3 test.py <grammatica> "<frase da parsificare>"`.


Es: `python3 test.py simple-sem.fcfg "every dog bites a bone"`.

## Elenco dei POS tags usati
[qui](https://universaldependencies.org/u/pos/)

## Debug python da linea di comando
Inserire `import pdb; pdb.set_trace()` nel codice. Scrivere `step(s)` per andare avanti ed entrare nelle funzioni, `next(n)` per andare avanti senza entrare nelle funzioni. Più dettagli [qui](https://codeburst.io/how-i-use-python-debugger-to-fix-code-279f11f75866)

## Appunti
- Su master funziona "tu hai amici"
- Su reification sperimentiamo la reificazione
