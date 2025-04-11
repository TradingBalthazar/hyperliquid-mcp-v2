#!/bin/bash

echo "=== Hyperliquid MCP Installation and Setup ==="
echo "This script will install and set up the Hyperliquid MCP server for HL Coder."

# Create a directory for the Hyperliquid MCP
echo "Creating directory..."
mkdir -p hyperliquid-mcp
cd hyperliquid-mcp

# Clone the repository
echo "Downloading necessary files..."
curl -s https://raw.githubusercontent.com/TradingBalthazar/hyperliquid-mcp-v2/main/index.js -o index.js
curl -s https://raw.githubusercontent.com/TradingBalthazar/hyperliquid-mcp-v2/main/package.json -o package.json
curl -s https://raw.githubusercontent.com/TradingBalthazar/hyperliquid-mcp-v2/main/hyperliquid_bridge.py -o hyperliquid_bridge.py
curl -s https://raw.githubusercontent.com/TradingBalthazar/hyperliquid-mcp-v2/main/configure-mcp.js -o configure-mcp.js
curl -s https://raw.githubusercontent.com/TradingBalthazar/hyperliquid-mcp-v2/main/dashboard.html -o dashboard.html

# Make scripts executable
chmod +x index.js
chmod +x configure-mcp.js
chmod +x hyperliquid_bridge.py

# Install dependencies
echo "Installing dependencies..."
npm install
pip install hyperliquid-python-sdk

# Create MCP configuration directory
echo "Configuring MCP server..."
mkdir -p ~/.local/share/code-server/User/globalStorage/rooveterinaryinc.roo-cline/settings

# Start the server
echo "Starting Hyperliquid MCP server..."
node index.js