from spacy_types import PreFormatDataset
import os


def process_wiki_ner(
    path: str, categoriesMapping: dict[str, str], categories_prefix=False
) -> PreFormatDataset:
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
            is_previous_ner_tag = False
            word, _, nerTag = entry.split("|")

            ner_categories = nerTag.split("-")

            if len(ner_categories) == 1:
                nerTag = categoriesMapping[ner_categories[0]]

                if nerTag != "O" and categories_prefix:
                    if is_previous_ner_tag:
                        nerTag = "I-" + nerTag
                    else:
                        nerTag = "B-" + nerTag

                if nerTag.startswith("B-"):
                    is_previous_ner_tag = True

                if nerTag.startswith("O"):
                    is_previous_ner_tag = False

            elif len(ner_categories) == 2:
                if categories_prefix and categoriesMapping[ner_categories[1]] != "O":
                    ner_categories[1] = categoriesMapping[ner_categories[1]]
                    nerTag = "-".join(ner_categories)
                else:
                    nerTag = categoriesMapping[ner_categories[1]]

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

        training_data.append((full_sentence, annotations, False))

        accumulator = []
        annotations = []
        full_sentence = ""

    print("amount of sentences in wiki-ner training data: ", len(training_data))
    return training_data


def main():
    process_wiki_ner("../../data/wiki-ner/aij-wikiner-pl-wp3")


if __name__ == "__main__":
    main()
