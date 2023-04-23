import json

FILE_NAME = "aa_frame_data_scout_fps"

with open("./Cones/araann/data/"+FILE_NAME+".json", "r") as f:
    jdata: dict[str, dict] = json.load(f)

merged_data = {}

mod_to_val = {
    0: 0,
    1: 5,
    2: 8,
    3: 10
}

for aa in jdata:
    val = jdata[aa]
    aa = int(aa)
    for idx in val["targeting_mods_tested"]:
        if aa+mod_to_val[idx] > 100 or aa+mod_to_val[idx] in merged_data:
            continue
        cond_data = val.copy()
        cond_data["data"] = {"horizontal_peak": cond_data[f"data_t{idx}"].copy()["horizontal_peak"]}
        del cond_data["targeting_mods_tested"]
        del cond_data["data_t0"]
        del cond_data["data_t1"]
        del cond_data["data_t2"]
        del cond_data["data_t3"]
        merged_data[aa+mod_to_val[idx]] = cond_data

with open("./Cones/araann/data/"+FILE_NAME+"_combined"+".json", "w") as f:
    json.dump(merged_data, f)