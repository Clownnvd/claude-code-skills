# MCP (Model Context Protocol)

> Source: https://nextjs.org/docs/app/guides/mcp (v16.1.6)

Next.js 16+ includes MCP support via a built-in endpoint at `/_next/mcp`, enabling AI coding agents to access your application's internals in real-time during development.

## Setup

**Requirement:** Next.js 16+

Add `next-devtools-mcp` to `.mcp.json` at project root:

```json
{
  "mcpServers": {
    "next-devtools": {
      "command": "npx",
      "args": ["-y", "next-devtools-mcp@latest"]
    }
  }
}
```

Start dev server normally -- `next-devtools-mcp` auto-discovers the running instance.

## Available Tools

| Tool | Description |
|------|-------------|
| `get_errors` | Retrieve build errors, runtime errors, and type errors from dev server |
| `get_logs` | Get path to dev log file (browser console + server output) |
| `get_page_metadata` | Get metadata about specific pages (routes, components, rendering info) |
| `get_project_metadata` | Retrieve project structure, configuration, dev server URL |
| `get_server_action_by_id` | Look up Server Actions by ID to find source file and function name |

## Capabilities

| Category | Features |
|----------|----------|
| Runtime Access | Error detection, live state queries, page metadata, Server Actions, dev logs |
| Dev Tools | Next.js knowledge base, migration/upgrade helpers, cache component guides |
| Browser Testing | Playwright MCP integration for verifying pages |

## Workflow

1. Start dev server: `npm run dev`
2. Coding agent auto-connects via `next-devtools-mcp`
3. Open app in browser to view pages
4. Query agent for insights and diagnostics

## Agent Benefits

- Context-aware suggestions based on existing project structure
- Query live application state (config, routes, middleware)
- Understand app router page/layout hierarchy
- Generate code following project patterns

## Architecture

- Built-in MCP endpoint at `/_next/mcp` within the dev server
- `next-devtools-mcp` discovers and communicates with these endpoints
- Supports multiple Next.js instances on different ports
- Forwards tool calls to appropriate dev server

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Not connecting | Ensure Next.js v16+, verify `.mcp.json` config |
| No response | Start/restart dev server, check agent loaded MCP config |

## Quick Reference

| Item | Detail |
|------|--------|
| Min version | Next.js 16 |
| Config file | `.mcp.json` at project root |
| Package | `next-devtools-mcp` |
| Endpoint | `/_next/mcp` (built into dev server) |
| Protocol | Model Context Protocol (open standard) |
| Auto-discovery | Yes, finds running Next.js instances automatically |
