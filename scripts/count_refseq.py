import os

for files in os.listdir("../Analysis"):
	count = -3
	try:
		for f in os.listdir("../Analysis/"+files+"/REFS"):
			count += 1
	except: print(files)
	print(files, count)
