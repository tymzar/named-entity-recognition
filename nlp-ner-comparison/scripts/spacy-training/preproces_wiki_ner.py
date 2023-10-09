import spacy
from spacy.tokens import DocBin
nlp = spacy.load("pl_core_news_lg")
nlp = spacy.blank("pl")

WIKI_NER_FILE = "../../data/ner/wikiner/wiki-ner/aij-wikiner-pl-wp3"

def split_dataset_to_triple_split(dataset):
    
    train_dataset = [] # 80%
    val_dataset = [] # 10%
    test_dataset = [] # 10%
    
    # insure that the dataset is sorted and shuffled splits must be random but unique
    dataset.sort()
    
    # get the length of the dataset
    dataset_length = len(dataset)
    
    # get the 80% of the dataset
    train_dataset_length = int(dataset_length * 0.8)
    
    # get the 10% of the dataset
    val_dataset_length = int(dataset_length * 0.1)
    
    # get the 10% of the dataset
    test_dataset_length = int(dataset_length * 0.1)
    
    # get the train dataset
    train_dataset = dataset[:train_dataset_length]
    
    # get the val dataset
    val_dataset = dataset[train_dataset_length:train_dataset_length + val_dataset_length]
    
    # get the test dataset
    test_dataset = dataset[train_dataset_length + val_dataset_length:]
    
    return train_dataset, val_dataset, test_dataset

def convert_to_spacy_format():
    training_data = []

    annotations = []
    accumulator = []
 
    for line in open(WIKI_NER_FILE, "r", encoding="utf-8"):
        
        if line == "\n":
            continue
        
        # split line by \t
        lineContent = line.strip().split(" ")
        # discard the first element second element is the word and the last element is the NER tag
        
        full_sentence = ""
        
        for entry in lineContent:
            word, _, nerTag = entry.split("|")
            
            startPointer = len(full_sentence)

            if nerTag != "O":
                accumulator.append((word, nerTag, startPointer))
        
            full_sentence += word + " "

        # annotations.append(accumulator)
        # based on the accumulator and the full sentence create a object similar to   ("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING")]),
        # and append it to the training data
        for annotationEntry in accumulator:
            word, nerTag, start = annotationEntry[0], annotationEntry[1], annotationEntry[2]

            wordStartIndex = full_sentence.find(word, start)
            wordEndIndex = wordStartIndex + len(word)
        
            
            annotations.append((wordStartIndex, wordEndIndex, nerTag))
    
        training_data.append((full_sentence, annotations))
        
        accumulator = []
        annotations = []
        full_sentence = ""
    
def write_to_spacy_format(dataset, file_name):
    
    db = DocBin()
    
    for text, annotations in dataset:
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
        
    db.to_disk(file_name)

def main():
    
    dataset = convert_to_spacy_format()
        
    train_dataset, val_dataset, test_dataset = split_dataset_to_triple_split(dataset)
    
    for dataset, file_name in [(train_dataset, "train.spacy"), (val_dataset, "val.spacy"), (test_dataset, "test.spacy")]:
        write_to_spacy_format(dataset, file_name)


if __name__ == "__main__":
    main()