from __future__ import unicode_literals
import os
from os import path
import re
import os
import re
import en_core_web_sm #spacy


data_dir = './data/indonesian_bert_all/Indonesian/ner/'

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def xml_iter(file_):
    with open(file_, 'r') as fin:
        for line in fin:
            yield line.strip()



def markupline2bio(line):
            #print(line.split('\t')[0])
        record = line.split('\t')[0]
        #print(record)
        #print(parse(record))
        #print(record[35:40], record[81:90])
        tags = re.findall(r'<ENAMEX\s+TYPE=\"(.+?)\">(.+?)</ENAMEX>', record)
        prev_start = 0
        prev_end = 0
        all_tokens = []
        all_tags = []
        for f in re.finditer(r'<ENAMEX\s+TYPE=\"(.+?)\">(.+?)</ENAMEX>', record):
            #print(record[f.start(0):f.end(0)], f.start(0), f.end(0))
            annotations = re.findall(r'<ENAMEX\s+TYPE=\"(.+?)\">(.+?)</ENAMEX>', record[f.start(0):f.end(0)])
            before_text = record[prev_end:f.start(0)]
            prev_start, prev_end = f.start(0), f.end(0)
            for tok in nlp(before_text):
                if str(tok).strip():
                    all_tokens.append(tok)
                    all_tags.append('O')
            for phrasetag in annotations:
                tag, phrase = annotations[0]
                tokens = nlp(phrase)
                for entity_tok_index, tok in enumerate(tokens):
                    if str(tok).strip():
                        all_tokens.append(tok)
                        if entity_tok_index == 0:
                            all_tags.append("B-" + tag)
                        else:
                            all_tags.append("I-" + tag)
                    else:
                        entity_tok_index -= 1

        after_text = record[prev_end:]
        for tok in nlp(after_text):
            if str(tok).strip():
                all_tokens.append(tok)
                all_tags.append('O')
        return all_tokens, all_tags

if __name__ == '__main__':
    xml_iterator = xml_iter(os.path.join(data_dir, 'data_train_github.txt'))
    #nlp = spacy.load("en_core_web_sm")
    nlp = en_core_web_sm.load()

    i = 0
    for line in xml_iterator:
        i += 1
        if i > 10:
            break
        all_tokens, all_tags = markupline2bio(line.strip())
        #print(all_tokens)
        #print(all_tags)
        print(line)
        for tok, tag in zip(all_tokens, all_tags):
            print(tok, tag)
        print()
