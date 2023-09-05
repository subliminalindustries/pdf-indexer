# pdf-indexer
Index pdf file paths according to text words


## Usage

```
usage: indexer.py [-h] [--src-dir SRC_DIR] [--output-file OUTPUT_FILE]

Index pdf file paths according to text words

options:
  -h, --help            show this help message and exit
  --src-dir SRC_DIR, -s SRC_DIR
                        Source directory
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        Output file (JSON)
```

## Output

The output contains two dictionaries: `keys` and `keywords`. `keys` contains mappings of file paths to integers, while `keywords` contains mappings of keywords to integers representing file paths as defined in `keys`:

```
{ "keys": { "/path/to/fileA.pdf": 0, ..., "/path/to/fileZ.pdf": 25 }, "keywords": { "bob": [ 0, 5 ], "is": [ 0, ..., 25 ], "your": [ 0, ..., 25 ], "uncle": [ 0, 5 ] }}
```

Punctiation, unicode and whitespace characters are removed from keywords, and keywords are converted to lowercase.
