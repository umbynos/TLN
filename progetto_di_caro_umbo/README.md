# Text Segmentation
La Text segmentation viene fatta attraverso il Text Tiling

# Testo Esercizio
Implementare un semplice sistema di segmentazione di testi ispirato al Text Tiling, e che usi / integri risorse come WordNet, named entities, etc.

## Appunti
Usare articoli e vettore nasari di es3 di Radicioni.
Suddividere l'articolo in frasi/paragrafi e sistemare in gruppi (per numero di frasi nel gruppo o per num totale di blocchi)
poi calcolare la wo (come in es3) tra due frasi consecutive nel blocco. Prendere la minima e piazzare una divisione con il blocco sopra.
Fare questa operazione per tutte le frasi all'interno di un blocco.

È un metodo un po' stupido poichè il numero di divisioni rimane uguale all'inizio.

## Appunti2
Sarebbe magari meglio mettere una frase all'interno di un nuovo blocco se è molto diversa dal blocco precedente.
Oppure scorro tutto il file e quando la frase successiva è molto diversa dalla precedente divido.

# ToDo
1) Lettura e inizializazione files [FATTO]
2) Creazione strutture dati [FATTO]
3) Weighted Overlap [FATTO da provare]
4) Suddivisione in blocchi [FATTO]
5) Fare WO sulle varie frasi nei cari blocchi [FATTO]
6) Applicare spostamento della suddivisione [DUNNO]
7) Magari applicare algo di elaborazione più intelligente