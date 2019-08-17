#!/usr/bin/env bash

module load bwa/0.7.10
module load samtools/1.9

REF=$1
F_READ=$2
R_READ=$3
OUT_ALIGN=$4
BIN=$5
SORTED=$6


echo "bwa index $REF"
bwa index $REF 
echo "bwa mem -t 20 $REF  $F_READ $R_READ > $OUT_ALIGN"
bwa mem -t 20 $REF  $F_READ $R_READ > $OUT_ALIGN
echo "samtools view -Sb -@ 20 -q 30 $OUT_ALIGN > $BIN"
samtools view -Sb -@ 20 -q 30 $OUT_ALIGN > $BIN
echo "samtools sort -@ 10 -o $SORTED $BIN"
samtools sort -@ 10 -o $SORTED $BIN

