# TODO: check that in train and dev datasets there is no more that 50% intersection in text fragments, otherwise
# put overlapping sentence to train only or dev only

import os
import xml.etree.ElementTree as ET

import spacy
from more_itertools import flatten

parser = spacy.load ('en')


class Error (Exception):
    def __init__ ( self, msg ):
        self.msg = msg

    def __str__ ( self ):
        return self.msg


def tagSentence ( currentPosition, word, all_parts, sentence, typeEntity ):
    positionSent = sentence['starts'].index (currentPosition)
    #     print ('Where the matching index is located:', positionSent)
    placeIn = sentence['tags'][positionSent]
    print (word, currentPosition)
    print ('all parts', all_parts)
    if len (all_parts) == 1:
        wantPut = 'S-' + typeEntity
    elif word == all_parts[0]:
        wantPut = 'B-' + typeEntity
    elif word == all_parts[-1]:
        wantPut = 'E-' + typeEntity
    else:
        wantPut = 'I-' + typeEntity

    if placeIn != 'O':
        print ('Mm, tag %s is already here, but you want to put %s' % (placeIn, wantPut))
    sentence['tags'][positionSent] = wantPut


def processSentence ( part, span, all_parts, sent, sentence, typeEntity ):
    words = parser (part)
    words = [tk.orth_ for tk in words if not tk.orth_.isspace ( )]
    start = int (span.split ( )[0])
    end = int (start + int (span.split ( )[1]))
    #                             print ('mathced sent', len(sent[start:end]))
    #                             print ('matched part', len(part))
    if sent[start:end] == part.strip ( ):
        currentPosition = start
        for word in words:
            #                                     end = start+len(word)
            if currentPosition in sentence['starts']:
                print ('we here', word)
                tagSentence (currentPosition, word, all_parts, sentence, typeEntity)
                currentPosition += len (word) + 1

            elif (currentPosition - 2) in sentence['starts']:
                tagSentence (currentPosition - 2, word, all_parts, sentence, typeEntity)
                currentPosition += len (word) - 1
            elif word in sentence['tokens']:
                index = sentence['tokens'].index (word)
                currentPosition = sentence['starts'][index]
                tagSentence (currentPosition, word, all_parts, sentence, typeEntity)
                currentPosition += len (word)
            else:
                raise Error ('Bmm, no position found for word: %s with position: %d' % (word, currentPosition))
    else:
        raise Error ("Wrong tagging")


def mapAll ( st, sentence, sent ):
    typeEntity = st.attrib['type']
    text = st.attrib['str']
    position = st.attrib['span']
    full_parts = parser (text)
    full_parts = [tk.orth_ for tk in full_parts if not tk.orth_.isspace ( )]
    print (full_parts)
    #                     tr = re.sub('\d+', '#', st)
    if " | " in text:
        print (text)
        parts = text.split (' | ')
        spans = position.split (';')
        #                         print (spans)
        all_parts = [el.split ( ) for el in parts]
        all_parts = list (flatten (all_parts))
        for part, span in zip (parts, spans):
            processSentence (part, span, all_parts, sent, sentence, typeEntity)
    else:
        print (text)
        processSentence (text, position, full_parts, sent, sentence, typeEntity)
    return sentence


trainPath = 'trainingFiles/'
outputPath = 'conll_tac_bioes20sp.txt'


def convert_xml_to_conll_format ( trainPath, outputPath ):
    """

    :param trainPath: path to the directory with training examples in xml format
    :param outputPath: txt file in CoNLL format with each column representing (token, POS, filename, tag),
    where 'tag' is in BIOES format
    :return: None
    """

    files = [i for i in os.listdir (trainPath) if i.endswith ("xml")]
    sentences = []
    filt = set ( )

    for file in files:  # parsing each xml file
        tree = ET.parse (trainPath + file)
        root = tree.getroot ( )
        filename = file[:-4]
        for v in root.iter ('Sentence'):
            sent = v.find ('SentenceText').text.strip ( )

            if sent not in filt:
                filt.add (sent)
                sentence = {'tokens': [], 'filename': [], 'POS': [], 'dep': [], 'tags': [], 'starts': []}
                #             sent = re.sub('\d+', '#', sent)
                tokens = parser (sent)
                sentence['tokens'] = [token.orth_ for token in tokens if not token.orth_.isspace ( )]
                sentence['POS'] = [token.tag_ for token in tokens if not token.orth_.isspace ( )]
                sentence['dep'] = [token.dep_ for token in tokens if not token.orth_.isspace ( )]
                sentence['filename'] = [filename]
                sentence['tags'] = ['O' for token in tokens]

                helpLength = -1
                for el in sentence['tokens']:
                    sentence['starts'].append (sent.find (el, helpLength + 1))
                    helpLength += len (el)

                sentenceTagg = {}
                for st in v.iter ('Mention'):
                    typeEntity = st.attrib['type']
                    if typeEntity == 'SpecificInteraction':
                        sentenceTagg = mapAll (st, sentence, sent)
                    elif (typeEntity == 'Precipitant' and ('B-SpecificInteraction' in sentence['tags'] or
                                                           'S-SpecificInteraction' in sentence['tags'])):
                        sentenceTagg = mapAll (st, sentence, sent)

                if sentenceTagg:
                    sentences.append (sentenceTagg)

    # convert list of dict to CONLL and write to file
    sentences = list (filter (None, sentences))  # filter empty instances of a list of sentences

    with open (outputPath, 'w') as fin:
        for sent in sentences:
            filename = sent['filename']
            for tok, pos, dep, tag in zip (sent['tokens'], sent['POS'], sent['dep'], sent['tags']):
                fin.write ('\t'.join ([tok, pos, dep, filename[0], tag]))
                fin.write ('\n')
            fin.write ('\n')
