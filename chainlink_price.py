import requests
from web3 import Web3

CHAINLINK_ABI = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

def load_token_feeds(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[Error] Failed to fetch feed data: {e}")
        return

    feeds = response.json()
    filtered = {}

    for feed in feeds:
        name = feed.get("name", "")
        proxy = feed.get("proxyAddress")
        docs = feed.get("docs", {})
        base = docs.get("baseAsset", "")
        quote = docs.get("quoteAsset", "")

        if name.endswith(" / USD") and proxy and quote.upper() == "USD":
            symbol = base.upper()
            filtered[symbol] = proxy

    return filtered


def get_price_by_symbol_at_block(rpc_url: str, token_feeds: dict, token_symbol: str, block_number: int) -> float:
    token_symbol = token_symbol.upper()
    if token_symbol not in token_feeds:
        raise ValueError(f"Token '{token_symbol}' not found in oracle dictionary.")

    web3 = Web3(Web3.HTTPProvider(rpc_url))
    contract = web3.eth.contract(address=token_feeds[token_symbol], abi=CHAINLINK_ABI)

    try:
        data_at_block = contract.functions.latestRoundData().call(block_identifier=block_number)
        decimals = contract.functions.decimals().call()
        return data_at_block[1] / (10 ** decimals)
    except Exception as e:
        print(f"[Error] Failed to get price for token '{token_symbol}' at block {block_number}: {e}")
        return None