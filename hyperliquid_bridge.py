#!/usr/bin/env python3

import argparse
import json
import sys
import os
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants

# Get environment variables
SECRET_KEY = os.environ.get('HYPERLIQUID_SECRET_KEY')
ACCOUNT_ADDRESS = os.environ.get('HYPERLIQUID_ACCOUNT_ADDRESS')
NETWORK = os.environ.get('HYPERLIQUID_NETWORK', 'mainnet')

if not SECRET_KEY:
    print(json.dumps({"error": "HYPERLIQUID_SECRET_KEY environment variable is required"}))
    sys.exit(1)

# Initialize the exchange
base_url = constants.MAINNET_API_URL if NETWORK == 'mainnet' else constants.TESTNET_API_URL
exchange = Exchange(
    base_url=base_url,
    private_key=SECRET_KEY,
    wallet_address=ACCOUNT_ADDRESS
)

def handle_mcp_request():
    # Read the request from stdin
    request_json = sys.stdin.readline().strip()
    request = json.loads(request_json)
    
    # Handle different request types
    if request['type'] == 'list_tools':
        handle_list_tools()
    elif request['type'] == 'call_tool':
        handle_call_tool(request['params'])
    elif request['type'] == 'list_resources':
        handle_list_resources()
    elif request['type'] == 'list_resource_templates':
        handle_list_resource_templates()
    elif request['type'] == 'read_resource':
        handle_read_resource(request['params'])
    else:
        send_error(f"Unknown request type: {request['type']}")

def handle_list_tools():
    tools = [
        {
            "name": "get_market_data",
            "description": "Get market data from Hyperliquid",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "dataType": {
                        "type": "string",
                        "description": "Type of market data to retrieve",
                        "enum": [
                            "all_mids",
                            "l2_snapshot",
                            "meta",
                            "meta_and_asset_ctxs",
                            "spot_meta",
                            "spot_meta_and_asset_ctxs",
                            "candles",
                            "funding_history"
                        ]
                    },
                    "coin": {
                        "type": "string",
                        "description": "Coin symbol (required for l2_snapshot, candles, funding_history)"
                    },
                    "interval": {
                        "type": "string",
                        "description": "Candle interval (required for candles)"
                    },
                    "startTime": {
                        "type": "integer",
                        "description": "Start time in milliseconds (required for candles, funding_history)"
                    },
                    "endTime": {
                        "type": "integer",
                        "description": "End time in milliseconds (optional for candles, funding_history)"
                    }
                },
                "required": ["dataType"]
            }
        },
        {
            "name": "get_user_data",
            "description": "Get user-specific data from Hyperliquid",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "dataType": {
                        "type": "string",
                        "description": "Type of user data to retrieve",
                        "enum": [
                            "user_state",
                            "spot_user_state",
                            "open_orders",
                            "frontend_open_orders",
                            "user_fills",
                            "user_fills_by_time",
                            "user_funding_history",
                            "user_fees",
                            "user_staking_summary",
                            "user_staking_delegations",
                            "user_staking_rewards",
                            "query_sub_accounts"
                        ]
                    },
                    "startTime": {
                        "type": "integer",
                        "description": "Start time in milliseconds (required for user_fills_by_time, user_funding_history)"
                    },
                    "endTime": {
                        "type": "integer",
                        "description": "End time in milliseconds (optional for user_fills_by_time, user_funding_history)"
                    }
                },
                "required": ["dataType"]
            }
        },
        {
            "name": "place_limit_order",
            "description": "Place a limit order on Hyperliquid",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "coin": {
                        "type": "string",
                        "description": "Coin symbol"
                    },
                    "isBuy": {
                        "type": "boolean",
                        "description": "Whether the order is a buy"
                    },
                    "size": {
                        "type": "number",
                        "description": "Order size"
                    },
                    "price": {
                        "type": "number",
                        "description": "Order price"
                    },
                    "timeInForce": {
                        "type": "string",
                        "description": "Time in force",
                        "enum": ["Gtc", "Ioc", "Alo"]
                    },
                    "reduceOnly": {
                        "type": "boolean",
                        "description": "Whether the order is reduce-only"
                    },
                    "clientOrderId": {
                        "type": "string",
                        "description": "Client order ID"
                    }
                },
                "required": ["coin", "isBuy", "size", "price", "timeInForce"]
            }
        },
        {
            "name": "place_market_order",
            "description": "Place a market order on Hyperliquid",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "coin": {
                        "type": "string",
                        "description": "Coin symbol"
                    },
                    "isBuy": {
                        "type": "boolean",
                        "description": "Whether the order is a buy"
                    },
                    "size": {
                        "type": "number",
                        "description": "Order size"
                    },
                    "slippage": {
                        "type": "number",
                        "description": "Slippage tolerance (default: 0.05)"
                    },
                    "clientOrderId": {
                        "type": "string",
                        "description": "Client order ID"
                    }
                },
                "required": ["coin", "isBuy", "size"]
            }
        },
        {
            "name": "cancel_order",
            "description": "Cancel an order on Hyperliquid",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "coin": {
                        "type": "string",
                        "description": "Coin symbol"
                    },
                    "orderId": {
                        "type": "integer",
                        "description": "Order ID"
                    },
                    "clientOrderId": {
                        "type": "string",
                        "description": "Client order ID"
                    }
                },
                "required": ["coin"],
                "oneOf": [
                    { "required": ["orderId"] },
                    { "required": ["clientOrderId"] }
                ]
            }
        },
        {
            "name": "update_leverage",
            "description": "Update leverage for a coin",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "coin": {
                        "type": "string",
                        "description": "Coin symbol"
                    },
                    "leverage": {
                        "type": "integer",
                        "description": "Leverage value"
                    },
                    "isCross": {
                        "type": "boolean",
                        "description": "Whether to use cross margin (default: true)"
                    }
                },
                "required": ["coin", "leverage"]
            }
        }
    ]
    
    send_response({"tools": tools})

def handle_call_tool(params):
    name = params['name']
    args = params['arguments']
    
    try:
        result = None
        
        if name == 'get_market_data':
            result = handle_market_data(args)
        elif name == 'get_user_data':
            result = handle_user_data(args)
        elif name == 'place_limit_order':
            result = handle_place_limit_order(args)
        elif name == 'place_market_order':
            result = handle_place_market_order(args)
        elif name == 'cancel_order':
            result = handle_cancel_order(args)
        elif name == 'update_leverage':
            result = handle_update_leverage(args)
        else:
            send_error(f"Unknown tool: {name}")
            return
        
        if 'error' in result:
            send_error(result['error'])
        else:
            send_tool_response(result)
    except Exception as e:
        send_error(str(e))

def handle_market_data(args):
    data_type = args.get('dataType')
    
    if data_type == 'all_mids':
        return exchange.get_all_mids()
    elif data_type == 'l2_snapshot':
        coin = args.get('coin')
        if not coin:
            return {'error': 'Coin is required for L2 snapshot'}
        return exchange.get_l2_snapshot(coin)
    elif data_type == 'meta':
        return exchange.get_meta()
    elif data_type == 'meta_and_asset_ctxs':
        return exchange.get_meta_and_asset_ctxs()
    elif data_type == 'spot_meta':
        return exchange.get_spot_meta()
    elif data_type == 'spot_meta_and_asset_ctxs':
        return exchange.get_spot_meta_and_asset_ctxs()
    elif data_type == 'candles':
        coin = args.get('coin')
        interval = args.get('interval')
        start_time = args.get('startTime')
        end_time = args.get('endTime')
        
        if not coin or not interval or not start_time:
            return {'error': 'Coin, interval, and startTime are required for candles'}
        
        return exchange.get_candles(
            coin=coin,
            interval=interval,
            start_time=start_time,
            end_time=end_time
        )
    elif data_type == 'funding_history':
        coin = args.get('coin')
        start_time = args.get('startTime')
        end_time = args.get('endTime')
        
        if not coin or not start_time:
            return {'error': 'Coin and startTime are required for funding history'}
        
        return exchange.get_funding_history(
            coin=coin,
            start_time=start_time,
            end_time=end_time
        )
    else:
        return {'error': f'Unknown data type: {data_type}'}

def handle_user_data(args):
    data_type = args.get('dataType')
    
    if data_type == 'user_state':
        return exchange.get_user_state()
    elif data_type == 'spot_user_state':
        return exchange.get_spot_user_state()
    elif data_type == 'open_orders':
        return exchange.get_open_orders()
    elif data_type == 'frontend_open_orders':
        return exchange.get_frontend_open_orders()
    elif data_type == 'user_fills':
        return exchange.get_user_fills()
    elif data_type == 'user_fills_by_time':
        start_time = args.get('startTime')
        end_time = args.get('endTime')
        
        if not start_time:
            return {'error': 'startTime is required for user fills by time'}
        
        return exchange.get_user_fills_by_time(
            start_time=start_time,
            end_time=end_time
        )
    elif data_type == 'user_funding_history':
        start_time = args.get('startTime')
        end_time = args.get('endTime')
        
        if not start_time:
            return {'error': 'startTime is required for user funding history'}
        
        return exchange.get_user_funding_history(
            start_time=start_time,
            end_time=end_time
        )
    elif data_type == 'user_fees':
        return exchange.get_user_fees()
    elif data_type == 'user_staking_summary':
        return exchange.get_user_staking_summary()
    elif data_type == 'user_staking_delegations':
        return exchange.get_user_staking_delegations()
    elif data_type == 'user_staking_rewards':
        return exchange.get_user_staking_rewards()
    elif data_type == 'query_sub_accounts':
        return exchange.query_sub_accounts()
    else:
        return {'error': f'Unknown data type: {data_type}'}

def handle_place_limit_order(args):
    coin = args.get('coin')
    is_buy = args.get('isBuy')
    size = args.get('size')
    price = args.get('price')
    time_in_force = args.get('timeInForce')
    reduce_only = args.get('reduceOnly', False)
    client_order_id = args.get('clientOrderId')
    
    if not coin or is_buy is None or size is None or price is None or not time_in_force:
        return {'error': 'Coin, isBuy, size, price, and timeInForce are required for placing a limit order'}
    
    order_type = {
        'limit': {
            'tif': time_in_force
        }
    }
    
    return exchange.place_order(
        coin=coin,
        is_buy=is_buy,
        sz=size,
        limit_px=price,
        order_type=order_type,
        reduce_only=reduce_only,
        cloid=client_order_id
    )

def handle_place_market_order(args):
    coin = args.get('coin')
    is_buy = args.get('isBuy')
    size = args.get('size')
    slippage = args.get('slippage', 0.05)
    client_order_id = args.get('clientOrderId')
    
    if not coin or is_buy is None or size is None:
        return {'error': 'Coin, isBuy, and size are required for market orders'}
    
    return exchange.market_order(
        coin=coin,
        is_buy=is_buy,
        sz=size,
        slippage=slippage,
        cloid=client_order_id
    )

def handle_cancel_order(args):
    coin = args.get('coin')
    order_id = args.get('orderId')
    client_order_id = args.get('clientOrderId')
    
    if not coin or (order_id is None and not client_order_id):
        return {'error': 'Coin and either orderId or clientOrderId are required for canceling an order'}
    
    return exchange.cancel_order(
        coin=coin,
        oid=order_id,
        cloid=client_order_id
    )

def handle_update_leverage(args):
    coin = args.get('coin')
    leverage = args.get('leverage')
    is_cross = args.get('isCross', True)
    
    if not coin or leverage is None:
        return {'error': 'Coin and leverage are required for updating leverage'}
    
    return exchange.update_leverage(
        coin=coin,
        leverage=leverage,
        is_cross=is_cross
    )

def handle_list_resources():
    resources = [
        {
            "uri": "hyperliquid://market/all-mids",
            "name": "Current mid prices for all coins",
            "mimeType": "application/json",
            "description": "Real-time mid prices for all actively traded coins on Hyperliquid"
        }
    ]
    
    send_response({"resources": resources})

def handle_list_resource_templates():
    resource_templates = [
        {
            "uriTemplate": "hyperliquid://market/l2-book/{coin}",
            "name": "L2 order book for a specific coin",
            "mimeType": "application/json",
            "description": "Order book data for a specific coin on Hyperliquid"
        },
        {
            "uriTemplate": "hyperliquid://user/{address}/state",
            "name": "User state for a specific address",
            "mimeType": "application/json",
            "description": "Trading details about a user including positions, margin, and account value"
        },
        {
            "uriTemplate": "hyperliquid://user/{address}/open-orders",
            "name": "Open orders for a specific address",
            "mimeType": "application/json",
            "description": "List of open orders for a specific user"
        }
    ]
    
    send_response({"resourceTemplates": resource_templates})

def handle_read_resource(params):
    uri = params['uri']
    
    # Match for all-mids resource
    if uri == 'hyperliquid://market/all-mids':
        data = exchange.get_all_mids()
        send_resource_response(uri, data)
        return
    
    # Match for L2 order book resource
    l2_book_match = uri.startswith('hyperliquid://market/l2-book/')
    if l2_book_match:
        coin = uri.split('/')[-1]
        data = exchange.get_l2_snapshot(coin)
        send_resource_response(uri, data)
        return
    
    # Match for user state resource
    user_state_match = uri.endswith('/state')
    if user_state_match:
        data = exchange.get_user_state()
        send_resource_response(uri, data)
        return
    
    # Match for user open orders resource
    open_orders_match = uri.endswith('/open-orders')
    if open_orders_match:
        data = exchange.get_open_orders()
        send_resource_response(uri, data)
        return
    
    send_error(f"Invalid URI format: {uri}")

def send_response(data):
    print(json.dumps(data))
    sys.stdout.flush()

def send_error(message):
    error_response = {
        "content": [
            {
                "type": "text",
                "text": f"Error: {message}"
            }
        ],
        "isError": True
    }
    print(json.dumps(error_response))
    sys.stdout.flush()

def send_tool_response(data):
    response = {
        "content": [
            {
                "type": "text",
                "text": json.dumps(data, indent=2)
            }
        ]
    }
    print(json.dumps(response))
    sys.stdout.flush()

def send_resource_response(uri, data):
    response = {
        "contents": [
            {
                "uri": uri,
                "mimeType": "application/json",
                "text": json.dumps(data, indent=2)
            }
        ]
    }
    print(json.dumps(response))
    sys.stdout.flush()

if __name__ == '__main__':
    while True:
        try:
            handle_mcp_request()
        except Exception as e:
            send_error(f"Unexpected error: {str(e)}")