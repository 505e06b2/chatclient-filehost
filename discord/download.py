#!/usr/bin/env python3

import argparse, urllib.request

parser = argparse.ArgumentParser(description="Download from Discord")
parser.add_argument("file_path", help="File to piece together and download")

args = parser.parse_args()

links = []
with open(args.file_path) as f:
	links = f.readlines()

file_name = ".".join(args.file_path.split(".")[:-1])

with open(file_name, "wb") as out:
	for x in links:
		with urllib.request.urlopen(urllib.request.Request(x, headers={"user-agent": "DiscordBot"})) as r:
			out.write(r.read())

print("Saved to", file_name)
