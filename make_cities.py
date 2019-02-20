import json
import subprocess
import osm_to_adj
import os

with open("./areas.json", "r") as f:
    states = json.load(f)

filter_args = '--keep="highway=motorway =trunk =primary =secondary =tertiary =unclassified =primary_link =secondary_link =tertiary_link =trunk_link =motorway_link"'


def main():
    for state, cities in states.items():
        file_name = f"./osm_data/{state}-latest.osm.pbf"
        for city, box in cities.items():
            print(state, city)
            box_str = f"-b={box[0]},{box[1]},{box[2]},{box[3]}"
            out_name = f"{city}.o5m"
            out = f"-o={out_name}"
            convert = subprocess.run(["./osmconvert", file_name, box_str, out])
            if convert.returncode != 0:
                print("something broke in covert")
                continue
            print("conversion done")
            args = f"./osmfilter {out_name} {filter_args} --drop-version -o={city}.xml"
            fil = subprocess.run(args, shell=True)
            if fil.returncode != 0:
                print("something broke in filter")
                continue
            print("filter done")
            ret = osm_to_adj.main(f"{city}.xml", 0, city)
            if ret is None:
                print("something broke in osm_to_adj")
                continue
            print("osm_to_adj done")
            data = json.loads(ret)
            print(f"nodes: {len(data['nodes'])}, edges: {len(data['edges'])}")
            with open(f"./osm_json/{city}.json", "w") as f:
                json.dump(data, f)

            shrink = osm_to_adj.main(f"{city}.xml", 5, f"shrunk_{city}")
            if shrink is None:
                print("something broke in osm_to_adj")
                continue
            print("osm_to_adj shrunk done")
            data = json.loads(shrink)
            print(f"nodes: {len(data['nodes'])}, edges: {len(data['edges'])}")
            with open(f"./osm_json/shrunk_{city}.json", "w") as f:
                json.dump(data, f)
            # remove intermediate files
            os.remove(out_name)
            os.remove(f"{city}.xml")

            print("done")


if __name__ == '__main__':
    main()
