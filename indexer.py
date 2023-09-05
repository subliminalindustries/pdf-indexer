#! /usr/bin/env python

import collections
import json
import os
import string
import sys
import pdftotext

from natsort import natsorted
from glob import iglob
from argparse import ArgumentParser

parser = ArgumentParser(description='Index pdf file paths according to text words')

parser.add_argument('--src-dir', '-s', action='append', help='Source directory')
parser.add_argument('--output-file', '-o', type=str, default='index.json', help='Output file (JSON)')


def find_recursive(path: str, ext: str = 'pdf'):
    result = list(iglob(os.path.join(path, f'*.{ext}')))

    for fp in os.listdir(os.path.realpath(path)):
        fp = os.path.realpath(os.path.join(path, fp))
        if os.path.isdir(fp):
            result.extend(find_recursive(fp, ext))

    return result


def extract_words(filename: str):
    print(f'Processing {filename}..')

    with open(filename, 'rb') as fp:
        pdf = pdftotext.PDF(pdf_file=fp)

    text = ' '.join([str(page) for page in pdf])
    text = text.replace('\n', ' ')
    text = ' '.join(text.strip().split())

    words = text.split()

    result = []
    for w in words:
        w = str(w.encode('ascii', 'ignore'))

        for c in string.punctuation:
            w = w.replace(c, ' ')

        for c in string.whitespace:
            w = w.replace(c, ' ')

        for s in w.split():
            s = s.lower()
            if result.__contains__(s):
                continue

            result.append(s)

    return result


if __name__ == '__main__':
    args = parser.parse_args(sys.argv[1:])

    output_filename = os.path.realpath(args.output_file)

    paths = args.src_dir
    if type(paths) is str:
        paths = [paths]

    files = []
    for p in paths:
        files.extend(find_recursive(p))

    files = natsorted(files)

    keyed_files = {}
    for k, v in enumerate(files):
        keyed_files[v] = k

    mapping = {
        'keys': keyed_files,
        'keywords': {}
    }
    for f in files:
        key = keyed_files[f]
        text_words = extract_words(f)
        for tw in text_words:
            if mapping['keywords'].get(tw) is None:
                mapping['keywords'][tw] = []

            mapping['keywords'][tw].append(key)

    mapping = collections.OrderedDict(natsorted(mapping.items()))

    with open(output_filename, 'w') as fp:
        json.dump(mapping, fp)
