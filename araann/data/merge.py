import json

with open("aa_frame_data_fps.json", "r") as f:
    fps_data: dict[str, dict] = json.load(f)
with open("aa_frame_data_harm.json", "r") as f:
    harm_data: dict[str, dict] = json.load(f)

merged_data = {}

for aa in fps_data:
    merged_data[aa] = fps_data[aa]

for aa in harm_data:
    merged_data[aa] = harm_data[aa]

with open("aa_frame_data.json", "w") as f:
    json.dump(merged_data, f)