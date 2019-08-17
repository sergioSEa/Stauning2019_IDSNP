module load bam-readcount/0.7.4

REF=$1
BAM=$2
OUT_COUNT=$3
UNIQUE=$4
OUTPUT_METRICS=$5
COUNT_by_N=$6
UNIQUE_META=$7

if [ ! -f $OUT_COUNT ]; then
bam-readcount -w 1 -b 30  -f $REF $BAM > $OUT_COUNT
fi



if [ ! -f $COUNT_by_N ]; then

cat $OUT_COUNT | sed 's/:/\t/g' | cut -f1-4,20,34,48,62 | awk '{if($3=="C")print $0"\t"$6; else if($3=="G")print $0"\t"$7;else if($3=="A")print $0"\t"$5;else if($3=="T")print $0"\t"$8}' > $COUNT_by_N
fi


if [ ! -f $UNIQUE_META ]; then
cat $UNIQUE | cut -f1,2,4 | fgrep -f- $COUNT_by_N > $UNIQUE_META
fi

echo "scripts/Compare_common_variants.py $UNIQUE $UNIQUE_META $OUTPUT_METRICS"
python scripts/Compare_common_variants.py $UNIQUE $UNIQUE_META $OUTPUT_METRICS
