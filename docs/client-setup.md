# Client setup

Requires Node.js 22.12 or later. Get a key at https://platform.dreamlayer.io and provide DREAMLAYER_API_KEY to the MCP subprocess. Never commit keys. Installing skills does not configure authentication or grant credits.

## Claude Code plugin
```
/plugin marketplace add TheDesignFounder/dreamlayer-agent-plugin
/plugin install dreamlayer@dreamlayer
```
Set DREAMLAYER_API_KEY in the environment launching Claude Code. Restart after changing it. This is DreamLayer's GitHub marketplace, not the official Anthropic directory.

## Codex plugin
```sh
codex plugin marketplace add https://github.com/TheDesignFounder/dreamlayer-agent-plugin.git
codex plugin add dreamlayer@dreamlayer
```
The repository marketplace packages the same nine skills and pinned MCP. OpenAI public directory review is separate. Set DREAMLAYER_API_KEY in the host environment.

## Portable installation
```sh
npx skills add TheDesignFounder/dreamlayer-agent-plugin --list
npx skills add TheDesignFounder/dreamlayer-agent-plugin
```
Select your agent and desired skills. Alternatively copy whole folders from .agents/skills into your project's .agents/skills. References and scripts must travel with SKILL.md.

## Cursor
Use .cursor/mcp.json with a private key supplied through the client's secret configuration. This placeholder is not a working key:
```json
{"mcpServers":{"dreamlayer":{"command":"npx","args":["-y","@dreamlayer/mcp@0.4.0-beta.4"],"env":{"DREAMLAYER_API_KEY":"YOUR_PRIVATE_API_KEY"}}}}
```

## OpenCode
Use opencode.json:
```json
{"$schema":"https://opencode.ai/config.json","mcp":{"dreamlayer":{"type":"local","command":["npx","-y","@dreamlayer/mcp@0.4.0-beta.4"],"environment":{"DREAMLAYER_API_KEY":"{env:DREAMLAYER_API_KEY}"},"enabled":true}}}
```

## GitHub Copilot in VS Code
Use .vscode/mcp.json; the password input keeps the actual key out of source control:
```json
{"inputs":[{"type":"promptString","id":"dreamlayer-api-key","description":"DreamLayer API key","password":true}],"servers":{"dreamlayer":{"type":"stdio","command":"npx","args":["-y","@dreamlayer/mcp@0.4.0-beta.4"],"env":{"DREAMLAYER_API_KEY":"${input:dreamlayer-api-key}"}}}}
```

## Gemini CLI
Use mcpServers in .gemini/settings.json with command npx and args ["-y","@dreamlayer/mcp@0.4.0-beta.4"]. Supply DREAMLAYER_API_KEY through the process environment or private user settings.

## OpenClaw

Install the published skill, then add the server. The timeout is not optional on a machine
that has never run the package: `npx -y` downloads it first, measured at 13 to 50 seconds
across two clean profiles, while OpenClaw waits 5 seconds by default and reports the server
as failed.

```sh
openclaw skills install @thedesignfounder/dreamlayer-image-workflows
openclaw config set skills.entries.dreamlayer-image-workflows.apiKey YOUR_KEY
openclaw mcp add dreamlayer --command npx --arg "-y" --arg "@dreamlayer/mcp@0.4.0-beta.4" \
  --env "DREAMLAYER_API_KEY=YOUR_KEY" --connect-timeout 90
openclaw mcp probe dreamlayer
```

`mcp probe` should report seven tools. `npm i -g @dreamlayer/mcp@0.4.0-beta.4` beforehand
removes the wait.

## Verify
List tools and read capabilities and balance. These spend nothing. Confirm sprite_sheet is advertised. A stale installed MCP may fail while the current beta works: update and restart the process. Stable 0.3.0 does not support this full workflow.

Sources: [Cursor](https://cursor.com/docs/skills), [OpenCode](https://opencode.ai/docs/mcp-servers/), [Copilot](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills), [VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers), [Gemini](https://geminicli.com/docs/cli/skills/), [Codex](https://developers.openai.com/plugins/build/plugins).
