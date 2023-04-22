import json
import matplotlib.pyplot as plt
import numpy as np

with open("aa_frame_data.json", "r") as f:
    jdata: dict[str, dict] = json.load(f)

stuff = {}

#make a horizontal bar graph for each aa
aa_values = []
dist_values = []
for aa in jdata:
    if aa == "100":
        continue
    aa_val = int(aa)
    data = jdata[aa]["data_t3"]["horizontal"]
    furtherst_dist = 0.0
    for val, dist in data:
        if val > 0:
            furtherst_dist = dist
    # furtherst_dist = sum([val for val, dist in data]) / len(data)
    color = "red"
    if jdata[aa]["screen_height"] == 2160:
        color = "blue"
    aa_values.append(aa_val)
    dist_values.append(furtherst_dist)
    stuff[aa_val] = furtherst_dist
    if jdata[aa]["adjuster_mod"]:
        plt.bar(aa_val, furtherst_dist, color=color, edgecolor="yellow", hatch="///")
    else:
        plt.bar(aa_val, furtherst_dist, color=color)

# for i, val in enumerate(aa_values):
#     lowest_aa = min(aa_values)
#     highest_aa = max(aa_values)
#     lowest_dist = dist_values[aa_values.index(lowest_aa)]
#     highest_dist = dist_values[aa_values.index(highest_aa)]

#     #draw a line from the lowest to the highest
#     plt.plot([lowest_aa, highest_aa], [lowest_dist, highest_dist], color="black", linestyle="dashed")

#linear estimate stuff with keys as x and value as y
x = np.array(list(stuff.keys()))
y = np.array(list(stuff.values()))
m, b = np.polyfit(x, y, 1)
#get r2
r2 = np.corrcoef(x, y)[0, 1] ** 2
plt.plot(x, m*x + b, color="black", linestyle="dashed")
print(f"y = {m:.9f}x + {b:.9f} : r2 = {r2:.3f}")

with open("stuff.json", "w") as f:
    #sort stuff
    stuff = {k: v for k, v in sorted(stuff.items(), key=lambda item: item[1])}
    json.dump(stuff, f)

plt.show()