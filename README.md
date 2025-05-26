# Chainlink Token Price

A simple Python utility to fetch token prices using Chainlink oracle contracts at specific block numbers.

## Features

- Works with any EVM-compatible RPC
- Uses Chainlink price feeds
- Supports dynamic token feed loading from JSON

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```
python main.py [-h] --block BLOCK --token TOKEN                                                                                                                                                                                                Fetch token price at a specific block using Chainlink oracle.                                                                                                                                                                                   options:                                                                                                                  -h, --help     show this help message and exit                                                                          --block BLOCK  Block number to query.                                                                                   --token TOKEN  Token symbol (e.g., ETH, BTC).  
```

## License

MIT