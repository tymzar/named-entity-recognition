from spacy.cli.train import train
from spacy.cli.evaluate import evaluate

import os
import sys

sys.path.append("../")

from settings import SETTINGS

# get path to current file
MODELS_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "../models/spacy"
)
CONFIG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "config.cfg"
)


def extract_dataset_files(model_path: str) -> [str, str, str]:
    """
    Extract the paths to the train, dev and test dataset files from the model path.

    Args:
        model_path (str): The path to the model folder.

    Returns:
        [str, str, str]: The paths to the train, dev and test dataset files.
    """

    current_data_path = os.path.join(model_path)
    files_in_directory = os.listdir(current_data_path)

    train_dataset_path = ""
    dev_dataset_path = ""
    test_dataset_path = ""

    for file_name in files_in_directory:
        print(file_name)
        if file_name.endswith(".spacy"):
            if file_name.startswith("train"):
                train_dataset_path = os.path.join(current_data_path, file_name)
            elif file_name.startswith("val"):
                dev_dataset_path = os.path.join(current_data_path, file_name)
            elif file_name.startswith("test"):
                test_dataset_path = os.path.join(current_data_path, file_name)

    return train_dataset_path, dev_dataset_path, test_dataset_path


def evaluate_spacy(model_name: str):
    """
    Evaluate a spacy model with the given name.

    Args:
        model_name (str): The name of the model that will be evaluated.

    Raises:
        Exception: If the model does not exist.
    """

    current_model_path = os.path.join(MODELS_PATH, model_name, "out/model-best")

    if not os.path.exists(current_model_path):
        error_message = f"Model {model_name} does not exist."
        raise Exception(error_message)

    _, _, test_data = extract_dataset_files(os.path.join(MODELS_PATH, model_name))

    evaluate(
        current_model_path,
        test_data,
        os.path.join(MODELS_PATH, model_name, "out/evaluation.json"),
    )


def train_spacy(model_name: str):
    """
    Train a spacy model with the given name.

    Args:
        model_name (str): The name of the model that will be trained.

    Raises:
        Exception: If the model does not exist.
    """

    current_model_path = os.path.join(MODELS_PATH, model_name, "out")
    current_dataset_path = os.path.join(MODELS_PATH, model_name)

    if not os.path.exists(current_model_path):
        # create a dir for model output
        os.makedirs(current_model_path, exist_ok=True)

    train_data, dev_data, _ = extract_dataset_files(current_dataset_path)

    train(
        CONFIG_FILE_PATH,
        output_path=current_model_path,
        overrides={
            "paths.train": train_data,
            "paths.dev": dev_data,
        },
    )

    evaluate_spacy(model_name)


def main():
    """
    Main function that trains model from the settings file.
    """

    # train_spacy(SETTINGS["model-name"])

    model_name = SETTINGS["model-name"]

    current_model_path = os.path.join(MODELS_PATH, model_name, "out/model-best")

    _, _, test_data = extract_dataset_files(os.path.join(MODELS_PATH, model_name))

    print(test_data)
    evaluate(
        current_model_path,
        test_data,
        os.path.join(MODELS_PATH, model_name, "out/evaluation.json"),
    )


if __name__ == "__main__":
    main()
