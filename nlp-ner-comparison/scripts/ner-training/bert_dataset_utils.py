import os
import pyconll
import spacy

from spacy_types import PreFormatDataset


def write_to_conllu_format(
    dataset: PreFormatDataset,
    tool: str,
    name: str,
) -> None:
    """
    Function that writes the dataset to a conllu format file.

    Args:
        dataset (SpacyDataset): The dataset that will be written to the file.
        file_name (str): The name of the file that will be written.
    """
    write_path = name + ".conll"
    os.makedirs(os.path.dirname(write_path), exist_ok=True)
    dataset_file = open(write_path, "w")

    nlp = spacy.load("pl_core_news_sm")

    for sentence in dataset:
        text, annotations, isToSkip = sentence

        if tool == "spacy" and isToSkip:
            continue

        for annotation_entry in annotations:
            start_index, end_index, ner_tag = annotation_entry

            current_word = (
                text[start_index:end_index].replace(" ", "").replace("\n", "")
            )

            parsed_word = nlp(current_word)[0]

            pos_tag = parsed_word.pos_
            syntactic_tag = parsed_word.dep_

            dataset_file.write(
                current_word
                + "\t"
                + pos_tag
                + "\t"
                + syntactic_tag
                + "\t"
                + ner_tag
                + "\n"
            )

        dataset_file.write("\n")

    dataset_file.close()
