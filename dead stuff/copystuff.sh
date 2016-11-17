#!/bin/bash

names=$( cat /Users/joseivelarde/Documents/MIT/NLP_UROP/GoldStandard3.txt )
# txtname=$( cat /Users/joseivelarde/Documents/MIT/NLP_UROP/GoldStandard2.txt )

for name in $names
do
	pdftotext /Users/joseivelarde/Documents/MIT/NLP_UROP/PDFs/"$name" /Users/joseivelarde/Documents/MIT/NLP_UROP/pdftotext/"${name:0:${#name} - 4}"
	
done