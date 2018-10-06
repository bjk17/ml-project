# Chess games using data with move times

Source data[1] is obtained from the Free Internet Chess Server (FICS). We chose *Standard* games (meaning time 
limits are in the order of tens of minutes per game) from reasonably strong players (average rating per match >2000).

[1]: https://www.ficsgames.org/download.html

## Pre-processed data set

As of now we'll only be looking at a very limited set of parameters so to speed up the Machine Learning algorithms
we've pre-processed the source data into comma separated value files (CSV files) in the `data1/` and `data2/` folders.
This was done by running different version of `python preprocess_dataset.py`.

### `data1/`

Every line is on the format `white_elo` (int), `black_elo`, `white_time_usage` (real number between 0 and 1 indicating
how much time White player used of their total allowed thinking time), `white_time_usage`, `result` (1 meaning White
wins, 0.5 draw and 0 that Black wins).

Games with `plycount < 2` (not both sides having played a move) were filtered out.

### `data2/`

Every line is on the format

```text
white_elo, black_elo, white_time_usage, black_time_usage, crude_position_estimate, result
```

where the time usage is *time left* as a ratio of possible time left (e.g. if the player would always play their moves
instantly this value but be `1.0`), and the crude position estimate is simply piece counting where the white's pieces
count as positive values and black pieces as negative values. Queens are worth 9 points, Rooks 5 points, Knights and
Bishops 3 points and Pawns 1 point.

Another ides would be to incorporate a chess engine's evaluation (e.g. the open source chess engine [Stockfish](
https://stockfishchess.org)), fixed to a certain ply depth count.

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
