import os

from spacy_types import PreFormatDataset


def write_to_stanford_format(
    dataset: PreFormatDataset,
    tool: str,
    name: str,
) -> None:
    """
    Function that writes the dataset to a spacy format file.

    Args:
        dataset (SpacyDataset): The dataset that will be written to the file.
        file_name (str): The name of the file that will be written.
    """
    write_path = name + ".tsv"
    os.makedirs(os.path.dirname(write_path), exist_ok=True)
    dataset_file = open(write_path, "w")

    for sentence in dataset:
        text, annotations, isToSkip = sentence
        if tool == "spacy" and isToSkip:
            continue

        for annotation_entry in annotations:
            start_index, end_index, ner_tag = annotation_entry

            current_word = text[start_index:end_index]
            dataset_file.write(current_word + "\t" + ner_tag + "\n")

        dataset_file.write("\n")

    dataset_file.close()
