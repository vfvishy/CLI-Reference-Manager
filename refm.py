#!/usr/bin/env python3
import sys
import json
import os
from typing import Dict, Any
import requests

REFERENCE_STYLES = {
	"harvard": "{author} ({year}). {title}. {journal}, {publisher}.",
	"apa": "{author} ({year}). {title}. {journal}. {publisher}.",
	"mla": "{author}. \"{title}.\" {journal}, {year}, {publisher}.",
	"chicago": "{author}. {title}. {journal}. {publisher}, {year}.",
	"vancouver": "{author}. {title}. {journal}. {year}; {publisher}.",
	"ieee": "{author}, \"{title},\" {journal}, {publisher}, {year}."
}

IN_TEXT_CITATIONS = {
	"harvard": "({author}, {year})",
	"apa": "({author}, {year})",
	"mla": "({author} {year})",
	"chicago": "({author} {year})",
	"vancouver": "[{author} {year}]",
	"ieee": "[{author}, {year}]"
}


def get_db_path():
	xdg_data_home = os.environ.get("XDG_DATA_HOME")
	if xdg_data_home:
		base_dir = os.path.join(xdg_data_home, "refm")
	else:
		base_dir = os.path.expanduser("~/.local/share/refm")
	os.makedirs(base_dir, exist_ok=True)
	return os.path.join(base_dir, "refm_db.json")

DB_PATH = get_db_path()

def load_db() -> Dict[str, Any]:
	if not os.path.exists(DB_PATH):
		return {}
	with open(DB_PATH, "r") as f:
		return json.load(f)

def save_db(db: Dict[str, Any]):
	with open(DB_PATH, "w") as f:
		json.dump(db, f, indent=2)
def fetch_metadata(doi: str) -> Dict[str, Any]:
	url = f"https://api.crossref.org/works/{doi}"
	resp = requests.get(url)
	if resp.status_code != 200:
		raise Exception("DOI not found")
	data = resp.json()["message"]
	return {
		"title": data.get("title", [""])[0],
		"author": ", ".join([f"{a.get('given', '')} {a.get('family', '')}" for a in data.get("author", [])]),
		"year": data.get("issued", {}).get("date-parts", [[""]])[0][0],
		"journal": data.get("container-title", [""])[0],
		"publisher": data.get("publisher", "")
	}

def add_repo(db, repo):
	if repo in db:
		print(f"Repository '{repo}' already exists.")
		return
	db[repo] = []
	save_db(db)
	print(f"Repository '{repo}' created.")

def add_paper(db, repo, doi):
	if repo not in db:
		print(f"Repository '{repo}' does not exist.")
		return
	try:
		meta = fetch_metadata(doi)
	except Exception as e:
		print(f"Error: {e}")
		return
	db[repo].append(meta)
	save_db(db)
	print(f"Paper added to '{repo}'.")

def export_repo(db, repo, style, out_file):
	if repo not in db:
		print(f"Repository '{repo}' does not exist.")
		return
	if style not in REFERENCE_STYLES:
		print(f"Style '{style}' not supported.")
		return
	fmt = REFERENCE_STYLES[style]
	with open(out_file, "w") as f:
		for ref in db[repo]:
			f.write(fmt.format(**ref) + "\n")
	print(f"Exported '{repo}' to '{out_file}' in {style} style.")


def export_short_citation(db, repo, style, out_file):
	if repo not in db:
		print(f"Repository '{repo}' does not exist.")
		return
	if style not in IN_TEXT_CITATIONS:
		print(f"Style '{style}' not supported for in-text citation.")
		return
	fmt = IN_TEXT_CITATIONS[style]
	with open(out_file, "w") as f:
		for ref in db[repo]:
			f.write(fmt.format(**ref) + "\n")
	print(f"Exported short citations for '{repo}' to '{out_file}' in {style} style.")

def main():
	if len(sys.argv) < 3:
		print("Usage:\n  refm makr REPONAME\n  refm add DOI REPONAME\n  refm export REPONAME STYLE OUTFILE\n  refm shortc REPONAME STYLE OUTFILE")
		return
	cmd = sys.argv[1]
	db = load_db()
	if cmd == "makr" and len(sys.argv) == 3:
		add_repo(db, sys.argv[2])
	elif cmd == "add" and len(sys.argv) == 4:
		add_paper(db, sys.argv[3], sys.argv[2])
	elif cmd == "export" and len(sys.argv) == 5:
		export_repo(db, sys.argv[2], sys.argv[3], sys.argv[4])
	elif cmd == "shortc" and len(sys.argv) == 5:
		export_short_citation(db, sys.argv[2], sys.argv[3], sys.argv[4])
	else:
		print("Invalid command or arguments.")



if __name__ == "__main__":
	main()
