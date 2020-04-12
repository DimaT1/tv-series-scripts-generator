#!/usr/bin/env bash

mds="./corpus_preprocessing/corpus_description.md
./corpus_preprocessing/preprocessing.md
./text_generation/text_generation.md"

mkdir -p .build
echo '' > ./.build/full.md

while IFS= read -r line; do
    cat "$line" >> ./.build/full.md
    printf "\n" >> ./.build/full.md
done <<< "$mds"

echo '# References' >> ./.build/full.md

pandoc -s --metadata-file=./docs/header.yaml --filter pandoc-citeproc ./.build/full.md -o ./docs/documentation.pdf
