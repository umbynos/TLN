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
- Stop words contribute to the computation of the size of
the token-sequence, but not to the computation of
the similarity between blocks of text.