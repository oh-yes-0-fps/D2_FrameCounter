import csv
import json

with open("aa_frame_data.json", "r") as f:
    jdata: dict[str, dict] = json.load(f)

for i in range(4):
    writer = csv.writer(open(f"targeting_{i}.csv", "w"))
    lst = list(jdata.keys())
    #sort by string as int
    lst.sort(key=lambda x: int(x))
    for aa in lst:
        
        
        pixels.insert(0, aa)
        writer.writerow(pixels)
