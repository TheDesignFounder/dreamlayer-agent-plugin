import {readFileSync,writeFileSync} from 'node:fs';
import {Client} from '/Users/user/dreamlayer-readiness-polish-20260923/mcp-install/node_modules/@modelcontextprotocol/sdk/dist/esm/client/index.js';
import {StdioClientTransport} from '/Users/user/dreamlayer-readiness-polish-20260923/mcp-install/node_modules/@modelcontextprotocol/sdk/dist/esm/client/stdio.js';
const entry = process.argv[2];
const transport = new StdioClientTransport({command:process.execPath,args:[entry],env:{...process.env,DREAMLAYER_API_KEY:readFileSync('/Users/user/.config/dreamlayer/api-key','utf8').trim()}});
const client=new Client({name:'dreamlayer-smithery-card-audit',version:'1.0.0'});
await client.connect(transport);
try {
  const info = client.getServerVersion();
  const res = await client.listTools();
  const out = {retrieved_at:new Date().toISOString(), entry, serverInfo: info, tools: res.tools};
  writeFileSync(process.argv[3], JSON.stringify(out,null,2));
  console.log('serverInfo', JSON.stringify(info), 'tools', res.tools.length);
  for (const t of res.tools) {
    const props = (t.inputSchema && t.inputSchema.properties) || {};
    const undesc = Object.entries(props).filter(([k,v]) => !(v && v.description)).map(([k]) => k);
    console.log(`- ${t.name}: title=${JSON.stringify(t.title??null)} desc=${(t.description||'').length}ch params=${Object.keys(props).length} undescribed=[${undesc.join(',')}] outputSchema=${!!t.outputSchema} annotations=${JSON.stringify(t.annotations??null)}`);
  }
} finally { await client.close(); }
