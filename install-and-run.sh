#!/bin/bash

echo "=== Hyperliquid MCP Installation and Setup ==="
echo "This script will install and set up the Hyperliquid MCP server for HL Coder."

# Create a directory for the Hyperliquid MCP
echo "Creating directory..."
mkdir -p hyperliquid-mcp
cd hyperliquid-mcp

# Create package.json directly
echo "Creating package.json..."
cat > package.json << 'EOL'
{
  "name": "hyperliquid-mcp",
  "version": "1.0.0",
  "description": "Hyperliquid MCP Server for HL Coder",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "author": "TradingBalthazar",
  "license": "MIT",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.1.0",
    "cors": "^2.8.5",
    "dotenv": "^16.4.5",
    "express": "^4.19.2",
    "open": "^10.1.0",
    "python-shell": "^5.0.0"
  }
}
EOL

# Download other files
echo "Downloading necessary files..."
curl -s https://raw.githubusercontent.com/TradingBalthazar/hyperliquid-mcp-v2/master/index.js -o index.js
curl -s https://raw.githubusercontent.com/TradingBalthazar/hyperliquid-mcp-v2/master/hyperliquid_bridge.py -o hyperliquid_bridge.py
curl -s https://raw.githubusercontent.com/TradingBalthazar/hyperliquid-mcp-v2/master/configure-mcp.js -o configure-mcp.js
curl -s https://raw.githubusercontent.com/TradingBalthazar/hyperliquid-mcp-v2/master/dashboard.html -o dashboard.html

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