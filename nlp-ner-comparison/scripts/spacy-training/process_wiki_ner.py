from spacy_types import PreSpacyDataset
import os


def process_wiki_ner(path: str, categoriesMapping: dict[str, str]) -> PreSpacyDataset:
    current_directory = os.path.dirname(os.path.realpath(__file__))
    root_directory = os.path.dirname(os.path.dirname(current_directory))
    path = os.path.join(root_directory, path)

    training_data = []

    annotations = []
    accumulator = []

    for line in open(path, "r", encoding="utf-8"):
        if line == "\n":
            continue

        # split line by \t
        lineContent = line.strip().split(" ")
        # discard the first element second element is the word and the last element is the NER tag

        full_sentence = ""

        for entry in lineContent:
            word, _, nerTag = entry.split("|")

            ner_categories = nerTag.split("-")

            if len(ner_categories) == 1:
                nerTag = categoriesMapping[ner_categories[0]]
            elif len(ner_categories) == 2:
                ner_categories[1] = categoriesMapping[ner_categories[1]]
                nerTag = "-".join(ner_categories)

            startPointer = len(full_sentence)

            accumulator.append((word, nerTag, startPointer))

            full_sentence += word + " "

        # annotations.append(accumulator)
        # based on the accumulator and the full sentence create a object similar to   ("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING")]),
        # and append it to the training data
        for annotationEntry in accumulator:
            word, nerTag, start = (
                annotationEntry[0],
                annotationEntry[1],
                annotationEntry[2],
            )

            wordStartIndex = full_sentence.find(word, start)
            wordEndIndex = wordStartIndex + len(word)

            annotations.append((wordStartIndex, wordEndIndex, nerTag))

        training_data.append((full_sentence, annotations))

        accumulator = []
        annotations = []
        full_sentence = ""

    print("amount of sentences in wiki-ner training data: ", len(training_data))
    return training_data


def main():
    process_wiki_ner("../../data/wiki-ner/aij-wikiner-pl-wp3")


if __name__ == "__main__":
    main()
