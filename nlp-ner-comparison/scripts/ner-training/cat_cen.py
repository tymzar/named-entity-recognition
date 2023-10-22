# coding=utf-8
"""CEN dataset."""

import csv
import datasets

_DESCRIPTION = "CEN dataset."

_URLS = {
    "train": "https://huggingface.co/datasets/clarin-knext/cen/resolve/main/data/train.iob",
    "valid": "https://huggingface.co/datasets/clarin-knext/cen/resolve/main/data/valid.iob",
    "test": "https://huggingface.co/datasets/clarin-knext/cen/resolve/main/data/test.iob",
}

_HOMEPAGE = "https://clarin-pl.eu/dspace/handle/11321/6"

_N82_TAGS = [
    "nam_adj",
    "nam_adj_city",
    "nam_adj_country",
    "nam_adj_person",
    "nam_eve",
    "nam_eve_human",
    "nam_eve_human_cultural",
    "nam_eve_human_holiday",
    "nam_eve_human_sport",
    "nam_fac_bridge",
    "nam_fac_goe",
    "nam_fac_goe_stop",
    "nam_fac_park",
    "nam_fac_road",
    "nam_fac_square",
    "nam_fac_system",
    "nam_liv_animal",
    "nam_liv_character",
    "nam_liv_god",
    "nam_liv_habitant",
    "nam_liv_person",
    "nam_loc",
    "nam_loc_astronomical",
    "nam_loc_country_region",
    "nam_loc_gpe_admin1",
    "nam_loc_gpe_admin2",
    "nam_loc_gpe_admin3",
    "nam_loc_gpe_city",
    "nam_loc_gpe_conurbation",
    "nam_loc_gpe_country",
    "nam_loc_gpe_district",
    "nam_loc_gpe_subdivision",
    "nam_loc_historical_region",
    "nam_loc_hydronym",
    "nam_loc_hydronym_lake",
    "nam_loc_hydronym_ocean",
    "nam_loc_hydronym_river",
    "nam_loc_hydronym_sea",
    "nam_loc_land",
    "nam_loc_land_continent",
    "nam_loc_land_island",
    "nam_loc_land_mountain",
    "nam_loc_land_peak",
    "nam_loc_land_region",
    "nam_num_house",
    "nam_num_phone",
    "nam_org_company",
    "nam_org_group",
    "nam_org_group_band",
    "nam_org_group_team",
    "nam_org_institution",
    "nam_org_nation",
    "nam_org_organization",
    "nam_org_organization_sub",
    "nam_org_political_party",
    "nam_oth",
    "nam_oth_currency",
    "nam_oth_data_format",
    "nam_oth_license",
    "nam_oth_position",
    "nam_oth_tech",
    "nam_oth_www",
    "nam_pro",
    "nam_pro_award",
    "nam_pro_brand",
    "nam_pro_media",
    "nam_pro_media_periodic",
    "nam_pro_media_radio",
    "nam_pro_media_tv",
    "nam_pro_media_web",
    "nam_pro_model_car",
    "nam_pro_software",
    "nam_pro_software_game",
    "nam_pro_title",
    "nam_pro_title_album",
    "nam_pro_title_article",
    "nam_pro_title_book",
    "nam_pro_title_document",
    "nam_pro_title_song",
    "nam_pro_title_treaty",
    "nam_pro_title_tv",
    "nam_pro_vehicle",
]

_NER_IOB_TAGS = ["O"]

for tag in _N82_TAGS:
    _NER_IOB_TAGS.extend([f"B-{tag}", f"I-{tag}"])


class CenDataset(datasets.GeneratorBasedBuilder):
    def _info(self) -> datasets.DatasetInfo:
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "lemmas": datasets.Sequence(datasets.Value("string")),
                    "mstags": datasets.Sequence(datasets.Value("string")),
                    "ner": datasets.Sequence(
                        datasets.features.ClassLabel(names=_NER_IOB_TAGS)
                    ),
                }
            ),
            homepage=_HOMEPAGE,
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager):
        downloaded_files = dl_manager.download_and_extract(_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": downloaded_files["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": downloaded_files["valid"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": downloaded_files["test"]},
            ),
        ]

    def _generate_examples(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as fin:
            reader = csv.reader(fin, delimiter="\t", quoting=csv.QUOTE_NONE)

            tokens = []
            lemmas = []
            mstags = []
            ner = []
            gid = 0

            for line in reader:
                if not line:
                    yield gid, {
                        "tokens": tokens,
                        "lemmas": lemmas,
                        "mstags": mstags,
                        "ner": ner,
                    }
                    gid += 1
                    tokens = []
                    lemmas = []
                    mstags = []
                    ner = []

                elif len(line) == 1:  # ignore --DOCSTART lines
                    continue

                else:
                    tokens.append(line[0])
                    lemmas.append(line[1])
                    mstags.append(line[2])
                    ner.append(line[3])
