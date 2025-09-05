
# CLI Literature Reference Manager

This project provides a command-line tool for managing literature references in repositories, adding papers by DOI, and exporting references in popular citation styles (Harvard, APA, etc.).

## Features
- Create named repositories for your references
- Add papers to a repository using DOI (fetches metadata automatically)
- Export repository references to a text file in Harvard or APA style

## Requirements
- Python 3
- `requests` library (install with `pip install requests`)

## How to Install
```bash 
sudo cp refm.py /usr/local/bin/refm
sudo chmod +x /usr/local/bin/refm
``` 

## Usage

### Create a repository
```bash
refm makr REPONAME
```

### Add a paper by DOI
```bash
refm add DOI REPONAME
# Example:
refm add 10.1038/nphys1170 myrepo
```


### Export repository to a file in a reference style
```bash
refm export REPONAME STYLE OUTFILE
# Example:
refm export myrepo harvard refs.txt
```

Supported styles: `harvard`, `apa` , `mla`, `ieee`, `chicago`, `vancouver`



## Citation Styles
Citation formats are defined in `styles.py`. You can add more styles as needed.

## License
MIT
