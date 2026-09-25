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
Select your agent and desired skills. Alternatively copy whole folders out of this repository into the path your host reads: `.agents/skills/` for Cursor and OpenCode, `.github/skills/` for Copilot, `.cline/skills/` for Cline. All three are generated from `plugins/dreamlayer/skills/` and are byte identical, so pick whichever your host loads. References and scripts must travel with SKILL.md.

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
Full instructions, including the CLI and the `.github/skills/` project path, are in [Copilot setup](copilot-setup.md). Use .vscode/mcp.json; the password input keeps the actual key out of source control:
```json
{"inputs":[{"type":"promptString","id":"dreamlayer-api-key","description":"DreamLayer API key","password":true}],"servers":{"dreamlayer":{"type":"stdio","command":"npx","args":["-y","@dreamlayer/mcp@0.4.0-beta.4"],"env":{"DREAMLAYER_API_KEY":"${input:dreamlayer-api-key}"}}}}
```

## Cline

Skills live in `.cline/skills/` in the project or `~/.cline/skills/` globally, and the MCP
server goes in the CLI settings file that `cline config mcp` prints. Full instructions are in
[Cline setup](cline-setup.md).

```sh
cline skill add TheDesignFounder/dreamlayer-agent-plugin -a cline -s '*'
cline config skills
cline config mcp
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

## Other hosts that read the same files

None of these needs a DreamLayer package of its own. Point the host at a directory this
repository already generates, or copy one folder.

| Host | What to do | Documented path |
| --- | --- | --- |
| Goose | Copy `.agents/skills/` into the project, or into `~/.agents/skills/` for every session | `.agents/skills/<name>/SKILL.md`, its recommended location; `.goose/skills/` and `.claude/skills/` still load |
| Kilo Code | The same copy; Kilo loads the shared directory by default | `.agents/skills/` and `~/.agents/skills/`, or its own `.kilo/skills/` |
| DeepSeek Harness | The same copy; it ranks a project's `.agents/skills` second, after `.dsh/skills` | `.agents/skills/<name>/SKILL.md` or `.dsh/skills/<name>/SKILL.md` |
| Qwen Code | Copy into `.qwen/skills/`; it reads no shared directory | `.qwen/skills/<name>/SKILL.md` or `~/.qwen/skills/` |
| Aider | No skill loading. Use a conventions file and read it in | `CONVENTIONS.md` through `--read` |
| Continue | No skill loading. Its rules are always on rather than loaded on demand | `.continue/rules/` |

```sh
cp -R dreamlayer-agent-plugin/.agents/skills/. your-project/.agents/skills/
cp -R dreamlayer-agent-plugin/.agents/skills/. your-project/.qwen/skills/
```

Each host still needs the MCP server configured its own way, with the key supplied through
that host's own secret settings. Checked on September 25, 2026 against each host's own
documentation. None of these six was run here, unlike the hosts in the
[validation record](validation.md).

## Verify
List tools and read capabilities and balance. These spend nothing. Confirm sprite_sheet is advertised. A stale installed MCP may fail while the current beta works: update and restart the process. Stable 0.3.0 does not support this full workflow.

Sources: [Cursor](https://cursor.com/docs/context/skills), [OpenCode](https://opencode.ai/docs/skills/), [Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills), [VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers), [Cline](https://docs.cline.bot/features/skills), [Goose](https://goose-docs.ai/docs/guides/context-engineering/using-skills/), [Kilo Code](https://kilo.ai/docs/customize/skills), [Qwen Code](https://qwenlm.github.io/qwen-code-docs/en/users/features/skills/), [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md), [Gemini](https://geminicli.com/docs/cli/skills/), [Codex](https://developers.openai.com/plugins/build/plugins).
