#!/bin/bash

main() {
    echo "Downloading resources for NKJP"

    echo "Downloading NKJP"
    mkdir -p ../../data/nkjp/resources/UD_Polish-PDB/
    curl https://raw.githubusercontent.com/UniversalDependencies/UD_Polish-PDB/master/pl_pdb-ud-train.conllu --output ../../data/nkjp/resources/UD_Polish-PDB/pl_pdb-ud-train.conllu
    curl https://raw.githubusercontent.com/UniversalDependencies/UD_Polish-PDB/master/pl_pdb-ud-dev.conllu --output ../../data/nkjp/resources/UD_Polish-PDB/pl_pdb-ud-dev.conllu
    curl https://raw.githubusercontent.com/UniversalDependencies/UD_Polish-PDB/master/pl_pdb-ud-test.conllu --output ../../data/nkjp/resources/UD_Polish-PDB/pl_pdb-ud-test.conllu

    echo "Downloading NKJP 1M"
    mkdir -p ../../data/nkjp/resources/NKJP
    curl 'http://clip.ipipan.waw.pl/NationalCorpusOfPolish?action=AttachFile&do=get&target=NKJP-PodkorpusMilionowy-1.2.tar.gz' --output ../../data/nkjp/resources/NKJP/nkjp.tgz
    tar -xvf ../../data/nkjp/resources/NKJP/nkjp.tgz -C ../../data/nkjp/resources/NKJP/
    rm ../../data/nkjp/resources/NKJP/nkjp.tgz

    echo "Downloading NKJP 1M UD"
    mkdir -p ../../data/nkjp/resources/NKJP_UD
    curl 'http://git.nlp.ipipan.waw.pl/alina/PDBUD/repository/archive.zip?ref=master' --output ../../data/nkjp/resources/NKJP_UD/nkjp_ud.zip
    unzip ../../data/nkjp/resources/NKJP_UD/nkjp_ud.zip -d ../../data/nkjp/resources/NKJP_UD/
    mv ../../data/nkjp/resources/NKJP_UD/PDBUD-master-*/NKJP1M-UD/NKJP1M-UD.conllu ../../data/nkjp/resources/NKJP_UD/

    echo "Finished downloading resources for NKJP"
}

main
