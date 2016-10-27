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

## Notice

    every body need to update the new data every day,
    if you wanna cal this function multi-time intra-day, you should cache it your self
    Data are combined with 2 parts

    1. the xlsx files inside the package
    2. newly fetched data those not in the package, we will fetch them on the fly