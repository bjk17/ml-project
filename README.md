# Chess games using data with move times

Source data[1] is obtained from the Free Internet Chess Server (FICS). We chose *Standard* games (meaning time 
limits are in the order of tens of minutes per game) from reasonably strong players (average rating per match >2000).

[1]: https://www.ficsgames.org/download.html

## Pre-processed data set

As of now we'll only be looking at a very limited set of parameters so to speed up the Machine Learning algorithms
we've pre-processed the source data into comma separated value files (CSV files) in the `data1/`, `data2/` and `data3`
folders. This was done by running different versions of `python preprocess_dataset.py`.

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

### `data3/`

In `data2/` we had a bias towards Black in the position estimate as Black might have captured a piece in the 20th move
which White would recapture back in move 21 but isn't counted for in our crude position estimate. Instead we're now
both estimating the position after White's 20th move (`white_position_estimate`) and Black's 20th move 
(`black_position_estimate`) resulting in lines on the form

```text
white_elo, black_elo, white_time_usage, black_time_usage, white_position_estimate, black_position_estimate, result
```

As a matter of fact we can see that we managed to cancel out the bias.

````bash
> cat data3/ficsgamesdb_201[0-7]_standard2000_movetimes.csv | awk -F , '{ sumWhite += $5; sumBlack += $6 } END { if (NR > 0) print "Average estimate after move 20 by player..."; print " White: " (sumWhite / NR); print " Black: " sumBlack / NR }'
Average estimate after move 20 by player...
 White: 0.36689
 Black: -0.389409
````

### Future ideas of pre-processing and other variables

One idea would be to incorporate a chess engine's evaluation (e.g. the open source chess engine [Stockfish](
https://stockfishchess.org)), fixed to a certain ply depth count. This would prevent biases implemented with 
crude estimates such as our piece counting.


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
