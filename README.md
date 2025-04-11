# Hyperliquid MCP for HL Coder

This repository contains a Model Context Protocol (MCP) server for Hyperliquid that integrates with HL Coder. It allows you to interact with Hyperliquid through natural language in HL Coder.

## Quick Start

To install and run the Hyperliquid MCP server, simply run the following command in HL Coder:

```bash
curl -s https://raw.githubusercontent.com/TradingBalthazar/hyperliquid-mcp-v2/main/install-and-run.sh | bash
```

This will:
1. Download and install the necessary files
2. Install the required dependencies
3. Start the Hyperliquid MCP server
4. Open a dashboard in your browser to enter your credentials

## Features

- Connect to Hyperliquid using your secret key
- Get market data (prices, order books, etc.)
- Get user data (positions, account value, etc.)
- Place and cancel orders
- Update leverage

## Setup

1. Run the installation command in HL Coder
2. When the dashboard opens in your browser, enter your Hyperliquid secret key
3. (Optional) Enter your Ethereum account address
4. Select the network (mainnet or testnet)
5. Click "Connect to Hyperliquid"

## Example Commands

Once connected, you can use natural language to interact with Hyperliquid in HL Coder. Here are some examples:

- "Get current market prices for all coins"
- "Show my current positions and account value"
- "Place a limit buy order for 0.1 BTC at $60,000"
- "Cancel all my open orders for ETH"
- "Update my leverage for BTC to 5x"

## Available Tools

The Hyperliquid MCP server provides the following tools:

### get_market_data

Get market data from Hyperliquid.

Parameters:
- `dataType`: Type of market data to retrieve (all_mids, l2_snapshot, meta, meta_and_asset_ctxs, spot_meta, spot_meta_and_asset_ctxs, candles, funding_history)
- `coin`: Coin symbol (required for l2_snapshot, candles, funding_history)
- `interval`: Candle interval (required for candles)
- `startTime`: Start time in milliseconds (required for candles, funding_history)
- `endTime`: End time in milliseconds (optional for candles, funding_history)

### get_user_data

Get user-specific data from Hyperliquid.

Parameters:
- `dataType`: Type of user data to retrieve (user_state, spot_user_state, open_orders, frontend_open_orders, user_fills, user_fills_by_time, user_funding_history, user_fees, user_staking_summary, user_staking_delegations, user_staking_rewards, query_sub_accounts)
- `startTime`: Start time in milliseconds (required for user_fills_by_time, user_funding_history)
- `endTime`: End time in milliseconds (optional for user_fills_by_time, user_funding_history)

### place_limit_order

Place a limit order on Hyperliquid.

Parameters:
- `coin`: Coin symbol
- `isBuy`: Whether the order is a buy
- `size`: Order size
- `price`: Order price
- `timeInForce`: Time in force (Gtc, Ioc, Alo)
- `reduceOnly`: Whether the order is reduce-only
- `clientOrderId`: Client order ID

### place_market_order

Place a market order on Hyperliquid.

Parameters:
- `coin`: Coin symbol
- `isBuy`: Whether the order is a buy
- `size`: Order size
- `slippage`: Slippage tolerance (default: 0.05)
- `clientOrderId`: Client order ID

### cancel_order

Cancel an order on Hyperliquid.

Parameters:
- `coin`: Coin symbol
- `orderId`: Order ID
- `clientOrderId`: Client order ID

### update_leverage

Update leverage for a coin.

Parameters:
- `coin`: Coin symbol
- `leverage`: Leverage value
- `isCross`: Whether to use cross margin (default: true)

## Available Resources

The Hyperliquid MCP server provides the following resources:

- `hyperliquid://market/all-mids`: Current mid prices for all coins
- `hyperliquid://market/l2-book/{coin}`: L2 order book for a specific coin
- `hyperliquid://user/{address}/state`: User state for a specific address
- `hyperliquid://user/{address}/open-orders`: Open orders for a specific address

## Security

Your secret key is stored locally and is only used to authenticate with Hyperliquid. It is never sent to any third-party servers.

## Requirements

- Node.js 14+
- Python 3.6+
- pip (for installing Python dependencies)

## License

MIT