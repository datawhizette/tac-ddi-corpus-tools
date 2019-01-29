# Tools for processing TAC DDI 2018 corpus

## 1. Description

This package provides several tools related to the [TAC DDI Corpus](https://bionlp.nlm.nih.gov/tac2018druginteractions/):
1. Conversion of the XML files into tabulated format (CoNLL). Tokenization is performed using [SpaCy](https://spacy.io/api/tokenizer).
2. Conversion of the processed corpus back to XML format required for submission. 
3. In a process, construction of entities and their positions was performed taking into account their discontinuous and overlapping nature.
