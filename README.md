prh-pokemon
===========

Compares company names from the Finnish company registry (PRH) to Pokémon names.

`pokemon.json` via [sindresorhus/pokemon](https://github.com/sindresorhus/pokemon) (MIT license).

Usage
-----

* Create a Python 3 virtualenv, install the requirements from requirements.txt.
* Run `python3 download_prh.py -b 61 -b 62 -b 63` to download all IT companies into `prh.shelf`.
* Run `python3 calculate_distances.py --out-file distances.pickle --result-file-template 'best-{metric}.txt' --best-json best.json` to calculate various distance metrics.
  * Add `--first-word-only` to only take the first word of each name into account.
  * The script does some flattening and preprocessing (e.g. removing "oy", "ab", etc.) before matching. It may be suboptimal.
* Grep the .txts to your heart's content.

