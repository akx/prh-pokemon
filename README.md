prh-pokemon
===========

Compares company names from the Finnish company registry (PRH) to Pokémon names.

`pokemon.json` via [sindresorhus/pokemon](https://github.com/sindresorhus/pokemon) (MIT license).

Usage
-----

* Create a Python 3 virtualenv, install the requirements from requirements.txt.
* Run `python3 download_prh.py -b 61 -b 62 -b 63` to download all IT companies into `prh.shelf`.
* Run `python3 calculate_distances.py --out-file distances.pickle` to calculate various distance metrics.
  * Add `--first-word-only` to only take the first word of each name into account.
  * The script does some flattening and preprocessing (e.g. removing "oy", "ab", etc.) before matching. It may be suboptimal.
* Run `python3 print_results.py --in-file distances.pickle --metric lev --min > best-min-lev.txt` to get a file of best matches given the Levenshtein metric.
  * Metrics supported are `lev`, `jaro`, `jaro_winkler` and `ratio`. With the `jaro` ones, use `--max` instead of `--min`.
* Grep to your heart's content.