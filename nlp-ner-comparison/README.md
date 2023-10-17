# Comparing available NER tools for Polish

## Introduction

## NER Tools

### Python

1. [spaCy](https://spacy.io/) - industrial-strength NLP library (Python)
2. [NLTK](https://www.nltk.org/) - Natural Language Toolkit (Python)
3. [flair](https://github.com/flairNLP/flair) - a very simple framework for state-of-the-art NLP (Python) [Polish](https://github.com/flairNLP/flair/issues/187)
4. [StanfordNLP](https://stanfordnlp.github.io/stanfordnlp/) - a Python NLP Library for Many Human Languages (Python)

### Go

1. [ner](https://github.com/sbl/ner) - Named Entity Recognition in Go (Go)

## Datasets

The Polish Sejm Corpus: http://clip.ipipan.waw.pl/PSC
BSNLP 2017 (Croatian, Czech, Polish, Russian, Slovak, Slovene, Ukrainian): http://bsnlp-2017.cs.helsinki.fi/shared_task_results.html
Polish Coreference Corpus: http://zil.ipipan.waw.pl/PolishCoreferenceCorpus
WikiNER: https://figshare.com/articles/Learning_multilingual_named_entity_recognition_from_Wikipedia/5462500
Corpus of Economic News (CEN Corpus): http://www.nlp.pwr.wroc.pl/narzedzia-i-zasoby/zasoby/cen
KPWr (Korpus Języka Polskiego Politechniki Wrocławskiej/Polish Corpus of Wrocław University of Technology): http://plwordnet.pwr.wroc.pl/index.php?option=com_content&view=article&id=35&Itemid=181&lang=pl ; http://plwordnet.pwr.wroc.pl/attachments/article/35/kpwr-1.1.7z (Broda et al., KPWr: Towards a Free Corpus of Polish, 2012)
NKJP: http://clip.ipipan.waw.pl/NationalCorpusOfPolish?action=AttachFile&do=view&target=NKJP-PodkorpusMilionowy-1.2.tar.gz

### Ready dataset sizes

### Combined dataset cen + kpwr + multinerd + wikineural

Multithreaded data preparation:

```bash
Dataset  val dataset length:  33885 file size:  9.536857604980469 MB
Finished in 272.01 second(s)
Dataset  test dataset length:  38365 file size:  10.319704055786133 MB
Finished in 290.83 second(s)
Dataset  train dataset length:  283836 file size:  74.80930137634277 MB
Finished in 766.54 second(s)
Full process finished in 772.62 second(s)
```

Multi-processed data preparation:

```bash
Dataset  val dataset length:  33885 file size:  9.536857604980469 MB
Finished in 74.79 second(s)
Dataset  test dataset length:  38365 file size:  10.319704055786133 MB
Finished in 82.03 second(s)
Dataset  train dataset length:  283836 file size:  74.80930137634277 MB
Finished in 585.65 second(s)
Full process finished in 599.26 second(s)
```

### Combined dataset cen + kpwr + multinerd + wikineural + wiki-ner

```bash
Dataset  train dataset length: file size:  125.3847534634277 MB
Dataset  test dataset length: file size:  13.3194055786133 MB
Dataset  val dataset length: file size:  12.9368604980469 MB
```

### All datasets

```bash
Dataset  val dataset length:  54139 file size:  17.501068115234375 MB
Finished in 120.14 second(s)
Dataset  test dataset length:  58617 file size:  18.099997520446777 MB
Finished in 125.31 second(s)
Dataset  train dataset length:  445858 file size:  144.18569087982178 MB
Finished in 914.38 second(s)
Full process finished in 1024.26 second(s)
```

### Data

1. [bsnlp-2019](http://bsnlp.cs.helsinki.fi/bsnlp-2019/shared_task.html)
2. [wiki-ner](https://github.com/dice-group/FOX/tree/master/input/Wikiner)
3. [wikineural](https://github.com/Babelscape/wikineural/tree/master/data/wikineural/pl)
4. [MultiNERD](https://github.com/Babelscape/multinerd)
5. [cen](http://www.nlp.pwr.wroc.pl/narzedzia-i-zasoby/zasoby/cen)
6. [nkjp]

## Useful links

1. [Named Entity Recognition (NER) with spaCy](https://towardsdatascience.com/named-entity-recognition-ner-with-spacy-8d1bb7108ebf)
2. [Go NLP resources](https://github.com/sdadas/polish-nlp-resources)
3. [Resources](https://github.com/juand-r/entity-recognition-datasets)
4. [Spacy usage](https://towardsdatascience.com/train-ner-with-custom-training-data-using-spacy-525ce748fab7)

## NER categories

1. Person - PERSON
2. Money - MONEY
3. Location/Addres - LOCATION
4. Email address
5. Phone number
6. PESEL
7. Orgazaizations - ORGNAME
   Event - EVENT
8. Time - TIME
9. Link
   10 IP (optional)
10. Token-like strings (optional)
11. Airports (optional)

### NKJP

Categories - {'GEOGNAME', 'TIME', 'ORGNAME', 'PERSNAME', 'DATE', 'PLACENAME'}

GEOGNAME -> LOCATION
TIME -> TIME
ORGNAME -> ORGNAME
PERSNAME -> PERSON
DATE -> TIME
PLACENAME -> LOCATION

### CEN

nam_adj - adjectives
nam_adj_city -> LOCATION
nam_adj_country -> LOCATION
nam_adj_person -> O
nam_eve_human -> O
nam_eve_human_cultural -> EVENT
nam_eve_human_holiday -> EVENT
nam_eve_human_sport -> EVENT
nam_fac_goe -> LOCATION
nam_fac_road -> LOCATION
nam_fac_square -> O
nam_fac_system -> O
nam_liv_god -> O
nam_liv_habitant -> PERSON
nam_liv_person -> PERSON
nam_loc -> LOCATION
nam_loc_astronomical -> LOCATION
nam_loc_country_region -> LOCATION
nam_loc_gpe_admin1 -> LOCATION
nam_loc_gpe_admin2 -> LOCATION
nam_loc_gpe_admin3 -> LOCATION
nam_loc_gpe_city -> LOCATION
nam_loc_gpe_conurbation -> LOCATION
nam_loc_gpe_country -> LOCATION
nam_loc_gpe_district -> LOCATION
nam_loc_gpe_subdivision -> LOCATION
nam_loc_historical_region -> LOCATION
nam_loc_hydronym -> LOCATION
nam_loc_hydronym_ocean -> LOCATION
nam_loc_hydronym_river -> LOCATION
nam_loc_hydronym_sea -> LOCATION
nam_loc_land -> LOCATION
nam_loc_land_continent -> LOCATION
nam_loc_land_island -> LOCATION
nam_loc_land_mountain -> LOCATION
nam_loc_land_region -> LOCATION
nam_num_house -> O
nam_num_phone -> PHONE
nam_org_company -> ORGNAME
nam_org_group -> O
nam_org_group_band -> ORGNAME
nam_org_institution -> ORGNAME
nam_org_nation -> To be decided
nam_org_organization -> ORGNAME
nam_org_organization_sub -> O
nam_org_political_party -> ORGNAME
nam_oth -> O
nam_oth_currency -> MONEY
nam_oth_data_format -> O # tech to decide
nam_oth_license -> O
nam_oth_position -> PERSON
nam_oth_tech -> O
nam_oth_www -> LINK
nam_pro -> O # tech
nam_pro_award -> EVENT
nam_pro_brand -> ORGNAME
nam_pro_media -> ORGNAME
nam_pro_media_periodic -> ORGNAME
nam_pro_media_radio -> ORGNAME
nam_pro_media_tv -> ORGNAME
nam_pro_media_web -> ORGNAME
nam_pro_model_car -> O
nam_pro_software -> O
nam_pro_software_game
nam_pro_title -> O
nam_pro_title_album -> O
nam_pro_title_article -> O
nam_pro_title_book -> O
nam_pro_title_document -> O
nam_pro_title_song -> O
nam_pro_title_treaty -> O
nam_pro_title_tv -> O
nam_pro_vehicle -> O

### KPWR

nam_adj - adjectives
nam_adj_city -> LOCATION
nam_adj_country -> LOCATION
nam_adj_person -> O
nam_eve_human -> O
nam_eve_human_cultural -> EVENT
nam_eve_human_holiday -> EVENT
nam_eve_human_sport -> EVENT
nam_fac_goe -> LOCATION
nam_fac_road -> LOCATION
nam_fac_square -> O
nam_fac_system -> O
nam_liv_god -> O
nam_liv_habitant -> PERSON
nam_liv_person -> PERSON
nam_loc -> LOCATION
nam_loc_astronomical -> LOCATION
nam_loc_country_region -> LOCATION
nam_loc_gpe_admin1 -> LOCATION
nam_loc_gpe_admin2 -> LOCATION
nam_loc_gpe_admin3 -> LOCATION
nam_loc_gpe_city -> LOCATION
nam_loc_gpe_conurbation -> LOCATION
nam_loc_gpe_country -> LOCATION
nam_loc_gpe_district -> LOCATION
nam_loc_gpe_subdivision -> LOCATION
nam_loc_historical_region -> LOCATION
nam_loc_hydronym -> LOCATION
nam_loc_hydronym_ocean -> LOCATION
nam_loc_hydronym_river -> LOCATION
nam_loc_hydronym_sea -> LOCATION
nam_loc_land -> LOCATION
nam_loc_land_continent -> LOCATION
nam_loc_land_island -> LOCATION
nam_loc_land_mountain -> LOCATION
nam_loc_land_region -> LOCATION
nam_num_house -> O
nam_num_phone -> PHONE
nam_org_company -> ORGNAME
nam_org_group -> O
nam_org_group_band -> ORGNAME
nam_org_institution -> ORGNAME
nam_org_nation -> To be decided
nam_org_organization -> ORGNAME
nam_org_organization_sub -> O
nam_org_political_party -> ORGNAME
nam_oth -> O
nam_oth_currency -> MONEY
nam_oth_data_format -> O # tech to decide
nam_oth_license -> O
nam_oth_position -> PERSON
nam_oth_tech -> O
nam_oth_www -> LINK
nam_pro -> O # tech
nam_pro_award -> EVENT
nam_pro_brand -> ORGNAME
nam_pro_media -> ORGNAME
nam_pro_media_periodic -> ORGNAME
nam_pro_media_radio -> ORGNAME
nam_pro_media_tv -> ORGNAME
nam_pro_media_web -> ORGNAME
nam_pro_model_car -> O
nam_pro_software -> O
nam_pro_software_game -> O
nam_pro_title -> O
nam_pro_title_album -> O
nam_pro_title_article -> O
nam_pro_title_book -> O
nam_pro_title_document -> O
nam_pro_title_song -> O
nam_pro_title_treaty -> O
nam_pro_title_tv -> O
nam_pro_vehicle -> O

### MultiNERD

PER -> PERSON
LOC -> LOCATION
ORG -> ORGNAME
ANIM -> O
BIO -> O
CEL -> O
DIS -> O
EVE -> EVENT
FOOD -> O
INST -> O
MEDIA -> O
PLANT -> O
MYTH -> O
TIME -> TIME
VEHI -> O

### WikiNER

LOC -> LOCATION
ORG -> ORGNAME
PER -> PERSON
MISC -> O
NON -> O
DAB -> O

### Wikineural

ORG -> ORGNAME
MISC -> O
PER -> PERSON
LOC -> LOCATION
