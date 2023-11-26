#!/usr/bin/python
#
#    This example shows how to use the MITIE Python API to train a named_entity_extractor.
#
#
import sys, os

# Make sure you put the mitielib folder into the python search path.  There are
# a lot of ways to do this, here we do it programmatically with the following
# two statements:

from mitie import *


CurrentSentence = list[tuple[tuple[int, int], str]]

# define mitie dataset type that will be a list of tuples of type ((int,int), string) where the first element of the tuple is a range of indexes of the word in the sentence and the second element is the tag of the word
MitieFormatDataset = list[tuple[CurrentSentence, list[str]]]


def process_conllu(path: str, list_entities: dict[str, int]) -> MitieFormatDataset:
    # read conllu file line by line
    # if line is empty then create a new sentence
    dataset: MitieFormatDataset = []
    current_file = open(path, "r", encoding="utf-8")

    # sentence_cutoff = 0

    current_range = []
    words = []
    current_ner_tag = "O"
    current_sentence_token_index = 0

    current_sentence: CurrentSentence = []

    for index, line in enumerate(current_file.readlines()):
        if line == "\n":
            dataset.append((current_sentence, words))

            current_sentence = []
            words = []
            current_sentence_token_index = 0
            current_ner_tag = "O"
            current_range = []

            # sentence_cutoff += 1

            # if sentence_cutoff > 5:
            #     break

            continue

        line_content = line.strip().split("\t")

        if len(line_content) not in [4]:
            # throw error
            raise Exception("Invalid line format")

        word, _, _, ner_tag = line_content

        if index == 0:
            current_ner_tag = ner_tag

        words.append(word)

        if ner_tag == "O":
            if len(current_range) != 0 and current_ner_tag != "O":
                current_range.append(current_sentence_token_index)
                current_sentence.append((tuple(current_range), current_ner_tag))
                current_range = []

            current_ner_tag = "O"
            current_sentence_token_index += 1
            continue

        if current_ner_tag == "O":
            current_range.append(current_sentence_token_index)

        if current_ner_tag != "O" and ner_tag != current_ner_tag:
            current_range.append(current_sentence_token_index)
            current_sentence.append((tuple(current_range), current_ner_tag))
            current_range = []

        current_ner_tag = ner_tag
        current_sentence_token_index += 1

    return dataset


def read_conll_data(paths: list[str]) -> MitieFormatDataset:
    full_dataset: MitieFormatDataset = []
    list_entities = {}

    for path in paths:
        dataset = process_conllu(path, list_entities)

        full_dataset.extend(dataset)

    return full_dataset


def train_mitie_ner_model():
    # read conll data
    dataset = read_conll_data(
        [
            "../models/mitie/all-no-nkjp/val.conll",
            "../models/mitie/all-no-nkjp/train.conll",
        ]
    )

    # prepaire data for mitie

    all_miteie_samples = []

    for current_sentence, words in dataset:
        current_mitie_sample = ner_training_instance(words)

        for token_range, tag in current_sentence:
            if len(token_range) != 2:
                continue

            start, end = token_range

            current_mitie_sample.add_entity(xrange(start, end), tag)

        all_miteie_samples.append(current_mitie_sample)

    trainer = ner_trainer(
        "../models/mitie/base/pl-mitie-lg/total_word_feature_extractor.dat"
    )

    trainer.num_threads = 10

    checkpoint = int(len(all_miteie_samples) / 10)

    print("Checkpoint: ", checkpoint)

    for index, sample in enumerate(all_miteie_samples):
        if index % checkpoint == 0:
            print(f"Added {index} samples")

        trainer.add(sample)

    # train mitie model
    # This function does the work of training.  Note that it can take a long time to run
    # when using larger training datasets.  So be patient.
    ner = trainer.train()

    # # Now that training is done we can save the ner object to disk like so.  This will
    # # allow you to load the model back in using a statement like:
    # #   ner = named_entity_extractor("new_ner_model.dat").
    # save mitie model
    ner.save_to_disk("new_ner_model.dat")

    # evaluate mitie model


if __name__ == "__main__":
    train_mitie_ner_model()

# sample = ner_training_instance(
#     [
#         "Mam",
#         "na",
#         "imię",
#         "Adam",
#         "Kowalski",
#         "i",
#         "jadę",
#         "do",
#         "warszawy",
#         "na",
#         "Politechnikę",
#         "Wrocławską",
#         ".",
#     ]
# )
# # Now that we have the tokens stored, we add the entity annotations.  The first
# # annotation indicates that the tokens in the range(3,5) is a person.  I.e.
# # "Davis King" is a person name.  Note that you can use any strings as the
# # labels.  Here we use "person" and "org" but you could use any labels you
# # like.
# sample.add_entity(xrange(3, 5), "person")
# sample.add_entity(xrange(10, 12), "org")

# # And we add another training example
# sample2 = ner_training_instance(
#     [
#         "Któregoś",
#         "innego",
#         "dnia",
#         "w",
#         "pracy",
#         "zobaczyłem",
#         "Weronikę",
#         "Dracewicz",
#         "która",
#         "też",
#         "pracuje",
#         "na",
#         "Politechnice",
#         "Warszawskiej",
#         ".",
#     ]
# )
# sample2.add_entity(xrange(6, 8), "person")
# sample2.add_entity(xrange(12, 14), "org")


# # Now that we have some annotated example sentences we can create the object that does
# # the actual training, the ner_trainer.  The constructor for this object takes a string
# # that should contain the file name for a saved mitie::total_word_feature_extractor.
# # The total_word_feature_extractor is MITIE's primary method for analyzing words and
# # is created by the tool in the MITIE/tools/wordrep folder.  The wordrep tool analyzes
# # a large document corpus, learns important word statistics, and then outputs a
# # total_word_feature_extractor that is knowledgeable about a particular language (e.g.
# # English).  MITIE comes with a total_word_feature_extractor for English so that is
# # what we use here.  But if you need to make your own you do so using a command line
# # statement like:
# #    wordrep -e a_folder_containing_only_text_files
# # and wordrep will create a total_word_feature_extractor.dat based on the supplied
# # text files.  Note that wordrep can take a long time to run or require a lot of RAM
# # if a large text dataset is given.  So use a powerful machine and be patient.
# trainer = ner_trainer(
#     "../models/mitie/base/pl-mitie-lg/total_word_feature_extractor.dat"
# )
# # Don't forget to add the training data.  Here we have only two examples, but for real
# # uses you need to have thousands.
# trainer.add(sample)
# trainer.add(sample2)
# # The trainer can take advantage of a multi-core CPU.  So set the number of threads
# # equal to the number of processing cores for maximum training speed.
# trainer.num_threads = 8

# # This function does the work of training.  Note that it can take a long time to run
# # when using larger training datasets.  So be patient.
# ner = trainer.train()

# # Now that training is done we can save the ner object to disk like so.  This will
# # allow you to load the model back in using a statement like:
# #   ner = named_entity_extractor("new_ner_model.dat").
# ner.save_to_disk("new_ner_model.dat")

# # But now let's try out the ner object.  It was only trained on a small dataset but it
# # has still learned a little.  So let's give it a whirl.  But first, print a list of
# # possible tags.  In this case, it is just "person" and "org".
# print("tags:", ner.get_possible_ner_tags())


# # Now let's make up a test sentence and ask the ner object to find the entities.
# tokens = [
#     "Dziś",
#     "spotkałem",
#     "się",
#     "z",
#     "Jacek",
#     "Murawski",
#     "z",
#     "Uniwersytetu",
#     "Warszawskiego",
#     ".",
# ]
# entities = ner.extract_entities(tokens)
# # Happily, it found the correct answers, "John Becker" and "HBU" in this case which we
# # print out below.


# print("\nEntities found:", entities)
# print("\nNumber of entities detected:", len(entities))
# for e in entities:
#     range = e[0]
#     tag = e[1]
#     entity_text = " ".join(tokens[i] for i in range)
#     print("    " + tag + ": " + entity_text)
