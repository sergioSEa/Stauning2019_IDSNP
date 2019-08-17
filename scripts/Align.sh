reference=$1
REFS=$2
output_parsnp=$3
VCF=$4

#module load parsnp/1.2 
echo "parsnp -r $reference -d $REFS -o $output_parsnp -p 20 -c"
parsnp -r $reference -d $REFS -o $output_parsnp -p 20 -c 

#module load  harvesttools/1.2 
harvesttools -i $output_parsnp/*.ggr -V $VCF
