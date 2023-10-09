import os

BASE_DATA_PATH = "../../data/bsnlp-2019/"
ANNOTATED="annotated/"
RAW="raw/"
LANGUAGES="pl/"
DATA_SOURCES=['ryanair/', 'nord_stream/']
DATASETS_TRAIN="training"

class FileEntry():          # leave this empty
    def __init__(self):   # constructor function using self
        self.raw = None  # variable using self.
        self.annotated = None  # variable using self

def create_training_data(file_raw, file_annotated):
    training_data = []
    sentences = []
    annotations = []
    accumulator = []
    
    # remove first 4 lines
    full_text = file_raw.readlines()[4:]
    current_point = 0
    
    
    for line in file_annotated:
        #read line by line till the empty line and store them in accumulator
                if line == "\n" and accumulator != []:
                    # annotations.append(accumulator)
                    # based on the accumulator and the full sentence create a object similar to   ("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING")]),
                    # and append it to the training data
                    lastWordIndex = 0
                    for annotationEntry in accumulator:
                        word, nerTag, start = annotationEntry[0], annotationEntry[1], annotationEntry[2]

                        wordStartIndex = full_text.find(word, start)
                        wordEndIndex = wordStartIndex + len(word)
                        
                        #update the last word index
                        lastWordIndex = wordEndIndex
                        
                        annotations.append((wordStartIndex, wordEndIndex, nerTag))



                    training_data.append((full_text, annotations))
                    
                    accumulator = []
                    annotations = []
                else:
                    # split line by \t
                    lineContent = line.strip().split("\t")
                    # discard the first element second element is the word and the last element is the NER tag
                    if len(lineContent) < 3:
                        continue

                    word, _, nerTag = lineContent[0], lineContent[1], lineContent[2]
                    # make a object to append to the accumulator that consists of the word and the NER tag
                    
                    wordStartIndex = full_text.find(word, start)

                    startPointer = current_point
                    current_point += len(word)
                    
                    if nerTag != "O":
                        accumulator.append((word, nerTag, startPointer))

    
    return training_data


def main():
    resolve_path = lambda x: os.path.join(BASE_DATA_PATH, x)
    files=[]
    
    for data_source in DATA_SOURCES:
        print("Current data source: ", data_source)
        
        for file in os.listdir(resolve_path(ANNOTATED + data_source + LANGUAGES)):
            file_entry = FileEntry()
            
            # get file content
            file_entry.annotated = open(resolve_path(ANNOTATED + data_source + LANGUAGES + file), "r")
            file_entry.raw = open(resolve_path(RAW + data_source + LANGUAGES + file), "r")
            
            files.append(file_entry)            

    dataset = []
    for file in files:
        dataset.append(create_training_data(file.raw, file.annotated))
    

if __name__ == "__main__":
    main()