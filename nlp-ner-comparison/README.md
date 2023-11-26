# Comparing available NER tools for Polish

## Introduction

## TODO

- https://spacy.io/usage/training#api
- stanford train
- spacy training script `python3.10 -m spacy train config.cfg  --output ./models/spacy/test/out --paths.train ./models/spacy/test/train.spacy --paths.dev ./models/spacy/test/dev.spacy`
- spacy script to test model `spacy evaluate ./models/spacy/test/out/best-model ./models/spacy/test/test.spacy `
- model testing
    <!-- - shuffle danych -->
    <!-- - flaga na B-, I- -->
  <!-- - Wazenie względem ilości w kategorii -->

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

```bash
Starting dataset write process for tool:  bert  -  Process-1
Starting dataset write process for tool:  bert  -  Process-2
Starting dataset write process for tool:  bert  -  Process-3
Joining and waiting for a process for tool:  bert  -  Process-3
Dataset  val dataset length:  58905 file size:  17.548523902893066 MB
Finished in 1271.84 second(s)
Joining and waiting for a process for tool:  bert  -  Process-2
Dataset  test dataset length:  62590 file size:  18.51771354675293 MB
Finished in 1337.51 second(s)
Joining and waiting for a process for tool:  bert  -  Process-1
Dataset  train dataset length:  501143 file size:  149.32019519805908 MB
Finished in 10702.96 second(s)
Full process for tool: bert finished in 10902.54 second(s)
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

## Train

O: 749888
PERSON: 0
ORGNAME: 0
LOCATION: 0
TIME: 0
EVENT: 0
MONEY: 0
B-ORGNAME: 4884
I-ORGNAME: 10126
B-PERSON: 14359
I-PERSON: 31752
B-MONEY: 99
B-LOCATION: 21647
B-O: 6942
I-O: 14775
I-LOCATION: 28489
B-EVENT: 625
I-EVENT: 1135
B-LINK: 8
B-TIME: 4735
I-TIME: 484
O: 802880
PERSON: 0
ORGNAME: 0
LOCATION: 0
TIME: 0
EVENT: 0
MONEY: 0
B-ORGNAME: 5452
I-ORGNAME: 10807
B-MONEY: 137
B-O: 7421
I-O: 15578
B-LOCATION: 25109
I-LOCATION: 28629
B-PERSON: 13867
I-PERSON: 31142
B-EVENT: 668
I-EVENT: 1246
I-MONEY: 6
B-LINK: 26
B-PHONE: 3
I-PHONE: 8
I-LINK: 3
B-TIME: 4950
I-TIME: 431
Dataset val dataset length: 58905 file size: 17.518997192382812 MB
Finished in 114.66 second(s)
Joining and waiting for a process for tool: spacy - Process-2
Dataset test dataset length: 62590 file size: 18.11066436767578 MB
Finished in 119.9 second(s)
Joining and waiting for a process for tool: spacy - Process-1
O: 6182384
PERSON: 0
ORGNAME: 0
LOCATION: 0
TIME: 0
EVENT: 0
MONEY: 0
B-O: 59963
I-O: 120083
B-ORGNAME: 59787
I-ORGNAME: 105979
B-PERSON: 98994
I-PERSON: 235284
B-LOCATION: 180732
I-LOCATION: 229313
B-MONEY: 673
I-MONEY: 10
B-LINK: 52
B-EVENT: 5891
I-EVENT: 10510
I-LINK: 16
B-PHONE: 20
I-PHONE: 25
B-TIME: 34428
I-TIME: 3113
Dataset train dataset length: 501143 file size: 144.1572666168213 MB
Finished in 867.24 second(s)
Full process for tool: spacy finished in 1049.88 second(s)
Starting dataset write process for tool: stanford - Process-4
Starting dataset write process for tool: stanford - Process-5
Starting dataset write process for tool: stanford - Process-6
Joining and waiting for a process for tool: stanford - Process-6
Joining and waiting for a process for tool: stanford - Process-5
Joining and waiting for a process for tool: stanford - Process-4
Full process for tool: stanford finished in 1070.55 second(s)

### MITIE results

# dataset -> total_word_feature_extractor.dat

1. 50MB -> 335MB
   number of raw ASCII files found: 1
   num words: 200000
   saving word counts to top_word_counts.dat
   number of raw ASCII files found: 1
   Sample 50000000 random context vectors
   Now do CCA (left size: 8582326, right size: 8582326).
   correlations: 0.783697 0.495714 0.428661 0.417896 0.399711 0.308799 0.257686 0.241372 0.214332 0.206914 0.180628 0.151268 0.143147 0.135543 0.129035 0.11404 0.104493 0.094976 0.0889702 0.081165 0.0765073 0.0743562 0.0730994 0.0653017 0.0622959 0.0602029 0.0504991 0.0483258 0.0475654 0.0458159 0.0405218 0.0396676 0.0377837 0.035018 0.0321907 0.0302941 0.0294151 0.0272736 0.0250081 0.023913 0.0227566 0.0216142 0.0207634 0.0199015 0.0191722 0.0172601 0.0167749 0.0165069 0.0156701 0.0152914 0.0150729 0.0147807 0.0135261 0.013273 0.0125623 0.0120217 0.0117249 0.0115241 0.010776 0.0105152 0.0102252 0.00982769 0.00967478 0.00906732 0.00888962 0.00882777 0.00853846 0.00810019 0.00803891 0.00766455 0.0073715 0.00711813 0.00686214 0.0067737 0.00648305 0.00637957 0.00621849 0.00609243 0.00578847 0.00560462 0.00551808 0.00540755 0.00527975 0.0051427 0.00495427 0.0048308 0.00470006 0.00460154 0.00457549 0.00444141
   CCA done, now build up average word vectors
   num words: 200000
   num word vectors loaded: 200000
   got word vectors, now learn how they correlate with morphological features.
   building morphological vectors
   L.size(): 200000
   R.size(): 200000
   Now running CCA on word <-> morphology...
   correlations: 0.972561 0.671965 0.612678 0.579442 0.505745 0.410469 0.370399 0.320987 0.303507 0.295264 0.284905 0.272496 0.260294 0.252493 0.247422 0.243564 0.224549 0.215319 0.211788 0.202069 0.198979 0.193592 0.187116 0.179735 0.177608 0.173987 0.167869 0.165495 0.159846 0.157329 0.152932 0.148687 0.146318 0.144891 0.1425 0.140035 0.138354 0.137298 0.13551 0.133037 0.131869 0.129603 0.129255 0.126594 0.125905 0.123318 0.119747 0.116908 0.116507 0.115395 0.114808 0.111849 0.111262 0.108799 0.108121 0.106949 0.105413 0.103576 0.103322 0.102464 0.101616 0.100574 0.100245 0.0993405 0.0986815 0.0981801 0.0973369 0.0969129 0.0962343 0.0956761 0.0950916 0.0949497 0.0937699 0.0930668 0.092798 0.0924761 0.0915229 0.0906338 0.0902752 0.0897365 0.0893135 0.0891064 0.0884818 0.0879273 0.0873452 0.0871056 0.0864901 0.0862346 0.0858451 0.0855675

morphological feature dimensionality: 90
total word feature dimensionality: 271 2. 100MB -> 337MB
number of raw ASCII files found: 2
num words: 200000
saving word counts to top_word_counts.dat
number of raw ASCII files found: 2
Sample 50000000 random context vectors
Now do CCA (left size: 17204027, right size: 17204027).
correlations: 0.779923 0.512237 0.436919 0.423704 0.412156 0.32337 0.260955 0.245038 0.222629 0.220487 0.186529 0.155599 0.145268 0.140225 0.1293 0.11533 0.10416 0.0969533 0.0920494 0.0812887 0.0788473 0.0760371 0.0711883 0.0664675 0.0616015 0.0582108 0.0499312 0.0481921 0.0471149 0.0457483 0.0405427 0.0391695 0.0366974 0.0343238 0.0317766 0.0301706 0.0284668 0.02708 0.024634 0.0230824 0.0221957 0.0211691 0.0201103 0.0192433 0.0177503 0.0170046 0.0165348 0.0160024 0.0154991 0.014842 0.0144806 0.0140849 0.0132977 0.0126606 0.012073 0.0118559 0.0112087 0.0108456 0.0105672 0.0102032 0.0100555 0.0096982 0.00935652 0.00908955 0.00844935 0.00818099 0.00796244 0.00762995 0.00753236 0.0072838 0.00706413 0.00690194 0.00681546 0.00654413 0.00626689 0.00608943 0.00596117 0.00557491 0.00536563 0.0051692 0.00503521 0.00487138 0.00479157 0.00464975 0.0042314 0.00396397 0.00389778 0.00373412 0.0036037 0.00347846
CCA done, now build up average word vectors
num words: 200000
num word vectors loaded: 200000
got word vectors, now learn how they correlate with morphological features.
building morphological vectors
L.size(): 200000
R.size(): 200000
Now running CCA on word <-> morphology...
correlations: 0.978974 0.713797 0.657182 0.632944 0.558261 0.47269 0.425248 0.372064 0.351736 0.339963 0.320005 0.311463 0.30237 0.294466 0.289986 0.280466 0.265051 0.25838 0.247886 0.235087 0.232196 0.225109 0.224001 0.212538 0.204304 0.202062 0.191768 0.184285 0.182187 0.181151 0.174696 0.169313 0.167562 0.16549 0.160309 0.157552 0.154192 0.152316 0.150774 0.146907 0.144155 0.142709 0.141969 0.138627 0.137163 0.134016 0.132602 0.129624 0.12818 0.126129 0.125144 0.12363 0.122081 0.120231 0.118327 0.116443 0.115346 0.114512 0.113029 0.112386 0.111879 0.111077 0.110131 0.108435 0.107854 0.107057 0.106172 0.105093 0.104389 0.103112 0.102088 0.101712 0.100469 0.0994505 0.0989811 0.0984102 0.0982125 0.0972503 0.096731 0.0956087 0.0950048 0.094337 0.0939208 0.0925872 0.0919503 0.0914311 0.0909645 0.0905782 0.0905216 0.0894758

morphological feature dimensionality: 90
total word feature dimensionality: 271 3. 150MB -> failed
number of raw ASCII files found: 3
num words: 200000
saving word counts to top_word_counts.dat
number of raw ASCII files found: 3
Sample 50000000 random context vectors
Now do CCA (left size: 25828623, right size: 25828623).

- thread #1, queue = 'com.apple.main-thread', stop reason = EXC_BAD_ACCESS (code=2, address=0x6f1a629238)
  frame #0: 0x0000000192905900 libLAPACK.dylib`SLARFT + 400
libLAPACK.dylib`SLARFT:
  -> 0x192905900 <+400>: ldr s0, [x27, x23, lsl #2]
  0x192905904 <+404>: fcmp s0, #0.0
  0x192905908 <+408>: b.ne 0x192905974 ; <+516>
  0x19290590c <+412>: sub x23, x23, #0x1

4. 200MB -> failed
   number of raw ASCII files found: 4
   num words: 200000
   saving word counts to top_word_counts.dat
   number of raw ASCII files found: 4
   Sample 50000000 random context vectors
   Now do CCA (left size: 34482189, right size: 34482189).
   Process 49420 stopped

- thread #1, queue = 'com.apple.main-thread', stop reason = EXC_BAD_ACCESS (code=2, address=0x6f1d74b3b0)
  frame #0: 0x0000000192905900 libLAPACK.dylib`SLARFT + 400
libLAPACK.dylib`SLARFT:
  -> 0x192905900 <+400>: ldr s0, [x27, x23, lsl #2]
  0x192905904 <+404>: fcmp s0, #0.0
  0x192905908 <+408>: b.ne 0x192905974 ; <+516>
  0x19290590c <+412>: sub x23, x23, #0x1
  Target 0: (wordrep) stopped.
