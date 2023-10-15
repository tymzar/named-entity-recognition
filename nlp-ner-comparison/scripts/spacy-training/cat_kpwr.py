# coding=utf-8
# Copyright 2021 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""KPWR-NER tagging dataset."""

import csv
from typing import List, Tuple, Dict, Generator
from spacy_types import PreSpacyDataset

import datasets

_DESCRIPTION = """KPWR-NER tagging dataset."""

_URLS = {
    "train": "https://huggingface.co/datasets/clarin-pl/kpwr-ner/resolve/main/data/kpwr-ner-n82-train-tune.iob",
    "test": "https://huggingface.co/datasets/clarin-pl/kpwr-ner/resolve/main/data/kpwr-ner-n82-test.iob",
}

_HOMEPAGE = "https://clarin-pl.eu/dspace/handle/11321/294"

_NER_TAGS = [
    "B-nam_adj",
    "B-nam_adj_city",
    "B-nam_adj_country",
    "B-nam_adj_person",
    "B-nam_eve",
    "B-nam_eve_human",
    "B-nam_eve_human_cultural",
    "B-nam_eve_human_holiday",
    "B-nam_eve_human_sport",
    "B-nam_fac_bridge",
    "B-nam_fac_goe",
    "B-nam_fac_goe_stop",
    "B-nam_fac_park",
    "B-nam_fac_road",
    "B-nam_fac_square",
    "B-nam_fac_system",
    "B-nam_liv_animal",
    "B-nam_liv_character",
    "B-nam_liv_god",
    "B-nam_liv_habitant",
    "B-nam_liv_person",
    "B-nam_loc",
    "B-nam_loc_astronomical",
    "B-nam_loc_country_region",
    "B-nam_loc_gpe_admin1",
    "B-nam_loc_gpe_admin2",
    "B-nam_loc_gpe_admin3",
    "B-nam_loc_gpe_city",
    "B-nam_loc_gpe_conurbation",
    "B-nam_loc_gpe_country",
    "B-nam_loc_gpe_district",
    "B-nam_loc_gpe_subdivision",
    "B-nam_loc_historical_region",
    "B-nam_loc_hydronym",
    "B-nam_loc_hydronym_lake",
    "B-nam_loc_hydronym_ocean",
    "B-nam_loc_hydronym_river",
    "B-nam_loc_hydronym_sea",
    "B-nam_loc_land",
    "B-nam_loc_land_continent",
    "B-nam_loc_land_island",
    "B-nam_loc_land_mountain",
    "B-nam_loc_land_peak",
    "B-nam_loc_land_region",
    "B-nam_num_house",
    "B-nam_num_phone",
    "B-nam_org_company",
    "B-nam_org_group",
    "B-nam_org_group_band",
    "B-nam_org_group_team",
    "B-nam_org_institution",
    "B-nam_org_nation",
    "B-nam_org_organization",
    "B-nam_org_organization_sub",
    "B-nam_org_political_party",
    "B-nam_oth",
    "B-nam_oth_currency",
    "B-nam_oth_data_format",
    "B-nam_oth_license",
    "B-nam_oth_position",
    "B-nam_oth_tech",
    "B-nam_oth_www",
    "B-nam_pro",
    "B-nam_pro_award",
    "B-nam_pro_brand",
    "B-nam_pro_media",
    "B-nam_pro_media_periodic",
    "B-nam_pro_media_radio",
    "B-nam_pro_media_tv",
    "B-nam_pro_media_web",
    "B-nam_pro_model_car",
    "B-nam_pro_software",
    "B-nam_pro_software_game",
    "B-nam_pro_title",
    "B-nam_pro_title_album",
    "B-nam_pro_title_article",
    "B-nam_pro_title_book",
    "B-nam_pro_title_document",
    "B-nam_pro_title_song",
    "B-nam_pro_title_treaty",
    "B-nam_pro_title_tv",
    "B-nam_pro_vehicle",
    "I-nam_adj_country",
    "I-nam_eve",
    "I-nam_eve_human",
    "I-nam_eve_human_cultural",
    "I-nam_eve_human_holiday",
    "I-nam_eve_human_sport",
    "I-nam_fac_bridge",
    "I-nam_fac_goe",
    "I-nam_fac_goe_stop",
    "I-nam_fac_park",
    "I-nam_fac_road",
    "I-nam_fac_square",
    "I-nam_fac_system",
    "I-nam_liv_animal",
    "I-nam_liv_character",
    "I-nam_liv_god",
    "I-nam_liv_person",
    "I-nam_loc",
    "I-nam_loc_astronomical",
    "I-nam_loc_country_region",
    "I-nam_loc_gpe_admin1",
    "I-nam_loc_gpe_admin2",
    "I-nam_loc_gpe_admin3",
    "I-nam_loc_gpe_city",
    "I-nam_loc_gpe_conurbation",
    "I-nam_loc_gpe_country",
    "I-nam_loc_gpe_district",
    "I-nam_loc_gpe_subdivision",
    "I-nam_loc_historical_region",
    "I-nam_loc_hydronym",
    "I-nam_loc_hydronym_lake",
    "I-nam_loc_hydronym_ocean",
    "I-nam_loc_hydronym_river",
    "I-nam_loc_hydronym_sea",
    "I-nam_loc_land",
    "I-nam_loc_land_continent",
    "I-nam_loc_land_island",
    "I-nam_loc_land_mountain",
    "I-nam_loc_land_peak",
    "I-nam_loc_land_region",
    "I-nam_num_house",
    "I-nam_num_phone",
    "I-nam_org_company",
    "I-nam_org_group",
    "I-nam_org_group_band",
    "I-nam_org_group_team",
    "I-nam_org_institution",
    "I-nam_org_nation",
    "I-nam_org_organization",
    "I-nam_org_organization_sub",
    "I-nam_org_political_party",
    "I-nam_oth",
    "I-nam_oth_currency",
    "I-nam_oth_data_format",
    "I-nam_oth_license",
    "I-nam_oth_position",
    "I-nam_oth_tech",
    "I-nam_oth_www",
    "I-nam_pro",
    "I-nam_pro_award",
    "I-nam_pro_brand",
    "I-nam_pro_media",
    "I-nam_pro_media_periodic",
    "I-nam_pro_media_radio",
    "I-nam_pro_media_tv",
    "I-nam_pro_media_web",
    "I-nam_pro_model_car",
    "I-nam_pro_software",
    "I-nam_pro_software_game",
    "I-nam_pro_title",
    "I-nam_pro_title_album",
    "I-nam_pro_title_article",
    "I-nam_pro_title_book",
    "I-nam_pro_title_document",
    "I-nam_pro_title_song",
    "I-nam_pro_title_treaty",
    "I-nam_pro_title_tv",
    "I-nam_pro_vehicle",
    "O",
]


class KPWRNER(datasets.GeneratorBasedBuilder):
    def _info(self) -> datasets.DatasetInfo:
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "lemmas": datasets.Sequence(datasets.Value("string")),
                    "orth": datasets.Sequence(datasets.Value("string")),
                    "ner": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=_NER_TAGS, num_classes=len(_NER_TAGS)
                        )
                    ),
                }
            ),
            homepage=_HOMEPAGE,
        )

    def _split_generators(
        self, dl_manager: datasets.DownloadManager
    ) -> List[datasets.SplitGenerator]:
        urls_to_download = _URLS
        downloaded_files = dl_manager.download_and_extract(urls_to_download)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": downloaded_files["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": downloaded_files["test"]},
            ),
        ]

    def _generate_examples(
        self, filepath: str
    ) -> Generator[Tuple[int, Dict[str, str]], None, None]:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)

            tokens = []
            lemma = []
            orth = []
            ner = []
            gid = 0

            for line in reader:
                if not line:
                    yield gid, {
                        "tokens": tokens,
                        "lemmas": lemma,
                        "orth": orth,
                        "ner": ner,
                    }
                    gid += 1
                    tokens = []
                    lemma = []
                    orth = []
                    ner = []

                elif len(line) == 1:  # ignore DOCS
                    continue

                else:
                    tokens.append(line[0])
                    lemma.append(line[1])
                    orth.append(line[2])
                    ner.append(line[3])
