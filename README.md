# audiotrans-transform-istft

[![License](https://img.shields.io/pypi/l/audiotrans-transform-istft.svg?style=flat-square)](https://github.com/keik/audiotrans-transform-istft/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/audiotrans-transform-istft.svg?style=flat-square)](https://pypi.python.org/pypi/audiotrans-transform-istft)
[![PyPI](https://img.shields.io/pypi/v/audiotrans-transform-istft.svg?style=flat-square)](https://pypi.python.org/pypi/audiotrans-transform-istft)
[![Travis CI](https://img.shields.io/travis/keik/audiotrans-transform-istft.svg?style=flat-square)](https://travis-ci.org/keik/audiotrans-transform-istft)
[![Coverage Status](https://img.shields.io/coveralls/keik/audiotrans-transform-istft.svg?style=flat-square)](https://coveralls.io/github/keik/audiotrans-transform-istft)

[audiotrans](https://github.com/keik/audiotrans) transform module to Inverse Short-Time Fourier Transformation (ISTFT)


## Installation

```
pip install audiotrans-transform-istft
```


## Usage

As `audiotrans` transform module, like

```
audiotrans <filepath> -t istft -v -c freq
```

Options of the below is available through subarg (like `[ foo -h ]`)

```
usage: istft [-h] [-v] [-H HOP_SIZE]

audiotrans transform module for Short-Time Fourier Transformation (ISTFT)

Transform wave array as np.ndarray shaped (1,) to ISTFT matrix as
np.ndarray shaped (1 + widnow_size/2, (len(wave) - window_size) / hop-size + 1).

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Run as verbose mode
  -H HOP_SIZE, --hop-size HOP_SIZE
                        Hop size to FFT. Default is 256
```


## Test

```
make test
```


## License

MIT (c) keik
