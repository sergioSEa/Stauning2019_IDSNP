import os
import sys

directory = sys.argv[1]
for folders in os.listdir(directory+"/refseq/bacteria/"):
        if folders.startswith("GCF"): pass
        else: continue

        if folders.endswith("gz"): continue

        for file in os.listdir(directory+"/refseq/bacteria/"+folders):
                if file.endswith(".gz"):
                        print("mv "+ directory+"/refseq/bacteria/"+folders +"/"+ file +" "+ directory)
                        print("rm -r " + directory+"/refseq/bacteria/"+ folders)
print("gunzip -f "+directory+ "/*")
