# Chess games using data with move times

Source data[1] is obtained from the Free Internet Chess Server (FICS). We chose *Standard* games (meaning time 
limits are in the order of tens of minutes per game) from reasonably strong players (average rating per match >2000).

[1]: https://www.ficsgames.org/download.html

## Pre-processed data set

As of now we'll only be looking at a very limited set of parameters so to speed up the Machine Learning algorithms
we've pre-processed the source data into comma separated value files (CSV files) in the `data/` folder. This was done
by running `python preprocess_dataset.py`. The runtime was almost an hour but only uses on thread and can easily be
sped up.

Every line is on the format `white_elo` (int), `black_elo`, `white_time_usage` (real number between 0 and 1 indicating
how much time White player used of their total allowed thinking time), `white_time_usage`, `result` (1 meaning White
wins, 0.5 draw and 0 that Black wins).

## Development

We're caching the source data on a private server to save FICS some valuable bandwith. If you're on a Unix based system
(e.g. Linux, macOS) then you can run the script `download_games.sh` to fetch and unpack the games for you. If not,
download them by hand from <https://misc.bjk.is/ml/games> into a new folder called `games/` and unpack the archives.

You also need to install the Python packages via pip (preferable using virtualenv):

```bash
> virtualenv venv
> sourve venv/bin/activate
> (venv) pip install -r requirements.txt
```

Run the unittests with

```bash
python -m unittest discover -s test/ -t test/
```
