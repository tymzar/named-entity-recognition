import spacy
import os
import threading
import time

from collections.abc import Sequence
from multiprocessing import Process
from settings import DATASETS, SETTINGS
from spacy.tokens import DocBin
from spacy_types import PreFormatDataset
from process_conllu import process_conllu
from process_wiki_ner import process_wiki_ner
from spacy_datasets_utils import split_dataset_to_triple_split, write_to_spacy_format
from stanford_datasets_utils import write_to_stanford_format
from process_iob import process_iob
from process_nkjp import process_nkjp, process_flat_dataset


def dataset_to_disk(
    dataset: PreFormatDataset,
    document_binary: DocBin,
    nlp: spacy.language.Language,
    tool: str,
    model_name: str,
    dataset_type: str,
):
    start_time = time.perf_counter()
    dataset_path = model_name + "/" + dataset_type

    match tool:
        case "spacy":
            write_to_spacy_format(dataset, document_binary, nlp, tool, dataset_path)

            file_size_mb = os.path.getsize(dataset_path + ".spacy") / (1024 * 1024)

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

        case "stanford":
            write_to_stanford_format(dataset, tool, dataset_path)

            file_size_mb = os.path.getsize(dataset_path + ".tsv") / (1024 * 1024)

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

        case "robert":
            print("RoBERTa NER not supported yet")


def main():
    # Start timer
    start_time = time.perf_counter()
    # do loop for     "ner-tools": ["spacy"],  # set to ["spacy", "stanford", "bert"]

    doc_object_train = DocBin()
    doc_object_test = DocBin()
    doc_object_val = DocBin()

    nlp = spacy.load("pl_core_news_lg")

    train_dataset: PreFormatDataset = []
    test_dataset: PreFormatDataset = []
    val_dataset: PreFormatDataset = []

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

    datasets_to_process = DATASETS

    if SETTINGS["datasets-to-process"] != []:
        datasets_to_process = filter(
            lambda dataset: dataset["name"] in SETTINGS["datasets-to-process"], DATASETS
        )
    else:
        print("No datasets to process set, processing all datasets")

    for dataset in datasets_to_process:
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

                (
                    dataset_train_dictionary,
                    dataset_test_dictionary,
                    dataset_val_dictionary,
                ) = process_flat_dataset(categoriesMapping=dataset["categoriesMapping"])

                dataset_dict["train"].extend(dataset_train_dictionary)
                dataset_dict["test"].extend(dataset_test_dictionary)
                dataset_dict["val"].extend(dataset_val_dictionary)

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

    for tool in SETTINGS["ner-tools"]:
        model_name = "./models/" + tool + "/" + SETTINGS["model-name"]

        if SETTINGS["multi-operation"] == "threading":
            thread_array: Sequence[threading.Thread] = []

            for _, dataset_type in enumerate(dataset_dict):
                new_thread = threading.Thread(
                    target=dataset_to_disk,
                    args=(
                        dataset_dict[dataset_type],
                        doc_object[dataset_type],
                        nlp,
                        tool,
                        model_name,
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
                        tool,
                        model_name,
                        dataset_type,
                    ),
                )

                process_array.append(new_process)

            for process in process_array:
                print("Starting dataset write process for tool: {tool}: ", process.name)
                process.start()

            for process in reversed(process_array):
                print(
                    "Joining and waiting for a process for tool: {tool}: ", process.name
                )
                process.join()

        end_time = time.perf_counter()

        print(
            f"Full process for tool: {tool} finished in {round(end_time - start_time, 2)} second(s)"
        )


if __name__ == "__main__":
    main()
