import os
import spacy
import random

from spacy_types import PreSpacyDataset
from spacy.tokens import DocBin


def write_to_spacy_format(
    dataset: PreSpacyDataset,
    document_object: DocBin,
    nlp: spacy.language.Language,
    name: str,
) -> None:
    """
    Function that writes the dataset to a spacy format file.

    Args:
        dataset (SpacyDataset): The dataset that will be written to the file.
        file_name (str): The name of the file that will be written.
    """

    for text, annotations in dataset:
        doc = nlp(text)
        ents = []
        # print(text)
        # print(annotations)
        for start, end, label in annotations:
            # print(doc.char_span(start, end, label=label))
            span = doc.char_span(start, end, label=label)
            # print(span)
            ents.append(span)

        # print(ents)
        doc.ents = ents
        document_object.add(doc)

    write_path = name + ".spacy"

    # make a directory if it does not exist
    os.makedirs(os.path.dirname(write_path), exist_ok=True)

    document_object.to_disk(name + ".spacy")


def split_dataset_to_triple_split(
    dataset: PreSpacyDataset,
) -> tuple[PreSpacyDataset, PreSpacyDataset, PreSpacyDataset]:
    """
    Split the dataset into train, val and test datasets. The split is 80% train, 10% val and 10% test.s

    Args:
        dataset (SpacyDataset): The dataset that will be split.

    Returns:
        tuple[SpacyDataset, SpacyDataset, SpacyDataset]: The train, val and test datasets.
    """

    train_dataset = []  # 80%
    val_dataset = []  # 10%
    test_dataset = []  # 10%

    # insure that the dataset is sorted and shuffled splits must be random but unique
    dataset.sort()

    # shuffle the dataset
    random.shuffle(dataset)

    # get the length of the dataset
    dataset_length = len(dataset)

    # get the 80% of the dataset
    train_dataset_length = int(dataset_length * 0.8)

    # get the 10% of the dataset
    val_dataset_length = int(dataset_length * 0.1)

    # get the train dataset
    train_dataset = dataset[:train_dataset_length]

    # get the val dataset
    val_dataset = dataset[
        train_dataset_length : train_dataset_length + val_dataset_length
    ]

    # get the test dataset
    test_dataset = dataset[train_dataset_length + val_dataset_length :]

    return train_dataset, val_dataset, test_dataset
