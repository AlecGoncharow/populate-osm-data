import os
import subprocess

def main():
    for f in os.listdir("./osm_json"):
        print(f)
        subprocess.run(["mongoimport", "-d", "osm", "-c", "cities", "--file", f"./osm_json/{f}"])

if __name__ == '__main__':
    main()
