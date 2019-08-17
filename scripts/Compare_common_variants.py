import sys
sample = sys.argv[1]
meta = sys.argv[2]
output = sys.argv[3]
to_find = {}

with open(sample) as variants_wound:
        for line in variants_wound:
                if line[0] == "#" or len(line) < 6: continue
                l = line.split("\t")
                position = l[1]
                variant = l[4]
                to_find[position] = variant


trans = {"A":4,"T":7,"G":6,"C":5}
majority = 0
missing = 0
match = 0
with open(meta) as meta_variants:
        # NC_007795.1     102748  C       3       0       0       0       3       0
        for i in meta_variants:
                l = i.rstrip().split('\t')
                V = to_find[l[1]]
                pos = trans[V]
                count = int(l[pos])
                try: ratio = float(count)/float(l[3])
                except: 
                    continue 

                if count == 0: missing += 1
                elif ratio >= 0.5: majority += 1
                match +=1
print(majority,missing,match)


with open(output, "w") as f:
    f.write("Positions_covered_and_varaint_in_majority\tNo_variant_but_position_coverd\tPositions_with_1_Read(out_of_total)\n")
    f.write(str(majority)+"\t"+ str(missing) + "\t"+ str(match)+"\n")
