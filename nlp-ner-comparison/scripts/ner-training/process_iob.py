from spacy_types import PreFormatDataset
import os


def process_iob(
    path: str, categoriesMapping: dict[str, str], categories_prefix: bool
) -> PreFormatDataset:
    current_directory = os.path.dirname(os.path.realpath(__file__))
    root_directory = os.path.dirname(os.path.dirname(current_directory))
    path = os.path.join(root_directory, path)

    dataset_contents = open(path, "r", encoding="utf-8")

    training_data: PreFormatDataset = []

    annotations = []
    accumulator = []
    full_sentence = ""

    for line in dataset_contents.readlines():
        # read line by line till the empty line and store them in accumulator
        if line == "\n" and accumulator != []:
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
        elif line != "\n":
            is_previous_ner_tag = False
            lineContent = line.strip().split("\t")
            # discard the first element second element is the word and the last element is the NER tag
            if len(lineContent) != 4:
                continue

            word, _, _, nerTag = (
                lineContent[0],
                lineContent[1],
                lineContent[2],
                lineContent[3],
            )

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

            # make a object to append to the accumulator that consists of the word and the NER tag
            startPointer = len(full_sentence)

            accumulator.append((word, nerTag, startPointer))
            # append the word to the full sentence
            full_sentence += word + " "

    print("amount of sentences in iob training data: ", len(training_data))
    return training_data


def main():
    process_iob("../../data/cen/train.iob")


if __name__ == "__main__":
    main()
