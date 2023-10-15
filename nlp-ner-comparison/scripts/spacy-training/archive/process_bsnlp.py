# TODO: to decide if this data is useful for our project

import os
from spacy_types import PreSpacyDataset
import spacy_datasets_utils
from io import TextIOWrapper


class FileEntry:  # leave this empty
    def __init__(self):  # constructor function using self
        self.raw: TextIOWrapper = None  # variable using self.
        self.annotated: TextIOWrapper = None  # variable using self


def create_training_data(
    file_raw: TextIOWrapper, file_annotated: TextIOWrapper, module
):
    training_data: PreSpacyDataset = []
    annotations = []
    accumulator = []
    full_text = ""

    print("Current file: ", file_raw.name)

    file_raw = file_raw.readlines()[4:]
    file_annotated = file_annotated.readlines()[1:]

    full_text = "".join(file_raw)

    # remove first 4 lines
    current_point = 0

    for line in file_annotated:
        # read line by line till the empty line and store them in accumulator
        if line != "\n":
            # split line by \t
            lineContent = line.strip().split("\t")
            # discard the first element second element is the word and the last element is the NER tag
            if len(lineContent) < 3:
                continue

            word, _, nerTag = lineContent[0], lineContent[1], lineContent[2]
            # make a object to append to the accumulator that consists of the word and the NER tag

            print(word, nerTag, current_point)

            wordStartIndex = full_text.find(word, current_point - 5)

            print(wordStartIndex)

            startPointer = current_point
            current_point += len(word)

            accumulator.append((word, nerTag, startPointer))

        if accumulator != []:
            for annotationEntry in accumulator:
                word, nerTag, start = (
                    annotationEntry[0],
                    annotationEntry[1],
                    annotationEntry[2],
                )

                wordStartIndex = full_text.find(word, start)
                wordEndIndex = wordStartIndex + len(word)

                annotations.append((wordStartIndex, wordEndIndex, nerTag))

            training_data.append((full_text, annotations))

    return training_data


def process_bsnlp(path: str, module: str) -> PreSpacyDataset:
    ANNOTATED = "annotated/"
    RAW = "raw/"
    LANGUAGES = "pl/"
    DATA_SOURCES = ["ryanair/", "nord_stream/"]
    PATH_TRAIN = "train/" if module == "train" else ""

    print("Current module: ", module, PATH_TRAIN)

    if module == "train":
        DATA_SOURCES = ["", ""]

    resolve_path = lambda x: os.path.join(path, x)
    files_annotated = []
    files_raw = []
    files: list[FileEntry] = []

    for data_source in DATA_SOURCES:
        print("Current data source: ", data_source)

        for file in os.listdir(
            resolve_path(PATH_TRAIN + ANNOTATED + data_source + LANGUAGES)
        ):
            # get file content
            annotated = open(
                resolve_path(PATH_TRAIN + ANNOTATED + data_source + LANGUAGES + file),
                "r",
            )

            files_annotated.append(annotated)

        for file in os.listdir(
            resolve_path(PATH_TRAIN + RAW + data_source + LANGUAGES)
        ):
            # get file content
            raw = open(
                resolve_path(PATH_TRAIN + RAW + data_source + LANGUAGES + file), "r"
            )

            files_raw.append(raw)

    if len(files_annotated) != len(files_raw):
        print("Files are not equal")
        exit(1)

    for file_property in zip(files_raw, files_annotated):
        file_entry = FileEntry()
        file_entry.raw = file_property[0]
        file_entry.annotated = file_property[1]
        files.append(file_entry)

    dataset: PreSpacyDataset = []

    for file in files:
        dataset.extend(create_training_data(file.raw, file.annotated, module))

    print("dataset length", len(dataset), dataset[-1])

    spacy_datasets_utils.write_to_spacy_format(dataset, "bsnlp.spacy")

    return dataset


def main():
    process_bsnlp("../../data/bsnlp-2019/", "train")


if __name__ == "__main__":
    main()
