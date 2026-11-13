// MCP server: lets Claude (Claude Desktop, Claude Code, or claude.ai as a custom connector) run the platform
// with the same tools TARS uses. Pair it with Gmail / Google Calendar connectors in Claude if you like.
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { ListToolsRequestSchema, CallToolRequestSchema } = require('@modelcontextprotocol/sdk/types.js');
const { tools, runTool, SYSTEM } = require('./tars');

const INSTRUCTIONS = SYSTEM.replace('You are TARS, the assistant inside', 'These tools run').concat(
  '\n- If the user also has a Google Calendar connector, you can add booked appointments to their calendar; the platform also publishes its own calendar feed.');

const READ_ONLY = new Set(['daily_list', 'scoreboard', 'search_customers', 'get_customer', 'stock_lookup', 'list_appointments']);

function createMcpServer() {
  const server = new Server({ name: 'dealer-autopilot', version: '1.0.0' }, { capabilities: { tools: {} }, instructions: INSTRUCTIONS });
  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: tools.map((t) => ({
      name: t.name, description: t.description, inputSchema: t.input_schema,
      annotations: { readOnlyHint: READ_ONLY.has(t.name), destructiveHint: false, openWorldHint: t.name === 'complete_task' },
    })),
  }));
  server.setRequestHandler(CallToolRequestSchema, async (req) => {
    try {
      const out = await runTool(req.params.name, req.params.arguments || {});
      return { content: [{ type: 'text', text: JSON.stringify(out, null, 1) }], isError: !!(out && out.error) };
    } catch (err) {
      return { content: [{ type: 'text', text: 'Error: ' + err.message }], isError: true };
    }
  });
  return server;
}

module.exports = { createMcpServer };
