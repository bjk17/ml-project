# Chess games using data with move times

Source data[1] is obtained from the Free Internet Chess Server (FICS). We chose *Standard* games (meaning time 
limits are in the order of tens of minutes per game) from reasonable strong players (average rating per match >2000).
We're caching it on a private server to save FICS some valuable bandwith.

[1]: https://www.ficsgames.org/download.html

## Development

Make sure you've downloaded and unzipped the whole content of <https://misc.bjk.is/ml/games> to `games/` folder in 
this repo. Also install the Python packages via pip (preferable using virtualenv):

```bash
> virtualenv venv
> sourve venv/bin/activate
> (venv) pip install -r requirements.txt
```

Run the unittests with

```bash
python -m unittest discover -s test/ -t test/
```
