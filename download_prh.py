import requests
import shelve
import argparse


def download_business_line(shelf, code):
    sess = requests.Session()
    url = 'https://avoindata.prh.fi/bis/v1?totalResults=true&maxResults=1000&resultsFrom=0&businessLineCode=%s' % code
    while url:
        print(url)
        print(len(shelf))
        resp = sess.get(url)
        resp.raise_for_status()
        data = resp.json()
        url = data.get('nextResultsUri')
        for result in data.get('results', ()):
            shelf[result['businessId']] = result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--business-line-code', '-b', dest='codes', action='append', default=[])
    ap.add_argument('--file', default='prh.shelf')
    args = ap.parse_args()
    shelf = shelve.open(args.file)
    for code in args.codes:
        download_business_line(shelf, code=code)


if __name__ == '__main__':
    main()
