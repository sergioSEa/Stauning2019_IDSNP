from pathlib import *
from subprocess import call
import argparse
import os 
import sys


#######################INPUT##############################
parser = argparse.ArgumentParser()
parser.add_argument('--isolate', '-i', action = 'store', default = '', dest = 'isolate')
parser.add_argument('--metagenome', '-w', action = 'store', default = 'n/p', dest = 'metagenome')
parser.add_argument('--reference', '-r', action = 'store', default = 'n/p', dest = 'reference')
parser.add_argument('--ForwardRead', '-R1', action = 'store', default = 'n/p', dest = 'ForwardRead')
parser.add_argument('--ReverseRead', '-R2', action = 'store', default = 'n/p', dest = 'ReverseRead')
parser.add_argument('--Remove', '-rm', action = 'store', default = 'False', dest = 'remove')
parser.add_argument('--species', '-sp', action = 'store', default = 'False', dest = 'species')
###########################################################

print(sys.argv)

def Get_species(isolate):
    'If no species is given as input, read them from a Design'
    print("Getting species of isolated")
    species = "None"
    with open("Design.csv","r") as Design:
        for line in Design:
            l = line.rstrip().split(";")
            if l[0] == isolate:
                species = l[2]
    return species
def Download_ncbi(species, output, type):
    'Download NCBI complete genomes of a species'
    species_translation = {
    "s.aureus": "Staphylococcus aureus", "Neisseria sp.":"Neisseria sp.", "S. arlettae": "Staphylococcus arlettae", 
    "S. saprophyticus": "Staphylococcus saprophyticus", "S.haemolyticus":"Staphylococcus haemolyticus" }
    try: species = species_translation[species]
    except: species
    print("Downloading  genomes of "+ species +" from NCBI")
    call("bash scripts/download_genus "+ str(Directory_NCBI) + " " + species + " " + type, shell = True)

args = parser.parse_args()
#Prepare inputs
isolate = args.isolate
for i in os.listdir("Data/WGS_Assemblies/"):
    if i.startswith(isolate):
        isolate_path = "Data/WGS_Assemblies/" + i 
name = isolate.split("_")[0]


metagenome = args.metagenome
metagenome_path = "Data/fastq_metagenomes/"

print("Currently Running "+isolate + " with metagenome " + metagenome)

if metagenome != "n/p":
    
    if args.ForwardRead == "n/p" and args.ReverseRead == "n/p":
        found = False
        mt  = metagenome.split("-")[0]
        for files in os.listdir("Data/fastq_metagenomes/"):
            if files.startswith(mt):
                read = files.split("_")[-1].split(".")[0]
                found = True
                if read == "R1":
                    metagenome_FR = "Data/fastq_metagenomes/"+files
                if read == "R2":
                    metagenome_RR = "Data/fastq_metagenomes/"+files
        if found == False:
            exit("Error, no metagenome read files were found")
    else:
        metagenome_FR = args.ForwardRead
        metagenome_RR = args.ReverseRead
        
reference = args.reference
if args.species == "n/p":
     Genus = Get_species(name)
else:
     Genus = args.species

#Input Check
if Genus == "None": 
    exit("Error: Isolate not found in design")
if metagenome == "n/p":
    mode = "Align"
else:
    mode = "Align_n_metrics"


#Creation of Directories if not present
Directory_work = Path('./Analysis/'+name)
if not Directory_work.exists():
    print("Creating Dir")
    call("mkdir "+ str(Directory_work), shell = True)


#If reference path not provided, check whether it is on Directory_work:
get_reference = False
if reference == "n/p":
    print("Getting Ref name")
    found = False
    for f in os.listdir(str(Directory_work)):
        if str(f).endswith(".fasta") or str(f).endswith(".fa") or str(f).endswith(".fna"):
            reference = Directory_work / (f)
            found = True
    if found == False:
        get_reference = True
        #exit("Error: No reference path found, try downloading a reference for "+Genus)
    
Directory_NCBI = Directory_work / ("REFS")

if not Directory_NCBI.exists():
    print("Generating NCBI directory")
    call("mkdir "+ str(Directory_NCBI), shell = True)

#Download NCBI files if not present
empty = len(list(Directory_NCBI.glob('*')))
if empty == 0:
    Download_ncbi(Genus, str(Directory_NCBI), "complete")
    empty = len(list(Directory_NCBI.glob('**/*')))
    if empty == 0:
        exit("Error: Download from NCBI failed")
    #Get files out and uncompressed
    print("Uncompressing NCBI assemblies")    
    order = "python scripts/get_NCBI_out.py "+str(Directory_NCBI) + " > "+str(Directory_NCBI / "command")
    call(order, shell = True)
    call("bash "+str(Directory_NCBI / "command"), shell = True)
    
    
    #If we don't have a reference, choose one
    if get_reference == True:
        print("Getting reference from downloaded NCBI files")
        import random
        r = random.choice(list(Directory_NCBI.glob('*')))
        command = "cp " + str(r) + " " +  str(Directory_work)
        call(command, shell = True)
        reference = Directory_work / (r.name)
    
    if len(list(Directory_NCBI.glob('*'))) < 3:
        print("Due to small amount of Complete genomes, draft genomes will be downloaded")
        Download_ncbi(Genus, str(Directory_NCBI), "draft")
        order = "python scripts/get_NCBI_out.py "+str(Directory_NCBI) + " > "+str(Directory_NCBI / "command")
        call(order, shell = True)
        call("bash "+str(Directory_NCBI / "command"), shell = True)
        
    print("Creating symlink from file")
    #Create symlink on Directory NCBI to the assembly
    order = "ln -s "+ "~/RESEARCH/"+isolate_path + " ~/RESEARCH/" +str(Directory_NCBI)
    call(order, shell = True)

file_align = Directory_work / ("Align.sh")
unique_variants = Directory_work / ("unique_snps_"+name+".txt")
REFS = str( ("~/RESEARCH/") / Directory_work / ("REFS"))
VCF = Directory_work / ("output.vcf")
output_parsnp =  Directory_work / ("parsnp_output")

if not VCF.exists():    
# If NCBI files ready, REF and Isolate: Then start the fun

    #if not file_align.exists():
    print("Running Align command")
    order = "mkdir "+ str(output_parsnp)
    call(order,shell="True")
    order = "bash scripts/Align.sh "+ str(("~/RESEARCH/") / reference) + " "+ str(REFS) + " " + str(output_parsnp) + " " + str(VCF)
    print(order)
    call(order,shell="True")


unique_variants = Directory_work / ("unique_snps.txt")
if not unique_variants.exists():
    print("Getting unique variants")
    order = "python scripts/identify_unique_variants.py "+ str(VCF) +" "+ Path(isolate_path).name + " >"+ str(unique_variants)
    call(order, shell= True)
    print("Variants generated in "+ str(unique_variants))

remove = args.remove

if mode == "Align": exit("Pipeline finish")
print("Starting Metagenome comparison")
SAM = str(Directory_work / (metagenome + ".sam"))
BAM = str(Directory_work / (metagenome + ".bam"))
Sorted_BAM = str(Directory_work / (metagenome + "_sort.bam"))
metrics = str(Directory_work / (metagenome+"_metrics.txt"))
count_by_nucleotide= str(Directory_work / (metagenome+"_count_by_nucleotide.txt"))
output_counting= str(Directory_work / (metagenome+"_output_counting.txt"))
unique_in_meta= str(Directory_work / (metagenome+"_unique_reads_metagenome.txt"))

if not Path(Sorted_BAM).exists():
    print("Mapping")
    order = "bash scripts/map.sh " + str(reference) + " " +  str(metagenome_FR) + " " + str(metagenome_RR) + " " + SAM + " " + BAM + " " + Sorted_BAM
    call(order, shell="True")
    
print("Stats Alignment")
order = ["bash scripts/Stats_Align.sh", str(reference),Sorted_BAM, str(output_counting),str(unique_variants),str(metrics),str(count_by_nucleotide),str(unique_in_meta)] 
call(" ".join(order),shell= "True")

print("Pipeline finish")

if remove == "True" or remove == True:
    print("Removing Intermediates")
    for i in [SAM,BAM,Sorted_BAM, count_by_nucleotide, output_counting, unique_in_meta]:
        order = "rm "+i
        call(order, shell="True")
