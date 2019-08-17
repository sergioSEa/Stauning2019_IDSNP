import sys
import numpy as np 
vcf = sys.argv[1]
bac = sys.argv[2]
counter = 0

with open(vcf, "r") as File:
        for line in File:
                if line.startswith("#CHROM"):
                        l = line.rstrip().split("\t")
                        pos = [i for i,x in enumerate(l) if x == bac][0]

                elif line.startswith("#"): continue

                else:
                        l = line.rstrip().split("\t")
                        arr = np.asarray(l[9:]).astype(np.float)

                        if l[pos] == "1" and  np.sum(arr) == 1 and l[6] == "PASS":
                                counter += 1
                                print(line.rstrip())
