
# CLI Literature Reference Manager

This project provides a command-line tool for managing literature references in repositories, adding papers by DOI, and exporting references in popular citation styles (Harvard, APA, etc.).

## Features
- Create named repositories for your references
- Add papers to a repository using DOI (fetches metadata automatically)
- Export repository references to a text file in Harvard or APA style

## Requirements
- Python 3
- `requests` library (install with `pip install requests`)

## Usage

### Create a repository
```bash
python refm.py makr REPONAME
```

### Add a paper by DOI
```bash
python refm.py add DOI REPONAME
# Example:
python refm.py add 10.1038/nphys1170 myrepo
```


### Export repository to a file in a reference style
```bash
python refm.py export REPONAME STYLE OUTFILE
# Example:
python refm.py export myrepo harvard refs.txt
```

Supported styles: `harvard`, `apa`

### View the entire reference database
```bash
python refm.py view
```
This will print all repositories and their contents in a readable format.

## Citation Styles
Citation formats are defined in `styles.py`. You can add more styles as needed.

## License
MIT
