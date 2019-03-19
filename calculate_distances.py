import argparse
import collections
import io
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


metric_infos = {
    'lev': (lev.distance, min),
    'jaro': (lev.jaro, max),
    'jaro_winkler': (lev.jaro_winkler, max),
    'ratio': (lev.ratio, max),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in-file', default='prh.shelf')
    ap.add_argument('--out-pickle', default=None)
    ap.add_argument('--first-word-only', default=False, action='store_true')
    ap.add_argument('--result-file-template', default=None, help='e.g. best-{metric}.txt')
    ap.add_argument('--best-json', default=None)
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
            for metric, (dfunc, cfunc) in metric_infos.items():
                distances[pair][metric] = dfunc(company_flat, pokeyman_flat)

    if args.out_pickle:
        print('Writing %s...' % args.out_pickle)
        with open(args.out_pickle, 'wb') as outf:
            pickle.dump(distances, outf, -1)

    if args.result_file_template or args.best_json:
        best_json_data = collections.defaultdict(dict)

        for metric, (dfunc, cfunc) in metric_infos.items():

            print('Gathering %s...' % metric)
            metrics = collections.defaultdict(dict)
            for (company, pokeyman), info in tqdm.tqdm(distances.items()):
                metrics[company][pokeyman] = info[metric]

            if args.result_file_template:
                filename = args.result_file_template.replace('{metric}', metric)
                print('Writing %s...' % filename)
                outf = open(filename, 'w')
            else:
                outf = io.StringIO()

            with outf:
                for company, pokeymans in tqdm.tqdm(sorted(metrics.items())):
                    best_name, best_metric = cfunc(pokeymans.items(), key=lambda p: p[1])
                    print(company, best_name, best_metric, sep=';', file=outf)
                    best_json_data[company][metric] = (best_name, best_metric)

        if args.best_json:
            print('Writing %s...' % args.best_json)
            with open(args.best_json, 'w') as outf:
                json.dump(best_json_data, outf)


if __name__ == '__main__':
    main()
