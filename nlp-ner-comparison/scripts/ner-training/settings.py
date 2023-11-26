from typing import TypedDict
from collections.abc import Sequence
from ner_categories_mapping import CEN_AND_KPWR_CATEGORIES_MAPPING


class DatasetDetails(TypedDict):
    name: str
    path: str
    format: str
    modules: list[str]
    categoriesMapping: dict[str, str]


SETTINGS = {
    "model-name": "prefix-partial",
    "ner-tools": ["bert"],  # set to ["spacy", "mitie", "bert"]
    "multi-operation": "processing",  # set to "processing" or "threading"
    "category-prefix": True,
    "datasets-to-process": [
        "cen-1.0",
        "kpwr",
        "multinerd",
        # "nkjp",
        "wikineural",
        "wiki-ner",
    ],  # set all datasets that you want to process
}

DATASETS: Sequence[DatasetDetails] = [
    {
        "name": "nkjp",
        "path": "data/nkjp",
        "format": "nkjp",
        "modules": [],
        "categoriesMapping": {
            "GEOGNAME": "LOCATION",
            "TIME": "TIME",
            "ORGNAME": "ORGNAME",
            "PERSNAME": "PERSON",
            "DATE": "TIME",
            "PLACENAME": "LOCATION",
            "O": "O",
        },
    },
    {
        "name": "cen-1.0",
        "path": "data/cen",
        "modules": ["train", "test", "val"],
        "format": "iob",
        "categoriesMapping": CEN_AND_KPWR_CATEGORIES_MAPPING,
    },
    {
        "name": "kpwr",
        "path": "data/kpwr-ner",
        "modules": ["train", "test"],
        "format": "iob",
        "categoriesMapping": CEN_AND_KPWR_CATEGORIES_MAPPING,
    },
    {
        "name": "multinerd",
        "path": "data/multinerd",
        "modules": ["train", "test", "val"],
        "format": "connlu",
        "categoriesMapping": {
            "PER": "PERSON",
            "LOC": "LOCATION",
            "ORG": "ORGNAME",
            "ANIM": "O",
            "BIO": "O",
            "CEL": "O",
            "DIS": "O",
            "EVE": "EVENT",
            "FOOD": "O",
            "INST": "O",
            "MEDIA": "O",
            "PLANT": "O",
            "MYTH": "O",
            "TIME": "TIME",
            "VEHI": "O",
            "O": "O",
        },
    },
    {
        "name": "wikineural",
        "path": "data/wikineural",
        "modules": ["train", "test", "val"],
        "format": "connlu",
        "categoriesMapping": {
            "ORG": "ORGNAME",
            "MISC": "O",
            "PER": "PERSON",
            "LOC": "LOCATION",
            "O": "O",
        },
    },
    {
        "name": "wiki-ner",
        "path": "data/wiki-ner/aij-wikiner-pl-wp3",
        "format": "wiki-ner",
        "modules": [],
        "categoriesMapping": {
            "LOC": "LOCATION",
            "ORG": "ORGNAME",
            "PER": "PERSON",
            "MISC": "O",
            "NON": "O",
            "DAB": "O",
            "O": "O",
        },
    },
]
