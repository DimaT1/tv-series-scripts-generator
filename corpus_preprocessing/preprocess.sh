#!/usr/bin/env bash

mkdir -p raws

for file in ./*.html; do
    html2text <(iconv -t UTF-8//IGNORE "$file" | tr '\n' ' ') | sed 's/\*//g;s/_//g;s/(/[/g;s/)/]/g;s/</[/g;s/>/]/g;s/^RACH:/Rachel:/;s/^MNCA:/Monica:/;s/^PHOE:/Phoebe:/;s/^CHAN:/Chandler/' > "./raws/${file//html/raw}"
done
