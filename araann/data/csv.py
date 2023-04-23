import csv
import json

with open("aa_frame_data_harm.json", "r") as f:
    jdata: dict[str, dict] = json.load(f)

for i in range(4):
    writer = csv.writer(open(f"targeting_{i}.csv", "w"))
    lst = list(jdata.keys())
    #sort by string as int
    lst.sort(key=lambda x: int(x))
    target = 'data_t'
    target = target + str(i)
    for aa in lst:
        pixels = []
        for x in jdata[aa][target]["horizontal"]:
            pixels.insert(0, x[0])
        writer.writerow(pixels)


