from transformers import BertForMaskedLM, BertTokenizer
import csv
import os
from itertools import compress
from NERDA.models import NERDA


def get_conll_data(path: str, limit: int = None, dir: str = None) -> dict:
    """Load CoNLL-2003 (English) data split.

    Loads a single data split from the
    [CoNLL-2003](https://www.clips.uantwerpen.be/conll2003/ner/)
    (English) data set.

    Args:
        split (str, optional): Choose which split to load. Choose
            from 'train', 'valid' and 'test'. Defaults to 'train'.
        limit (int, optional): Limit the number of observations to be
            returned from a given split. Defaults to None, which implies
            that the entire data split is returned.
        dir (str, optional): Directory where data is cached. If set to
            None, the function will try to look for files in '.conll' folder in home directory.

    Returns:
        dict: Dictionary with word-tokenized 'sentences' and named
        entity 'tags' in IOB format.

    Examples:
        Get test split
        >>> get_conll_data('test')

        Get first 5 observations from training split
        >>> get_conll_data('train', limit = 5)

    """

    file_path = path
    assert os.path.isfile(
        file_path
    ), f"File {file_path} does not exist. Try downloading CoNLL-2003 data with download_conll_data()"

    # read data from file.
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t", quoting=csv.QUOTE_NONE)
        for row in reader:
            data.append([row])

    sentences = []
    sentence = []
    entities = []
    tags = []

    for row in data:
        # extract first element of list.
        row = row[0]
        # TO DO: move to data reader.
        if len(row) > 0 and row[0] != "-DOCSTART-":
            sentence.append(row[0])
            tags.append(row[-1])
        if len(row) == 0 and len(sentence) > 0:
            # clean up sentence/tags.
            # remove white spaces.
            selector = [word != " " for word in sentence]
            sentence = list(compress(sentence, selector))
            tags = list(compress(tags, selector))
            # append if sentence length is still greater than zero..
            if len(sentence) > 0:
                sentences.append(sentence)
                entities.append(tags)
            sentence = []
            tags = []

    if limit is not None:  # changed [:limit]
        sentences = sentences[limit:]
        entities = entities[limit:]

    return {"sentences": sentences, "tags": entities}


def main():
    model = BertForMaskedLM.from_pretrained("dkleczek/bert-base-polish-cased-v1")
    tokenizer = BertTokenizer.from_pretrained("dkleczek/bert-base-polish-cased-v1")

    # from NERDA.datasets import get_conll_data, download_conll_data
    # download_conll_data()
    training = get_conll_data("../models/bert/prefix-partial/train.conll")
    validation = get_conll_data("../models/bert/prefix-partial/test.conll")

    print(training["sentences"][3])
    print(training["tags"][3])

    tag_scheme = [
        "B-LOCATION",
        "B-TIME",
        "B-ORGNAME",
        "B-MONEY",
        "B-PERSON",
        "B-TIME",
        "B-EVENT",
        "I-LOCATION",
        "I-TIME",
        "I-ORGNAME",
        "I-MONEY",
        "I-PERSON",
        "I-TIME",
        "I-EVENT",
    ]

    # tag_scheme = [
    #     "B-nam_adj",
    #     "B-nam_adj_city",
    #     "B-nam_adj_country",
    #     "B-nam_adj_person",
    #     "B-nam_eve",
    #     "B-nam_eve_human",
    #     "B-nam_eve_human_cultural",
    #     "B-nam_eve_human_holiday",
    #     "B-nam_eve_human_sport",
    #     "B-nam_fac_goe",
    #     "B-nam_fac_goe_stop",
    #     "B-nam_fac_park",
    #     "B-nam_fac_road",
    #     "B-nam_fac_square",
    #     "B-nam_fac_system",
    #     "B-nam_fac_bridge",
    #     "B-nam_liv_god",
    #     "B-nam_liv_habitant",
    #     "B-nam_liv_person",
    #     "B-nam_liv_character",
    #     "B-nam_loc",
    #     "B-nam_liv_animal",
    #     "B-nam_loc_astronomical",
    #     "B-nam_loc_country_region",
    #     "B-nam_loc_gpe_admin1",
    #     "B-nam_loc_gpe_admin2",
    #     "B-nam_loc_gpe_admin3",
    #     "B-nam_loc_gpe_city",
    #     "B-nam_loc_gpe_conurbation",
    #     "B-nam_loc_gpe_country",
    #     "B-nam_loc_gpe_district",
    #     "B-nam_loc_gpe_subdivision",
    #     "B-nam_loc_historical_region",
    #     "B-nam_loc_hydronym",
    #     "B-nam_loc_hydronym_ocean",
    #     "B-nam_loc_hydronym_river",
    #     "B-nam_loc_hydronym_sea",
    #     "B-nam_loc_hydronym_lake",
    #     "B-nam_loc_land_peak",
    #     "B-nam_loc_land",
    #     "B-nam_loc_land_continent",
    #     "B-nam_loc_land_island",
    #     "B-nam_loc_land_mountain",
    #     "B-nam_loc_land_region",
    #     "B-nam_num_house",
    #     "B-nam_num_phone",
    #     "B-nam_org_company",
    #     "B-nam_org_group",
    #     "B-nam_org_group_band",
    #     "B-nam_org_institution",
    #     "B-nam_org_nation",
    #     "B-nam_org_group_team",
    #     "B-nam_org_organization",
    #     "B-nam_org_organization_sub",
    #     "B-nam_org_political_party",
    #     "B-nam_oth",
    #     "B-nam_oth_currency",
    #     "B-nam_oth_data_format",
    #     "B-nam_oth_license",
    #     "B-nam_oth_position",
    #     "B-nam_oth_tech",
    #     "B-nam_oth_www",
    #     "B-nam_pro",
    #     "B-nam_pro_award",
    #     "B-nam_pro_brand",
    #     "B-nam_pro_media",
    #     "B-nam_pro_media_periodic",
    #     "B-nam_pro_media_radio",
    #     "B-nam_pro_media_tv",
    #     "B-nam_pro_media_web",
    #     "B-nam_pro_model_car",
    #     "B-nam_pro_software",
    #     "B-nam_pro_software_game",
    #     "B-nam_pro_title",
    #     "B-nam_pro_title_album",
    #     "B-nam_pro_title_article",
    #     "B-nam_pro_title_book",
    #     "B-nam_pro_title_document",
    #     "B-nam_pro_title_song",
    #     "B-nam_pro_title_treaty",
    #     "B-nam_pro_title_tv",
    #     "B-nam_pro_vehicle",
    #     "I-nam_adj",
    #     "I-nam_adj_city",
    #     "I-nam_adj_country",
    #     "I-nam_adj_person",
    #     "I-nam_eve",
    #     "I-nam_eve_human",
    #     "I-nam_eve_human_cultural",
    #     "I-nam_eve_human_holiday",
    #     "I-nam_eve_human_sport",
    #     "I-nam_fac_goe",
    #     "I-nam_fac_goe_stop",
    #     "I-nam_fac_park",
    #     "I-nam_fac_road",
    #     "I-nam_fac_square",
    #     "I-nam_fac_system",
    #     "I-nam_fac_bridge",
    #     "I-nam_liv_god",
    #     "I-nam_liv_habitant",
    #     "I-nam_liv_person",
    #     "I-nam_liv_character",
    #     "I-nam_loc",
    #     "I-nam_liv_animal",
    #     "I-nam_loc_astronomical",
    #     "I-nam_loc_country_region",
    #     "I-nam_loc_gpe_admin1",
    #     "I-nam_loc_gpe_admin2",
    #     "I-nam_loc_gpe_admin3",
    #     "I-nam_loc_gpe_city",
    #     "I-nam_loc_gpe_conurbation",
    #     "I-nam_loc_gpe_country",
    #     "I-nam_loc_gpe_district",
    #     "I-nam_loc_gpe_subdivision",
    #     "I-nam_loc_historical_region",
    #     "I-nam_loc_hydronym",
    #     "I-nam_loc_hydronym_ocean",
    #     "I-nam_loc_hydronym_river",
    #     "I-nam_loc_hydronym_sea",
    #     "I-nam_loc_hydronym_lake",
    #     "I-nam_loc_land_peak",
    #     "I-nam_loc_land",
    #     "I-nam_loc_land_continent",
    #     "I-nam_loc_land_island",
    #     "I-nam_loc_land_mountain",
    #     "I-nam_loc_land_region",
    #     "I-nam_num_house",
    #     "I-nam_num_phone",
    #     "I-nam_org_company",
    #     "I-nam_org_group",
    #     "I-nam_org_group_band",
    #     "I-nam_org_institution",
    #     "I-nam_org_nation",
    #     "I-nam_org_group_team",
    #     "I-nam_org_organization",
    #     "I-nam_org_organization_sub",
    #     "I-nam_org_political_party",
    #     "I-nam_oth",
    #     "I-nam_oth_currency",
    #     "I-nam_oth_data_format",
    #     "I-nam_oth_license",
    #     "I-nam_oth_position",
    #     "I-nam_oth_tech",
    #     "I-nam_oth_www",
    #     "I-nam_pro",
    #     "I-nam_pro_award",
    #     "I-nam_pro_brand",
    #     "I-nam_pro_media",
    #     "I-nam_pro_media_periodic",
    #     "I-nam_pro_media_radio",
    #     "I-nam_pro_media_tv",
    #     "I-nam_pro_media_web",
    #     "I-nam_pro_model_car",
    #     "I-nam_pro_software",
    #     "I-nam_pro_software_game",
    #     "I-nam_pro_title",
    #     "I-nam_pro_title_album",
    #     "I-nam_pro_title_article",
    #     "I-nam_pro_title_book",
    #     "I-nam_pro_title_document",
    #     "I-nam_pro_title_song",
    #     "I-nam_pro_title_treaty",
    #     "I-nam_pro_title_tv",
    #     "I-nam_pro_vehicle",
    # ]

    transformer = (
        "dkleczek/bert-base-polish-cased-v1"  # only bert small models/roberta OOM
    )

    # hyperparameters for network
    dropout = 0.1
    # hyperparameters for training
    training_hyperparameters = {
        "epochs": 5,
        "warmup_steps": 500,
        "train_batch_size": 64,
        "learning_rate": 0.0001,
    }

    model = NERDA(
        dataset_training=training,
        dataset_validation=validation,
        tag_scheme=tag_scheme,
        tag_outside="O",
        transformer=transformer,
        dropout=dropout,
        hyperparameters=training_hyperparameters,
    )

    model.train()

    # test = get_conll_data("valid")
    # model.evaluate_performance(test)

    # test = get_conll_data("test", 4000)
    # model.evaluate_performance(test)

    model.predict_text("Cristiano Ronaldo gra dla Juventusu FC")
    model.predict_text("Tatry są najwyższą górą w Polsce")

    model.save_network("test.bin")


if __name__ == "__main__":
    main()
