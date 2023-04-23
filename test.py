import numpy as np
import json 

jdata = json.load(open("Cones/araann/data/aa_frame_data_scout_fps_combined.json", "r"))

entries: list[tuple[int, int]] = []
for aa in jdata:
    val = jdata[aa]["data"]["horizontal_peak"]
    aa = int(aa)
    print(f"{aa},{val}")
    entries.append((aa, val))

entries = np.array(entries) # type: ignore
#get linear est of entries
m, b = np.polyfit(entries[:, 0], entries[:, 1], 1) # type: ignore
#get r2
r2 = 1 - (np.sum((entries[:, 1] - (m*entries[:, 0] + b))**2)/np.sum((entries[:, 1] - np.mean(entries[:, 1]))**2)) # type: ignore


print(f"m: {m}, b: {b}, r2: {r2}")