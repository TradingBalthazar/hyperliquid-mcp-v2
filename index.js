#!/usr/bin/env node

const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const open = require('open');
require('dotenv').config();

// Create Express app
const app = express();
const PORT = process.env.PORT || 3456; // Use a different port than 3000 to avoid conflicts

// Enable CORS
app.use(cors());

// Parse JSON request body
app.use(express.json());

// Serve the dashboard HTML file
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'dashboard.html'));
});

// API routes
app.post('/api/authenticate', (req, res) => {
  const { secretKey, accountAddress, network } = req.body;
  
  if (!secretKey) {
    return res.status(400).json({ error: 'Secret key is required' });
  }
  
  // Save the credentials to the .env file
  const envContent = `HYPERLIQUID_SECRET_KEY=${secretKey}
HYPERLIQUID_ACCOUNT_ADDRESS=${accountAddress || ''}
HYPERLIQUID_NETWORK=${network || 'mainnet'}
`;
  
  fs.writeFileSync(path.join(__dirname, '.env'), envContent);
  
  // Configure the MCP server
  const configScript = spawn('node', [path.join(__dirname, 'configure-mcp.js')]);
  
  configScript.on('close', (code) => {
    if (code === 0) {
      res.json({ success: true, message: 'Authentication successful' });
    } else {
      res.status(500).json({ error: 'Failed to configure MCP server' });
    }
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  console.log('Opening web dashboard in your browser...');
  
  // Open the web dashboard in the default browser
  open(`http://localhost:${PORT}`);
});

// Start the MCP server if credentials are available
if (process.env.HYPERLIQUID_SECRET_KEY) {
  console.log('Starting Hyperliquid MCP server...');
  
  const mcpServer = spawn('python3', [path.join(__dirname, 'hyperliquid_bridge.py')], {
    env: {
      ...process.env,
      HYPERLIQUID_SECRET_KEY: process.env.HYPERLIQUID_SECRET_KEY,
      HYPERLIQUID_ACCOUNT_ADDRESS: process.env.HYPERLIQUID_ACCOUNT_ADDRESS || '',
      HYPERLIQUID_NETWORK: process.env.HYPERLIQUID_NETWORK || 'mainnet'
    }
  });
  
  mcpServer.stdout.on('data', (data) => {
    console.log(`MCP server: ${data}`);
  });
  
  mcpServer.stderr.on('data', (data) => {
    console.error(`MCP server error: ${data}`);
  });
  
  mcpServer.on('close', (code) => {
    console.log(`MCP server exited with code ${code}`);
  });
}

// Handle process termination
process.on('SIGINT', () => {
  console.log('Shutting down...');
  process.exit(0);
});