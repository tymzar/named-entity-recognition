import spacy
import os
from settings import DATASETS
from spacy.tokens import DocBin
from spacy_types import PreSpacyDataset
from process_conllu import process_conllu
from process_wiki_ner import process_wiki_ner
from spacy_datasets_utils import split_dataset_to_triple_split, write_to_spacy_format
from process_iob import process_iob
from process_nkjp import process_nkjp


def main():
    doc_object_train = DocBin()
    doc_object_test = DocBin()
    doc_object_val = DocBin()

    nlp = spacy.load("pl_core_news_lg")

    train_dataset: PreSpacyDataset = []
    test_dataset: PreSpacyDataset = []
    val_dataset: PreSpacyDataset = []

    dataset_dict = {
        "train": train_dataset,
        "test": test_dataset,
        "val": val_dataset,
    }

    doc_object = {
        "train": doc_object_train,
        "test": doc_object_test,
        "val": doc_object_val,
    }

    for dataset in DATASETS:
        match dataset["format"]:
            case "connlu":
                for module in dataset["modules"]:
                    dataset_dict[module].extend(
                        process_conllu(
                            dataset["path"] + "/" + module + ".conllu",
                            categoriesMapping=dataset["categoriesMapping"],
                        )
                    )
            case "iob":
                for module in dataset["modules"]:
                    dataset_dict[module].extend(
                        process_iob(
                            dataset["path"] + "/" + module + ".iob",
                            categoriesMapping=dataset["categoriesMapping"],
                        )
                    )

            case "wiki-ner":
                extracted_dataset = process_wiki_ner(
                    dataset["path"], categoriesMapping=dataset["categoriesMapping"]
                )

                (
                    extracted_train_dataset,
                    extracted_test_dataset,
                    extracted_val_dataset,
                ) = split_dataset_to_triple_split(extracted_dataset)

                dataset_dict["train"].extend(extracted_train_dataset)
                dataset_dict["test"].extend(extracted_test_dataset)
                dataset_dict["val"].extend(extracted_val_dataset)
            case "nkjp":
                doc_object_train, doc_object_test, doc_object_val = process_nkjp(
                    doc_object_train,
                    doc_object_test,
                    doc_object_val,
                    nlp,
                    categoriesMapping=dataset["categoriesMapping"],
                )
            case _:
                print("Dataset format not supported", dataset["type"])

    for _, dataset_type in enumerate(dataset_dict):
        # TODO: add multithreading for this
        doc_object[dataset_type] = write_to_spacy_format(
            dataset_dict[dataset_type], doc_object[dataset_type], nlp
        )

        # TODO: add multithreading for this
        doc_object[dataset_type].to_disk(dataset_type + ".spacy")
        # print dataset length and file size
        file_size_mb = os.path.getsize(dataset_type + ".spacy") / (1024 * 1024)

        print(
            "Dataset ",
            dataset_type,
            "dataset length: ",
            len(dataset_dict[dataset_type]),
            "file size: ",
            file_size_mb,
            "MB",
        )


if __name__ == "__main__":
    main()
