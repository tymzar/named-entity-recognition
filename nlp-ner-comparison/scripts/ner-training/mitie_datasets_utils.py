import os
import json
from datetime import datetime
from spacy_types import PreFormatDataset


def write_to_mitie_format(
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
    write_path = name + ".json"
    os.makedirs(os.path.dirname(write_path), exist_ok=True)
    dataset_file = open(write_path, "w")

    label_accumulator = {}

    clean_mitie_train_data = []
    # create data for ner training
    for sentence in dataset:
        text, annotations, _ = sentence

        clean_mitie_train_data.append((text, annotations))

        for _, _, ner_tag in annotations:
            if ner_tag in label_accumulator:
                label_accumulator[ner_tag] += 1
            else:
                label_accumulator[ner_tag] = 1

    dataset_file.write(json.dumps(clean_mitie_train_data))
    dataset_file.close()
