import spacy
import os
import threading
import time

from collections.abc import Sequence
from multiprocessing import Process
from settings import DATASETS, SETTINGS
from spacy.tokens import DocBin
from spacy_types import PreSpacyDataset
from process_conllu import process_conllu
from process_wiki_ner import process_wiki_ner
from spacy_datasets_utils import split_dataset_to_triple_split, write_to_spacy_format
from process_iob import process_iob
from process_nkjp import process_nkjp


def dataset_to_disk(
    dataset: PreSpacyDataset,
    document_binary: DocBin,
    nlp: spacy.language.Language,
    dataset_type: str,
):
    start_time = time.perf_counter()

    write_to_spacy_format(dataset, document_binary, nlp, dataset_type)

    file_size_mb = os.path.getsize(dataset_type + ".spacy") / (1024 * 1024)

    print(
        "Dataset ",
        dataset_type,
        "dataset length: ",
        len(dataset),
        "file size: ",
        file_size_mb,
        "MB",
    )

    end_time = time.perf_counter()

    print(f"Finished in {round(end_time - start_time, 2)} second(s)")


def main():
    # Start timer
    start_time = time.perf_counter()

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
                (
                    doc_object_train_proc,
                    doc_object_test_proc,
                    doc_object_val_proc,
                ) = process_nkjp(
                    doc_object_train,
                    doc_object_test,
                    doc_object_val,
                    nlp,
                    categoriesMapping=dataset["categoriesMapping"],
                )

                doc_object["test"] = doc_object_test_proc
                doc_object["val"] = doc_object_val_proc
                doc_object["train"] = doc_object_train_proc
            case _:
                print("Dataset format not supported", dataset["type"])

    # thread_train = threading.Thread(
    #     target=write_to_spacy_format,
    #     args=(dataset_dict["train"], doc_object["train"], nlp),
    # )

    # thread_test = threading.Thread(
    #     target=write_to_spacy_format,
    #     args=(dataset_dict["test"], doc_object["test"], nlp),
    # )

    # thread_val = threading.Thread(
    #     target=write_to_spacy_format,
    #     args=(dataset_dict["val"], doc_object["val"], nlp),
    # )

    # thread_dict = {
    #     "train": thread_train,
    #     "test": thread_test,
    #     "val": thread_val,
    # }

    # for _, dataset_type in enumerate(dataset_dict):
    #     # TODO: add multithreading for this

    #     print("Starting data prepare thread for: ", dataset_type)
    #     doc_object[dataset_type] = thread_dict[dataset_type].start()

    # thread_write_train = threading.Thread(
    #     target=doc_object_train.to_disk, args=("train.spacy",)
    # )

    # thread_write_test = threading.Thread(
    #     target=doc_object_test.to_disk, args=("test.spacy",)
    # )

    # thread_write_val = threading.Thread(
    #     target=doc_object_val.to_disk, args=("val.spacy",)
    # )

    # thread_write_dict = {
    #     "train": thread_write_train,
    #     "test": thread_write_test,
    #     "val": thread_write_val,
    # }

    # for _, dataset_type in enumerate(dataset_dict):
    #     print("Joining and waiting for a thread for: ", dataset_type)
    #     doc_object[dataset_type] = thread_dict[dataset_type].join()

    #     print("Starting dataset write thread for: ", dataset_type)
    #     thread_write_dict[dataset_type].start()

    # for _, dataset_type in enumerate(dataset_dict):
    #     print("Joining and waiting for a thread for: ", dataset_type)
    #     thread_write_dict[dataset_type].join()

    #     file_size_mb = os.path.getsize(dataset_type + ".spacy") / (1024 * 1024)

    #     print(
    #         "Dataset ",
    #         dataset_type,
    #         "dataset length: ",
    #         len(dataset_dict[dataset_type]),
    #         "file size: ",
    #         file_size_mb,
    #         "MB",
    #     )

    if SETTINGS["multi-operation"] == "threading":
        thread_array: Sequence[threading.Thread] = []

        for _, dataset_type in enumerate(dataset_dict):
            new_thread = threading.Thread(
                target=dataset_to_disk,
                args=(
                    dataset_dict[dataset_type],
                    doc_object[dataset_type],
                    nlp,
                    dataset_type,
                ),
            )

            thread_array.append(new_thread)

        for thread in thread_array:
            print("Starting dataset write thread for: ", thread.name)
            thread.start()

        for thread in reversed(thread_array):
            print("Joining and waiting for a thread for: ", thread.name)
            thread.join()
    elif SETTINGS["multi-operation"] == "processing":
        process_array: Sequence[Process] = []

        for _, dataset_type in enumerate(dataset_dict):
            new_process = Process(
                target=dataset_to_disk,
                args=(
                    dataset_dict[dataset_type],
                    doc_object[dataset_type],
                    nlp,
                    dataset_type,
                ),
            )

            process_array.append(new_process)

        for process in process_array:
            print("Starting dataset write process for: ", process.name)
            process.start()

        for process in reversed(process_array):
            print("Joining and waiting for a process for: ", process.name)
            process.join()

    end_time = time.perf_counter()

    print(f"Full process finished in {round(end_time - start_time, 2)} second(s)")


if __name__ == "__main__":
    main()
