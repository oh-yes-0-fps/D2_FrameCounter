import json

with open("aa_frame_data_fps.json", "r") as f:
    fps_data: dict[str, dict] = json.load(f)
with open("aa_frame_data_shotguns.json", "r") as f:
    harm_data: dict[str, dict] = json.load(f)

merged_data = {}

for aa in harm_data:
    if not int(aa) + 10 > 100:
        merged_data[str(int(aa)+10)] = {}
        merged_data[str(int(aa)+10)]["screen_height"] = harm_data[aa]["screen_height"]
        merged_data[str(int(aa)+10)]["screen_width"] = harm_data[aa]["screen_width"]
        merged_data[str(int(aa)+10)]["render_resolution"] = harm_data[aa]["render_resolution"]
        merged_data[str(int(aa)+10)]["color"] = harm_data[aa]["color"]
        merged_data[str(int(aa)+10)]["data"] = harm_data[aa]["data_t3"]

for aa in harm_data:
    if not int(aa) + 8 > 100:
        merged_data[str(int(aa)+8)] = {}
        merged_data[str(int(aa)+8)]["screen_height"] = harm_data[aa]["screen_height"]
        merged_data[str(int(aa)+8)]["screen_width"] = harm_data[aa]["screen_width"]
        merged_data[str(int(aa)+8)]["render_resolution"] = harm_data[aa]["render_resolution"]
        merged_data[str(int(aa)+8)]["color"] = harm_data[aa]["color"]
        merged_data[str(int(aa)+8)]["data"] = harm_data[aa]["data_t2"]

for aa in harm_data: 
    if not int(aa) + 5 > 100:
        merged_data[str(int(aa)+5)] = {}
        merged_data[str(int(aa)+5)]["screen_height"] = harm_data[aa]["screen_height"]
        merged_data[str(int(aa)+5)]["screen_width"] = harm_data[aa]["screen_width"]
        merged_data[str(int(aa)+5)]["render_resolution"] = harm_data[aa]["render_resolution"]
        merged_data[str(int(aa)+5)]["color"] = harm_data[aa]["color"]
        merged_data[str(int(aa)+5)]["data"] = harm_data[aa]["data_t1"]

for aa in harm_data:
    merged_data[aa] = {}
    merged_data[aa]["screen_height"] = harm_data[aa]["screen_height"]
    merged_data[aa]["screen_width"] = harm_data[aa]["screen_width"]
    merged_data[aa]["render_resolution"] = harm_data[aa]["render_resolution"]
    merged_data[aa]["color"] = harm_data[aa]["color"]
    merged_data[aa]["data"] = harm_data[aa]["data_t0"]



    

with open("aa_frame_data_shotgun_combined2.json", "w") as f:
    json.dump(merged_data, f)