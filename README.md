# cn_treasury_curve

treasury curve of china (collectiing data from chinabond.com.cn)

## Installation

```bash
pip install cn-treasury_curve
```

## Usage

```bash
Usage: cn-treasury-curve [OPTIONS] PATH_TO_SAVE

  Save china treasury curve data to file

Options:
  -f, --fileformat TEXT  zipline (default) - zipline style file , all - dump
                         all file
  --help                 Show this message and exit.
```

example

```bash
> cn-treasury-curve -f zipline /tmp/treasury-curve.csv
```