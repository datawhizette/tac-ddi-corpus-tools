# TODO: catch cases when there is one starting word for several entities

import os
import xml.etree.ElementTree as ET

import spacy
from more_itertools import flatten


class Error (Exception):
    def __init__ ( self, msg ):
        self.msg = msg

    def __str__ ( self ):
        return self.msg


def search_entities ( words, tags, starts, wantTag ):
    """
    Recursive function to search for the consequences comprising entities of DDI type in a list of
    words of one sentence

    :param words: a list of words in a sentence
    :param tags: a list of tags for each word
    :param starts: a list of tag's beginning position in a sentence
    :param wantTag: true tag we want to find
    :return: compound entities for each sentence which further would be mapped to exact location and located in xml
    file for submission
    """

    global entities
    entities = []
    global tag
    tag = []
    global newEntity
    global newTag
    global previous
    global beginning
    global lengths
    lengths = []
    global prevlen

    if (len (words) < 2):
        return []
    if (words[0] not in '().,;:!?""'):
        if (tags[0][:2] == 'B-' and tags[0][2:] == wantTag):
            newEntity = []
            newTag = []
            newEntity.append (words[0])
            newTag.append (tags[0])
            print (starts)
            beginning = starts[0]
            previous = 'B'
            prevlen = str (starts[0] + len (words[0]) - beginning)
            if ('I-' + wantTag not in tags and 'E-' + wantTag not in tags and 'S-' + wantTag not in tags):
                entities.append (words[0])
                lengths.append (str (beginning) + ' ' + prevlen)
                newEntity = []
                newTag = []

        if (tags[0][:2] == 'I-' and tags[0][2:] == wantTag and 'B-' + wantTag in newTag):
            if previous == 'B' or previous == 'E' or previous == 'I':
                prevlen = str (starts[0] + len (words[0]) - beginning)
                newEntity.append (words[0])
            else:
                newEntity.append ('| ' + words[0])
                lengths.append (str (beginning) + ' ' + prevlen + ';')
                beginning = starts[0]
                prevlen = str (starts[0] + len (words[0]) - beginning)
            #
            newTag.append (tags[0])
            previous = 'I'
            if ('E-' + wantTag not in tags or 'E-' in newTag):
                entities.append (' '.join (newEntity))
                lengths.append (str (beginning) + ' ' + prevlen)
                newEntity = []
                newTag = []

        if (tags[0][:2] == 'E-' and tags[0][
                                    2:] == wantTag and 'B-' + wantTag in newTag and 'E-' + wantTag not in newTag):
            if (tags[1][:2] == 'I-' and tags[1][2:] == wantTag):
                if (previous == 'B' or previous == 'I'):
                    newEntity.append (words[0])
                    prevlen = str (starts[0] + len (words[0]) - beginning)
                else:
                    newEntity.append ('| ' + words[0])
                    lengths.append (str (beginning) + ' ' + prevlen + ';')
                    beginning = starts[0]
                    prevlen = str (starts[0] + len (words[0]) - beginning)
                #
                newTag.append (tags[0])
                previous = 'E'
            else:
                if (previous == 'B' or previous == 'I'):
                    newEntity.append (words[0])
                    prevlen = str (starts[0] + len (words[0]) - beginning)
                else:
                    newEntity.append ('| ' + words[0])
                    lengths.append (str (beginning) + ' ' + prevlen + ';')
                    beginning = starts[0]
                    prevlen = str (starts[0] + len (words[0]) - beginning)
                entities.append (' '.join (newEntity))
                lengths.append (str (beginning) + ' ' + prevlen)
                tag.append (wantTag)
                newEntity = []
                newTag = []

        if (tags[0][:2] == 'S-' and tags[0][2:] == wantTag and words[0] not in entities):
            if ('B-' in newTag):
                if (previous == 'B' or previous == 'I' or previous == 'E'):
                    newEntity.append (words[0])
                    prevlen = str (starts[0] + len (words[0]) - beginning)
                else:
                    newEntity.append ('| ' + words[0])
                    lengths.append (str (beginning) + ' ' + prevlen + ';')
                    beginning = starts[0]
                    prevlen = str (starts[0] + len (words[0]) - beginning)
                entities.append (' '.join (newEntity))
                lengths.append (str (beginning) + ' ' + prevlen)
                newEntity = []
                newTag = []
            else:
                print ('and here', wantTag)
                entities.append (words[0])
                lengths.append (str (starts[0]) + ' ' + str (len (words[0])))
                tag.append (wantTag)
    else:
        previous = 'O'
    return entities + search_entities (words[1:], tags[1:], starts[1:], wantTag)


def search_lengths ( words, tags, starts, wantTag ):
    """
    Recursive function to search for positions of entities in a sentence

    :param words: a list of words in a sentence
    :param tags: a list of tags for each word
    :param starts: a list of tag's beginning position in a sentence
    :param wantTag: true tag we want to find
    :return: positions of entities in a sentence
    """

    global entities
    entities = []
    global tag
    tag = []
    global newEntity
    global newTag
    global previous
    global beginning
    global lengths
    lengths = []
    global prevlen

    if (len (words) < 2):
        return []
    if (words[0] not in '().,;:!?""'):
        if (tags[0][:2] == 'B-' and tags[0][2:] == wantTag):
            newEntity = []
            newTag = []
            newEntity.append (words[0])
            newTag.append (tags[0])
            beginning = starts[0]
            previous = 'B'
            prevlen = str (starts[0] + len (words[0]) - beginning)

            if ('I-' + wantTag not in tags and 'E-' + wantTag not in tags and 'S-' + wantTag not in tags):
                entities.append (words[0])
                lengths.append (str (beginning) + ' ' + prevlen)
                newEntity = []
                newTag = []

        if (tags[0][:2] == 'I-' and tags[0][2:] == wantTag and 'B-' + wantTag in newTag):
            if previous == 'B' or previous == 'E' or previous == 'I':
                prevlen = str (starts[0] + len (words[0]) - beginning)
                newEntity.append (words[0])
            else:
                newEntity.append ('| ' + words[0])
                lengths.append (str (beginning) + ' ' + prevlen + ';')
                beginning = starts[0]
                prevlen = str (starts[0] + len (words[0]) - beginning)
            newTag.append (tags[0])
            previous = 'I'
            if ('E-' + wantTag not in tags or 'E-' in newTag):
                entities.append (' '.join (newEntity))
                lengths.append (str (beginning) + ' ' + prevlen)
                newEntity = []
                newTag = []

        if (tags[0][:2] == 'E-' and tags[0][
                                    2:] == wantTag and 'B-' + wantTag in newTag and 'E-' + wantTag not in newTag):
            print ('here')
            if (tags[1][:2] == 'I-' and tags[1][2:] == wantTag):
                if (previous == 'B' or previous == 'I'):
                    newEntity.append (words[0])
                    prevlen = str (starts[0] + len (words[0]) - beginning)
                else:
                    newEntity.append ('| ' + words[0])
                    lengths.append (str (beginning) + ' ' + prevlen + ';')
                    beginning = starts[0]
                    prevlen = str (starts[0] + len (words[0]) - beginning)
                newTag.append (tags[0])
                previous = 'E'
            else:
                if (previous == 'B' or previous == 'I'):
                    newEntity.append (words[0])
                    prevlen = str (starts[0] + len (words[0]) - beginning)
                else:
                    newEntity.append ('| ' + words[0])
                    lengths.append (str (beginning) + ' ' + prevlen + ';')
                    beginning = starts[0]
                    prevlen = str (starts[0] + len (words[0]) - beginning)
                entities.append (' '.join (newEntity))
                lengths.append (str (beginning) + ' ' + prevlen)
                tag.append (wantTag)
                newEntity = []
                newTag = []

        if (tags[0][:2] == 'S-' and tags[0][2:] == wantTag and words[0] not in entities):
            if ('B-' in newTag):
                if (previous == 'B' or previous == 'I' or previous == 'E'):
                    print ('check here')
                    newEntity.append (words[0])
                    prevlen = str (starts[0] + len (words[0]) - beginning)
                else:
                    newEntity.append ('| ' + words[0])
                    lengths.append (str (beginning) + ' ' + prevlen + ';')
                    beginning = starts[0]
                    prevlen = str (starts[0] + len (words[0]) - beginning)
                entities.append (' '.join (newEntity))
                lengths.append (str (beginning) + ' ' + prevlen)
                #                 lengths.append(truespin(newLen))
                newEntity = []
                newTag = []
            else:
                print ('and here', wantTag)
                entities.append (words[0])
                lengths.append (str (starts[0]) + ' ' + str (len (words[0])))
                tag.append (wantTag)
    else:
        previous = 'O'

    return lengths + search_lengths (words[1:], tags[1:], starts[1:], wantTag)


def merge ( lst ):
    """
    Utility needed to save entities and locations in correct for submission format

    :param lst: list of elements of entities/location numbers
    :return: list in a correct format
    """
    new = []
    st = ''
    for el in lst:
        if el[-1] == ';':
            st += el
        else:
            if st != '':
                st += el
                new.append (st)
                st = ''
            else:
                new.append (el)
    return new


def read_conll_output_into_list ( mainFile, testTr, testSp ):
    with open (mainFile, 'r', encoding='utf-8') as fin, open (testTr, 'r', encoding='utf-8') as fin1, open (testSp, 'r',
                                                                                                            encoding='utf-8') as fin2:
        sentences = []
        sentence = {'words': [], 'tagsTr': [], 'tagsSp': [], 'filename': []}
        counter = 1
        for line, line1, line2 in zip (fin, fin1, fin2):
            if len (line.split ( )) == 0:
                sentence['filename'].append (fn)
                sentence['count'] = counter
                sentences.append (sentence)
                sentence = {'words': [], 'tagsTr': [], 'tagsSp': [], 'filename': []}
                counter += 1
            else:
                word = line.split ( )[0]
                tagTr = line1.split ( )[-1]
                tagSp = line2.split ( )[-1]
                fn = line.split ( )[3]
                #             print (word)
                sentence['words'].append (word)
                sentence['tagsTr'].append (tagTr)
                sentence['tagsSp'].append (tagSp)
    return sentences


def len_util ( testPath, new_sent ):
    idx = 0
    parser = spacy.load ('en')

    files = [i for i in os.listdir (testPath) if i.endswith ("xml")]

    for file in files:  # parsing each xml file
        tree = ET.parse (testPath + file)
        root = tree.getroot ( )
        for v in root.iter ('Sentence'):
            sent = v.find ('SentenceText').text.strip ( )
            tokens = sent.split ( )
            starts = []
            new_starts = []
            helpLength = -1
            for el in tokens:
                starts.append (sent.find (el, helpLength + 1))
                helpLength += len (el)
            for tok, start in zip (tokens, starts):
                #             print (start)
                moresplit = parser (tok)
                new = [token.orth_ for token in moresplit if not token.orth_.isspace ( )]
                newstart = [start] * len (new)
                new_starts.append ([el for el in newstart])
            new_sent[idx]['starts'] = list (flatten (new_starts))
            idx += 1
    return new_sent


def find_entities ( sent_ent ):
    i = 0
    for sent in sent_ent:
        i += 1
        print ('count', i)
        print (sent)
        sent['triggers'] = ((search_entities (sent['words'], sent['tagsTr'], sent['starts'], 'Trigger')))
        sent['specints'] = ((search_entities (sent['words'], sent['tagsSp'], sent['starts'], 'SpecificInteraction')))
        sent['precipitants'] = ((search_entities (sent['words'], sent['tagsSp'], sent['starts'], 'Precipitant')))

        sent['triggers_loc'] = ((merge (search_lengths (sent['words'], sent['tagsTr'], sent['starts'], 'Trigger'))))
        sent['specints_loc'] = (
            (merge (search_lengths (sent['words'], sent['tagsSp'], sent['starts'], 'SpecificInteraction'))))
        sent['precipitants_loc'] = (
            merge (search_lengths (sent['words'], sent['tagsSp'], sent['starts'], 'Precipitant')))

    for sent in sent_ent:
        dubl = []
        places = []
        for s, loc in zip (sent['triggers'], sent['triggers_loc']):
            print (s, loc)
            if s not in dubl:
                dubl.append (s)
                places.append (loc)
        sent['triggers'] = dubl
        sent['triggers_loc'] = places

    for sent in sent_ent:
        dubl = []
        places = []
        for s, loc in zip (sent['specints'], sent['specints_loc']):
            if s not in dubl:
                dubl.append (s)
                places.append (loc)

        sent['specints'] = dubl
        sent['specints_loc'] = places

    for sent in sent_ent:
        dubl = []
        places = []
        for s, loc in zip (sent['precipitants'], sent['precipitants_loc']):
            print (s, loc)
            if s not in dubl:
                dubl.append (s)
                places.append (loc)
        sent['precipitants'] = dubl
        sent['precipitants_loc'] = places

    for sent in sent_ent:
        if not ((sent['triggers'] or sent['specints']) and sent['precipitants']):
            sent['triggers'] = []
            sent['specints'] = []
            sent['precipitants'] = []

    return sent_ent


# testPath = '../TAC2018/test2Files/'
# outputFile = '../test2_output_CONLL.txt'
# testTr = '../tagged_test2_nochar_conll.txt'
# testSp= '../tagged_test2_nochar_conll_sp.txt'
# outputPath = '../processedTestXml_nochar_2/'

def conll_to_xml(testPath, outputFile, testTr, testSp, outputPath):
    """
    Convert conll output of the model back to xml files in required for submission format by
    merging results of predictions for 2 kind of entities -- Triggers, SpecificInteractions and
    constructing entities taking into account their overlapping and discontinuous structure

    :param testPath: path where test files in XML format are located
    :param outputFile: test data without tags in CoNLL format
    :param testTr, testSp: results of processing of {Trigger, Precipitant} entities and
    (SpecificInteraction, Precipitant} entities
    :param outputPath: path where results would be written to
    :return: directory with resulting xml files suitable for submission
    """

    files = [i for i in os.listdir (testPath) if i.endswith ("xml")]
    parser = spacy.load ('en')
    idx = 0
    new_sent = read_conll_output_into_list (outputFile, testTr, testSp)
    sent_ent = len_util (testPath, new_sent)
    sent_ent = find_entities (sent_ent)

    for file in files:  # parsing each xml file
        tree = ET.parse (testPath + file)
        root = tree.getroot ( )
        for v in root.iter ('Sentence'):
            sent = v.find ('SentenceText').text.strip ( )
            tokens = [token.orth_ for token in parser (sent) if not token.orth_.isspace ( )]
            #         print(tokens)
            if sent_ent[idx]['words'] == tokens:
                if sent_ent[idx]['precipitants']:
                    #                 create node 'Mention'
                    for tr, loc in zip (sent_ent[idx]['triggers'], sent_ent[idx]['triggers_loc']):
                        m = ET.SubElement (v, 'Mention')
                        m.set ('id', str (idx))
                        m.set ('str', tr)
                        m.set ('span', loc)
                        m.set ('type', 'Trigger')
                    for pr, loc in zip (sent_ent[idx]['precipitants'], sent_ent[idx]['precipitants_loc']):
                        m = ET.SubElement (v, 'Mention')
                        m.set ('id', str (idx))
                        m.set ('str', pr)
                        m.set ('span', loc)
                        m.set ('type', 'Precipitant')
                        m.set ('code', '')
                    for sp, loc in zip (sent_ent[idx]['specints'], sent_ent[idx]['specints_loc']):
                        m = ET.SubElement (v, 'Mention')
                        m.set ('id', str (idx))
                        m.set ('str', sp)
                        m.set ('span', loc)
                        m.set ('type', 'SpecificInteraction')
                        m.set ('code', '')
                    m = ET.SubElement (v, 'Interaction')
                    m.set ('type', '')
                    m.set ('effect', '')
                    m.set ('precipitant', '')
                    m.set ('trigger', '')
            else:
                raise Error (
                    "sentences don'\t match each other\nsentence in xml {}\nSentence to match: {}\n".format (tokens,
                                                                                                             new_sent[
                                                                                                                 idx][
                                                                                                                 'words']))
            idx += 1
        tree.write(outputPath + file)
