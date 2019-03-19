import argparse
import collections
import json
import Levenshtein as lev
import pickle
import re
import requests
import shelve
import tqdm
import unicodedata


def flatten(s, first_word_only=False):
    s = unicodedata.normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode()
    if first_word_only:
        s = s.split(None)[0]
    s = re.sub(r'[^\w]+', '', s)
    return s


def read_names(shelf_filename):
    with shelve.open(shelf_filename) as shelf:
        for val in shelf.values():
            name = val['name']
            name = re.sub(r'\b(oy|oyj|ky|ltd|inc|ab)\b', ' ', name, flags=re.I)
            name = name.strip()
            yield name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in-file', default='prh.shelf')
    ap.add_argument('--out-file', required=True)
    ap.add_argument('--first-word-only', default=False, action='store_true')
    args = ap.parse_args()
    names = set(read_names(args.in_file))
    companies = {l: flatten(l, first_word_only=args.first_word_only) for l in names}
    pokeymans = {l: flatten(l, first_word_only=args.first_word_only) for l in json.load(open('pokemon.json'))}

    distances = {}

    citer = list(sorted(companies.items()))
    piter = list(sorted(pokeymans.items()))
    for company, company_flat in tqdm.tqdm(citer):
        for pokeyman, pokeyman_flat in piter:
            pair = (company, pokeyman)
            distances.setdefault(pair, {})  # save some time vs. defaultdict
            distances[pair]['lev'] = lev.distance(company_flat, pokeyman_flat)
            distances[pair]['jaro'] = lev.jaro(company_flat, pokeyman_flat)
            distances[pair]['jaro_winkler'] = lev.jaro_winkler(company_flat, pokeyman_flat)
            distances[pair]['ratio'] = lev.ratio(company_flat, pokeyman_flat)

    with open(args.out_file, 'wb') as outf:
        pickle.dump(distances, outf, -1)


if __name__ == '__main__':
    main()
