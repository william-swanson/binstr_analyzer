# Binary String Analyzer

A quick utility to do some simple statistical analysis on a binary string. Currently, there are two tests provided: standard deviations on a normal curve and approximate entropy. These tests aim to help determine if the binary string is normal. The tests can be run individually or together.

## Normal Curve
Example:
`python binstr_analyzer.py normcurve [-p 0.5 -c 1.96] 01010101`

## Approximate Entropy
Basic:
`python binstr_analyzer.py apen [-k 1] 01010101`

A range of values can be specified for k to calculate those values of ApEn(k) as follows:

`python binstr_analyzer.py apen [-k 1:5] 01010101`

The k values can be plotted versus ApEn(k) values by adding the `--show-plt` flag.

`python binstr_analyzer.py apen [-k 1:5 --show-plt] 01010101`

## All
All the additional features from Normal Curve and Approximate Entropy can be used with `all`.

Example:
`python binstr_analyzer.py all [-p 0.5 -c 1.96 -k 1] 01010101`