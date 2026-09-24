# Distribution bundles

The MCPB package contains the published beta.3 MCP server and its dependencies. It is a local stdio package; it does not create a remote HTTP MCP service.

```sh
cd packaging/mcpb
npm ci --ignore-scripts
npx @anthropic-ai/mcpb validate manifest.json
npx @anthropic-ai/mcpb pack . ../../dist/dreamlayer.mcpb
```

Provide the API key through the installer's sensitive user configuration. It is never embedded in the bundle. The server uploads only files explicitly selected for image operations and writes only explicitly chosen result paths. Standard image work and sprite work consume credits; see live capabilities and balance before generating.

For Smithery, sign in and use its Local/MCPB publish route. A public REST URL is not a Streamable HTTP MCP endpoint and must not be submitted as one.
