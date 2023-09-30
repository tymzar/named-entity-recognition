import spacy
from spacy.tokens import DocBin
import re
nlp = spacy.load("pl_core_news_lg")
nlp = spacy.blank("pl")
training_data = []
# Read your CoNLL-U format data
with open("../data/wikineural/val.conllu", "r", encoding="utf-8") as file:
 sentences = []
 annotations = []

 accumulator = []
 full_sentence = ""
 for line in file:
      #read line by line till the empty line and store them in accumulator
            if line == "\n" and accumulator != []:
                # annotations.append(accumulator)
                # based on the accumulator and the full sentence create a object similar to   ("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING")]),
                # and append it to the training data
                lastWordIndex = 0
                for annotationEntry in accumulator:
                    word, nerTag, start = annotationEntry[0], annotationEntry[1], annotationEntry[2]


                    
                    wordStartIndex = full_sentence.find(word, start)
                    wordEndIndex = wordStartIndex + len(word)
                    
                    #update the last word index
                    lastWordIndex = wordEndIndex
                    
                    annotations.append((wordStartIndex, wordEndIndex, nerTag))
                    
                    
                    # wordStartIndex = full_sentence.find(word)
                    # wordEndIndex = wordStartIndex + len(word)
                    # annotations.append((wordStartIndex, wordEndIndex, nerTag))
            
            
            
                training_data.append((full_sentence, annotations))
                
                accumulator = []
                annotations = []
                full_sentence = ""
            else:
                # split line by \t
                lineContent = line.strip().split("\t")
                # discard the first element second element is the word and the last element is the NER tag
                if len(lineContent) < 3:
                    continue
                
                
                
                _, word, nerTag = lineContent[0], lineContent[1], lineContent[2]
                # make a object to append to the accumulator that consists of the word and the NER tag
                
                startPointer = len(full_sentence)
                
                if nerTag != "O":
                    accumulator.append((word, nerTag, startPointer))
                # append the word to the full sentence
                full_sentence += word + " "
    
            
db = DocBin()
for text, annotations in training_data:
    doc = nlp(text)
    ents = []
    # print(text)
    # print(annotations)
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        # print(span)
        ents.append(span)
        
    # print(ents)
    doc.ents = ents
    db.add(doc)
db.to_disk("./dev.spacy")