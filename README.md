# Stauning2019_IDSNP
Pipeline used in Stauning et al in order to identify genetic variants unique to a bacterial isolate that are present in a metagenome.  

Software requeriments (versions used for the manuscrit):  
 * Python 3 or above  
 * parsnp and harvesttools v1.2  
 * ncbi-genome-download v0.2.8  
 * bwa v0.7.10  
 * samtools v1.9  
 * bam-readcount  

##Identifying unique SNPs in wound isolates  
In order to be able to recognize specific bacteria, a group of ID SNPs are defined from each isolate. ID SNPs are defined as unique SNPs in one isolate with respect other available NCBI genomes of the same species. All available complete genomes of the same species are downloaded using NCBI Genome Downloading Scripts [1]. Multiple alignment and variant calling of the genomes' core sequences are performed using Parsnp from the harvest suit [2]. Unique SNPs of the wound isolate are identified from the resulting variant calling file (vcf).  

##Identification of reads containing ID SNPs in metagenomes  

Fastq files for a metagenome is mapped to each isolates' reference genome using bwa-mem [3]. The resulting mapped reads are filtered by a minimal mapping quality of 30. Mapping files are subsequently sorted and the number of different nucleotides observed by position is then quantified using bam-readcount [4]. Positions present in both isolate's ID SNPs and the position's read-count are considered as covered. From the covered variants, the proportion of positions with at least one read matching an ID variant is recorded, together with the proportion of positions in which the majority of reads match ID SNPs.  

[1] [https://github.com/kblin/ncbi-genome-download]  
[2] Treangen,  Todd  J.,  et  al.  ”The  Harvest  suite  for  rapid  core-genomealignment  and  visualization  of  thousands  of  intraspecific  microbialgenomes.” Genome biology 15.11 (2014): 524  
[3] Aligning  sequence  reads,  clone  sequences  and  assemblycontigs with BWA-MEM.” arXiv preprint arXiv:1303.3997 (2013)  
[4] [https://github.com/genome/bam-readcount]  

