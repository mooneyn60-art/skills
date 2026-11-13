// Run the MCP server over stdio (for Claude Desktop / Claude Code on the same computer as the database).
// The scheduler does NOT run here - keep `npm start` running for the automated sends.
process.removeAllListeners('warning');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { createMcpServer } = require('./mcp');

createMcpServer().connect(new StdioServerTransport()).catch((e) => {
  console.error(e);
  process.exit(1);
});
