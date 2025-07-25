# Stats scripts

These are Python scripts that collect various stats and add them to a database.


## Installation

```shell
git clone https://github.com/NaturalHistoryMuseum/daily-stats.git
cd daily-stats
pip install .
```

Configuration is via environment variables or an `.env` file. The available variables are listed in `template.env`.


## Usage

The `stats` scripts can be run individually as a Python script, e.g.:

```shell
python daily_stats/stats/alma_contents.py
```

Or via the CLI, e.g.:

```shell
daily-stats alma-contents
```
