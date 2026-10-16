# Optional REA investigation

Use Reverse Engineer Anything when a shipped, compiled, or minified artifact helps answer
a bounded behavior question. If readable project source already answers the question,
inspect it directly. DreamLayer is an artwork tool, not a REA analysis provider.

Record origin, version/revision, redistribution permission, SHA-256, and the exact question.
Preserve original bytes and keep analysis Evidence private until sanitized. Distinguish
REA observations, the agent's interpretation, runtime verification, and later source checks.

Relay garden uses a self-authored minified JavaScript target. It is a controlled example,
not a recovered commercial game and not a blind evaluation. REA 6.5.0 locates a Math.hypot
read, its enclosing function, and a caller relation. The agent interprets the artifact's
formula; numeric runtime tests establish the bounded equivalence. REA reports partial
coverage and unresolved facts, which must remain in the account.

```sh
# Inside the example after npm ci; the pinned REA CLI needs no native analysis engine.
npm run investigate
npm test
```

Full local Evidence is written under `.local/`. The public excerpt is not an importable
Evidence record. Read the example's `docs/rea-workflow.md` for exact commands and boundaries.
For REA MCP setup use [REA's official installation guide](https://github.com/morluto/rea/blob/main/docs/installation.md).
Do not claim CLI execution proves MCP registration. Installing this skill registers neither
REA nor DreamLayer. Do not modify upstream REA for the example.
