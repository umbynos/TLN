# Automatic Summarization with NASARI
Novel Approach to a Semantically-Aware Representation of Items
Vectore Space representation

## NOTA
La parola poterbbe non essere presente all'interno di BabelNet

## WHAT TO DO
Riassumere questi 3 documenti utilizzando NASARI
- Donald-Trump-vs-Barack-Obama-on-Nuclear-Weapons-in-East-Asia.txt (464 parole)
- People-Arent-Upgrading-Smartphones-as-Quickly-and-That-Is-Bad-for-Apple.txt (416 parole)
- The-Last-Man-on-the-Moon—Eugene-Cernan-gives-a-compelling-account.txt (901 parole)
Fare gli esperimenti con tassi di compressione (compression rates) diversi: 10%, 20% e 30%

Seleziona le frasi con parole più salienti o che contengono più informazioni
La salienza di solito si trova calcolando la topic signature (un insieme di salienti o di signature terms).
Ogni valore della salienza della topic signature deve essere maggiore di una certa soglia. Dovrebbero esistere delle funzioni che la calcolano (la frequenza non è detto che vada bene).
La SPECIFICITA LESSICALE può essere utilizzata per individuare i termini più salienti e dare così un valore alle frasi dove sono

## Audio Elisa
Contenuto dei testi: titolo e paragrafi divisi da righe vuote  
Ovviamente si cerca di ottenere dei riassunti estrattivi (non astrattivi)  
Esistono varie misure per fare i riassunti -> relevance criteria
- Metodo del titolo: eliminare le stop words e utilizzare le parole rimaste per trovare le frasi importanti del testo
- Posizione nel testo: nell'85% dei casi il topic viene presentato all'inizio del testo
- Optimum Position Policy (OPP): le frasi più rilevanti sono in posizioni che dipendono dal genere. Queste posizioni possono essere note oppure si posssono determinare automaticamente attraverso il training  
Step 1: For each article, determine the overlap
between sentences and the index terms (e.g., title
terms)  
Step 2: Determine a partial ordering over the
locations where sentences containing important
words occur: Optimal Position Policy (OPP)
- Il metodo delle battute d'entrata. Es:“The main aim of the present paper is to describe…”,
“The purpose of this article is to review…”,
“In this report, we outline…”,
“Our investigation has shown that…”,  
Le parole si suddividono in bonus e stigma. Bonus: comparatives, superlatives, conclusive expressions, etc.
Stigma: negatives, pronouns, etc. non-important sentences contain
‘stigma phrases’ such as hardly and impossible.  
These phrases can be detected automatically.  
Method: Add to sentence score if it contains a bonus phrase,
penalize if it contains a stigma phrase.
- Il metodo basato sulla coesione: le frafi più importanti hanno più collegamenti con altre  
La coesione si può calcolare su  
  - word co-occurrences (Apply IR methods at the document level: texts
are collections of paragraphs. Use a traditional, IR-based, word similarity measure to
determine for each paragraph Pi the set Si of
paragraphs that Pi is related to. Method: determine relatedness score Si for each paragraph; extract paragraphs with largest Si scores);
  - local salience and grammatical relations;
  - co-reference;
  - lexical similarity (WordNet, lexical chains);
  - combinations of the above.

Ne basta una, vedere se farne di più  
Loro l'hanno fatto con il titolo e con la coesione dei paragrafi  
Con il titolo per ogni parola del titolo trovi il vettore di Nasasri  
Con la coesione tra i paragrafi anche (per ogni parola del paragrafo trovi il vettore)  
Per valutare l'operato si usa la weighted overlap tra il vettore del titolo ed i vettori del paragrafo
e poi tra i vari paragrafi  
I risultati vanno ottenuti con prove diverse: es 15% di importanza al titolo, 50, 75...  
Per valutare non c'è altro modo se non leggerli noi.
Magari scrivire qualcosa nella relazione (es: con questa importanza al titolo, i riassunti vengono male perché il titolo è fuorviante)   

NOTA  
I vettori unified di NASARI non sono molto aggiornati e in più noi ne utilizziamo una versione ristretta  
Per diminuire il problema, loro hanno fatto un altro giro: per ogni vettore trovato si cercano i vettori delle parole presenti nel vettore nasari della prima passata  
Così facendo si ottiene una matrice (puoi fare quanti giri vuoi, ma diventa enorme)  
