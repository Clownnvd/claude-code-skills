# Debugging

> Source: https://nextjs.org/docs/app/guides/debugging (v16.1.6)

## VS Code Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js: debug server-side",
      "type": "node-terminal",
      "request": "launch",
      "command": "npm run dev -- --inspect"
    },
    {
      "name": "Next.js: debug client-side",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000"
    },
    {
      "name": "Next.js: debug full stack",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/next/dist/bin/next",
      "runtimeArgs": ["--inspect"],
      "skipFiles": ["<node_internals>/**"],
      "serverReadyAction": {
        "action": "debugWithEdge",
        "killOnServerStop": true,
        "pattern": "- Local:.+(https?://.+)",
        "uriFormat": "%s",
        "webRoot": "${workspaceFolder}"
      }
    }
  ]
}
```

| Config | Debugs | Browser |
|---|---|---|
| `debug server-side` | Server code | None |
| `debug client-side` | Client code | Chrome |
| `debug full stack` | Both | Edge (change to `debugWithChrome` for Chrome) |

For monorepos (Turborepo), add `"cwd": "${workspaceFolder}/apps/web"` to server/full-stack configs.

## Browser DevTools

### Client-Side

1. Run `next dev`
2. Open DevTools (`Ctrl+Shift+J` / `Cmd+Option+I`)
3. Go to **Sources** tab
4. Use `debugger` statements or `Ctrl+P` to find files (paths start with `webpack://_N_E/./`)

### Server-Side

1. Start with inspect flag:
   ```bash
   npm run dev -- --inspect
   ```
2. Open `chrome://inspect` (Chrome) or `about:debugging` (Firefox)
3. Find your Next.js app under **Remote Target** and click **Inspect**
4. Source paths: `webpack://{app-name}/./`

| Flag | Purpose |
|---|---|
| `--inspect` | Enable debugger on default port 9229 |
| `--inspect=0.0.0.0` | Allow remote debugging (e.g., Docker) |
| `NODE_OPTIONS=--inspect-brk` | Break before user code runs |
| `NODE_OPTIONS=--inspect-wait` | Wait for debugger to attach |

## JetBrains WebStorm

1. Edit Configurations > add **JavaScript Debug**
2. Set URL to `http://localhost:3000`
3. Run both the Node app and browser debug configs

## Error Overlay Inspector

Click the **Node.js icon** below the Next.js version in the error overlay to copy the DevTools URL for inspecting server errors.

## Windows Note

Disable **Windows Defender** real-time scanning -- it checks every file read and significantly slows Fast Refresh.

## Quick Reference

| Task | How |
|---|---|
| Debug server in VS Code | `node-terminal` launch config with `--inspect` |
| Debug client in VS Code | `chrome` launch config to `localhost:3000` |
| Debug full stack | `node` launch with `serverReadyAction` |
| Server debug via browser | `npm run dev -- --inspect` then `chrome://inspect` |
| Set breakpoint in code | Add `debugger` statement |
| Find source files | `Ctrl+P`, search `webpack://_N_E/` |
| Remote debug (Docker) | `--inspect=0.0.0.0` |
| React components | Install React Developer Tools browser extension |
