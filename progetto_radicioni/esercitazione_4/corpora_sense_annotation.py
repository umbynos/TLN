# Corpora and Sense Identification
# Task: Semantic Word Similarity


#########################
# SVOLGIMENTO
#########################

# ANNOTAZIONE
# Annotare a mano con un punteggio da o a 4 (decimali compresi) la samilarità tra 100 coppie di termini (words.txt):
# - 4: molto simimli -> sinonimi
# - 3: simili -> le parole condiviono molto, ma non si riferiscono allo stesso concetto (es leone e zebra)
# - 2: leggermente simili -> le parole non hanno un significato molto simile, ma condividono lo stesso argomento, dominio, funzione oppure sono correlati (es casa e finestra)
# - 1: diversi -> le due parole sono diverse, ma potrebbero avere piccoli dettagli che le accomunino; potrebbero essere trovato in un articolo che tochi il loro argomento (es: software e tastiera)
# - 0: completamente diversi -> le due parole non hanno lo stesso significato e appartengono a topic diversi (es: biro e rana)
# Avremo quindi un file di 100 linee ciascuna contenente due parole seguite da un numero in [0,4]. NOTA: magari inserisci anche un commento sulla motivazione che ti ha spinto a mettere quel valore
# Dobbiamo calcolare il valore medio dato dagli annotatori e l'iner-rater agreement (sempre basandosi sui numeri dati da noi. Qui usiamo Pearson e Spearman)
# NOTA: NEL CORPUS CI SONO DEGLI ACCENTI. SE HAI PROBLEMI SAPPILO

# Sense Identification
# Nell’attribuire un valore di similarità a una coppia di termini (per esempio, società e cultura) quali sensi vengono selezionati?
# Partiamo dall’assunzione che i due termini funzionino come contesto di disambiguazione l’uno per l’altro.
# Calcolare la similarità come il massimo ottenuto (come per es 1) utilizzando come metrica la cosine-similarity fra i vettori NASARI dei sensi associati ai vari termini
# A differenza di quanto fatto nella prima esercitazione, ora non siamo interessati a calcolare il punteggio di similarità fra 2 termini, ma a individuare i sensi che massimizzano tale punteggio
# Si tratta quindi di eseguire questa operazione: c1, c2 = argmax [sim(c1,c2)] con c1€s(w1) e c2€s(w2) [prima era sim(w1,w2)=...]

# OUTPUT 
# 2 BabelNet synset ID e dalla relativa glossa (la glossa serve perche il synset id ci dice molto poco)
# Valutiamo il risultato ottenuto (cioè la coppia dei sensi identificati, e la relativa appropriatezza) direttamente,
# stabilendo se i sensi in questione sono quelli idealmente selezionati da noi stessi nel momento dell’annotazione [a mano]
# Misuriamo in questo caso l’accuratezza sia sui singoli elementi, sia sulle coppie
# NB: per questa valutazione non è necessario conoscere il BabelNet synset ID corretto, ma è sufficiente valutare sulla base della glossa, se il senso individuato è appropriato.


def main():
	print("Hello world!")

if __name__== "__main__":
	main()