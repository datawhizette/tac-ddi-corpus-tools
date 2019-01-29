import os
import xml.etree.ElementTree as ET

import spacy


# testPath = 'test1Files/'
# outputPath = 'testFiles_pretagged/test1_output_CONLL.txt'

def convert_xml_to_conll_format_test ( testPath, outputPath ):
    """
    Convert test files in xml format to CoNLL format and write the result to txt file
    
    input: path to initial files directory and output txt file location
   
    """
    files = [i for i in os.listdir (testPath) if i.endswith ("xml")]
    parser = spacy.load ('en')

    sentences = []

    for file in files:  # parsing each xml file
        tree = ET.parse (testPath + file)
        root = tree.getroot ( )
        filename = file[:-4]
        for v in root.iter ('Sentence'):
            sent = v.find ('SentenceText').text.strip ( )
            sentence = {'tokens': [], 'filename': [], 'POS': [], 'dep': [], 'tags': []}
            tokens = parser (sent)  # split sentence into tokens
            sentence['tokens'] = [token.orth_ for token in tokens if not token.orth_.isspace ( )]
            sentence['POS'] = [token.tag_ for token in tokens if not token.orth_.isspace ( )]
            sentence['dep'] = [token.dep_ for token in tokens if not token.orth_.isspace ( )]
            sentence['filename'] = [filename]
            sentence['tags'] = ['O' for token in tokens]
            sentences.append (sentence)

    with open (outputPath, 'w', encoding='utf-8') as fin:
        for sent in sentences:
            filename = sent['filename']
            for tok, pos, dep, tag in zip (sent['tokens'], sent['POS'], sent['dep'], sent['tags']):
                fin.write ('\t'.join ([tok, pos, dep, filename[0], tag]))
                fin.write ('\n')
            fin.write ('\n')
