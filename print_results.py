import pickle
import collections
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in-file', required=True)
    ap.add_argument('--metric', required=True)
    ap.add_argument('--min', dest='order', action='store_const', const='min')
    ap.add_argument('--max', dest='order', action='store_const', const='max')
    args = ap.parse_args()
    if not args.order:
        ap.error('specify --min or --max')

    with open(args.in_file, 'rb') as f:
        distances = pickle.load(f)

    metrics = collections.defaultdict(dict)

    for (company, pokeyman), info in distances.items():
        if args.metric not in info:
            raise ValueError('unknown metric %s, try one of %s' % (args.metric, info.keys()))
        metrics[company][pokeyman] = info[args.metric]

    comparator = min if args.order == 'min' else max

    for company, pokeymans in sorted(metrics.items()):
        best_name, best_metric = comparator(pokeymans.items(), key=lambda p: p[1])
        print(company, best_name, best_metric, sep=';')


if __name__ == '__main__':
    main()
