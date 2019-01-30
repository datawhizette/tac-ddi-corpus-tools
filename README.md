# Tools for processing TAC DDI 2018 corpus

## 1. Description

This package provides several tools related to the [TAC DDI Corpus](https://bionlp.nlm.nih.gov/tac2018druginteractions/):
1. Conversion of the XML files into tabulated format (CoNLL). Tokenization is performed using [SpaCy](https://spacy.io/api/tokenizer).
2. Conversion of the processed corpus back to XML format required for submission. 
3. In a process, construction of entities and their positions was performed taking into account their discontinuous and overlapping nature.

Characteristics of CoNLL data:
- each line - one word with its characteristics, separated by tabs. Characteristics include: part-of-speech tag and label
- every sentence is separated from each other by empty line
- in this case, labels follow BIOES (beginning-inside-outside-end-single (of) entity) format. 

Characteristics of XML data
- files are split into folders by drug names
- discontinuous entites are split by '|', and spans by ';' characters. For example, in a sentence "Both alcohol and tadalafil , a PDE5 inhibitor , act as mild vasodilators" an entity would be "Both | act as | vasodilators" and the span for this entity "0 4;48 6;60 12".

## 2. Usage

All the code is implemented using Python 3.6. 

To run the script to convert XML data to ConLL format or back, please follow the examples below.
```bash
python main.py convert-train --input_path ./trainingFiles/ \
    --output_file ./conll_tac_bioes.txt 
    
python main.py convert-test --input_path ./testFiles/ \
    --output_file ./conll_tac_bioes_test.txt
    
python main.py convert-results --input_path ./TAC2018/test2Files/ \
    --input_file ./test_output_CONLL.txt \
    --trigger_file ./tagged_test_conll_tr.txt \
    --specificints_file ./tagged_test_conll_sp.txt \
    --output_path ./processedTestXml/
```

Here, in a last example there are 2 outputs of predictions, which are further merged into one file, but feel free to modify code 
to your data.
