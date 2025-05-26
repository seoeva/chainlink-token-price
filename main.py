import argparse
import os
from dotenv import load_dotenv
from chainlink_price import load_token_feeds, get_price_by_symbol_at_block

def main():
    # Load RPC and feed URLs from .env file
    load_dotenv()

    rpc_url = os.getenv("RPC_URL")
    feed_url = os.getenv("FEED_URL")

    if not rpc_url or not feed_url:
        print("[Error] RPC_URL or FEED_URL not found in .env file.")
        return

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fetch token price at a specific block using Chainlink oracle.")
    parser.add_argument("--block", type=int, required=True, help="Block number to query.")
    parser.add_argument("--token", type=str, required=True, help="Token symbol (e.g., ETH, BTC).")

    args = parser.parse_args()

    # Load token feed mapping and fetch the price
    token_feeds = load_token_feeds(feed_url)
    price = get_price_by_symbol_at_block(rpc_url, token_feeds, args.token, args.block)

    if price is not None:
        print(f"{args.token.upper()} price at block {args.block}: {price}")
    else:
        print("Failed to retrieve price.")

if __name__ == "__main__":
    main()
