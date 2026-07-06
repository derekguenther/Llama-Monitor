const { spawn } = require('child_process');
const proc = spawn('node', ['/home/yolo_agent/superpowers-chrome/mcp/dist/index.js', '--headless'], { stdio: ['pipe','pipe','pipe'] });
let id = 1;
const responses = [];
proc.stdout.on('data', d => {
  for (const line of d.toString().trim().split('\n')) {
    if (line.trim()) try { responses.push(JSON.parse(line)); } catch {}
  }
});
proc.stderr.on('data', () => {});
proc.on('error', e => console.error(e.message));
function send(m, p, i) { proc.stdin.write(JSON.stringify({jsonrpc:'2.0',id:i??id++,method:m,params:p||{}})+'\n'); }
setTimeout(() => send('initialize', {protocolVersion:'2024-11-05', capabilities:{tools:{}}, clientInfo:{name:'invoker',version:'1.0'}}, 1), 500);
setTimeout(() => send('tools/call', {name:'use_browser', arguments:{action:'navigate', selector:null, payload:'http://localhost:8080'}}), 3000);
setTimeout(() => send('tools/call', {name:'use_browser', arguments:{action:'eval', selector:null, payload:JSON.stringify({
  format: 'text',
  code: "(function() { var card = document.querySelector('.slot-context-card'); var graphs = document.querySelectorAll('.slot-graph'); var c1 = document.getElementById('slot-progress-graph'); var c2 = document.getElementById('context-used-graph'); var cards = document.querySelectorAll('.card'); var info = { card: { h: (card||{}).offsetHeight, w: (card||{}).offsetWidth, styleH: (card||{}).style.height }, graph1: { h: (graphs[0]||{}).offsetHeight }, graph2: { h: (graphs[1]||{}).offsetHeight }, canvas1: { h: (c1||{}).offsetHeight, w: (c1||{}).offsetWidth, cls: (c1||{}).className, naturalH: (c1||{}).height }, canvas2: { h: (c2||{}).offsetHeight, cls: (c2||{}).className }, serverStatus: (cards[0]||{}).offsetHeight, summary: (cards[1]||{}).offsetHeight, sysResources: (cards[3]||{}).offsetHeight }; var cs = c1 ? getComputedStyle(c1) : null; if (cs) { info.canvas1Computed = { pos: cs.position, h: cs.height, display: cs.display }; } var cs2 = card ? getComputedStyle(card) : null; if (cs2) { info.cardComputed = { display: cs2.display, h: cs2.height }; } return JSON.stringify(info); })()"
}})), 10000);
setTimeout(() => {
  for (const r of responses) {
    if (r.id && r.id >= 3 && r.result && r.result.content) {
      for (const c of r.result.content) {
        if (c.type === 'text') console.log(c.text);
      }
    }
  }
  proc.kill('SIGTERM');
  process.exit(0);
}, 16000);
