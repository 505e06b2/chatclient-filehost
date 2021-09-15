#!/usr/bin/env python3

import argparse, json, os, urllib.request

parser = argparse.ArgumentParser(description="Upload to Guilded")
parser.add_argument("file_path", help="File to upload")

args = parser.parse_args()

def generateRequests(options, file_path):
	file_bytes = b""
	with open(file_path, "rb") as f:
		file_bytes = f.read()

	#split into <= ?Mb chunks
	chunk_size = options["max_file_size"] * 1024 #kb -> b
	file_byte_chunks = [file_bytes[i:i+chunk_size] for i in range(0, len(file_bytes), chunk_size)]
	file_name = os.path.basename(file_path)

	file_index = 0
	extension = ""

	ret = []
	for current_chunk in file_byte_chunks:
		if len(file_byte_chunks) > 1:
			file_index += 1
			extension = f".{file_index:03d}"

		ret.append(
			urllib.request.Request(
				"https://media.guilded.gg/media/upload?dynamicMediaTypeId=ContentMedia",
				headers={
					"content-type": "multipart/form-data; boundary=boundary"
				},
				method="POST",
				data=b"\r\n".join([
					b'--boundary',
					b'content-disposition: form-data; name="file"; filename="' + f"{file_name}{extension}".encode("utf8") + b'"',
					b'content-type: video/mp4',
					b'',
					current_chunk,
					b'--boundary--',
					b''
				])
			)
		)

	return ret

options = {}
with open("config.json") as f:
	options = json.load(f)

links = []
for x in generateRequests(options, args.file_path):
	try:
		ret = json.load( urllib.request.urlopen(x) )
		link = ret["url"].split("?")[0]
		if options["print_links"]: print(link)
		links.append(link)
	except urllib.error.HTTPError as e:
		print(e.read())
		print("Ensure it's an image or video file - the magic bytes are checked!")
		break

if len(links) and options["link_extension"]:
	file_name = os.path.basename(args.file_path) + "." + options["link_extension"]
	with open(file_name, "w") as f:
		for x in links:
			f.write(x + "\n")
	print("Saved to", file_name)
