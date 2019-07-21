# Text Segmentation
Implementare un semplice sistema di segmentazione
di testi ispirato al Text Tiling, e che usi / integri risorse
come WordNet, named entities, etc.

Utilizzo WordNet: https://www.nltk.org/_modules/nltk/tokenize/texttiling.html

## Text Tiling Algorithm
Credits: https://www.aclweb.org/anthology/J97-1003
TextTiling: Segmenting Text into
Multi-paragraph Subtopic Passages
Marti A. Hearst*, Xerox PARC  
Da pagina 16  
The Text Tiling algorithm for discovering subtopic structure
using term repetition has three main parts:
1. Tokenization
2. Lexical Score Determination
3. Boundary Identification

### Tokenization
- Divide input text into individual lexical units (list of words)
- Skip title
- Convert to lower-case
- Skip stop words and punctuation
- Reduce tokens to their morphemes
- Subdivide text into pseudosentences of a predefined
 size w (equal-sized units: number of shared terms
between two long sentences and between a long and a short
sentence would probably yield incomparable scores; sentences
are too short to expect normalization to really accommodate
for the differences) [token-sequences]
- Morphologically analyzed token is stored in a table along
with a record of the token-sequence number
it occurred in, and the number of times it appeared in the 
token-sequence
- A record is also kept of the locations of the paragraph
breaks within the text  
NOTA: questo ed il record precedente non sono stati fatti
- Stop words contribute to the computation of the size of
the token-sequence, but not to the computation of
the similarity between blocks of text.

### Lexical Score Determination
Vediamo due tipi di score:
- Block comparison: confronta blocchi adiacenti di testi per
vedere quanto sono simili in base a quante parole hanno in
comune (similarità lessicale). k: dimensione dei blocchi.  
La similarità si calcola per ogni sequenza di token: viene assegnato
uno score ad ogni gap di sequenze di token i in base a quanto
i blocchi che vanno da i-k a i sono simili ai blocchi che vanno
da i+1 a i+k+1.  
Similarità tra blocchi: siano b1={token-sequence_{i-k},...,
token-sequence_{i}} e b2={token-sequence_{i+l},...,
token-sequence_{i+k+l}}, allora score = formula pag 17
- Vocabulary Introduxtion Method: assegna uno score ad una
sequeza di token in base a quante nuove parole ci sono 
nell'intervallo in cui si trova il punto di mezzo (midpoint)  
Numero di parole nuove / numero di parole totali

NOTA: si utilizzano le pseudo sentences perché i paragrafi
hanno una lunghezza irregolare che porterebbe ad un confronto
sbilanciato. Per usarli ci andrebbe una normalizzazione  

Non utilizzo nessuno dei due: utilizzo WordNet e quindi come
valutazione di similarità utilizzo Wu & Palmer o Leacock Chodorow

### Boundary Identification



# TO DO
Lexical Score Determination  
Leggere pdf pag 16 e fare cosa dice
