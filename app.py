from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Protocol Visualizer Dashboard")

class Action(BaseModel):
    mode: str
    url: str = ""
    to: str = ""
    subject: str = ""
    body: str = ""
    quality: str = "1080p"
    action: str = ""

@app.get("/", response_class=HTMLResponse)
def index():
    return HTML

@app.post("/api/action")
def action(data: Action):
    # The visualization is generated client-side from the selected action.
    return {"ok": True, "mode": data.mode, "action": data.action}

HTML = r"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Protocol Visualizer</title>
<style>
:root{--bg:#0b1020;--panel:#121a2e;--panel2:#0e1628;--text:#e8eefc;--muted:#91a0bd;--accent:#6ea8fe;--green:#53d18d;--orange:#ffb454;--red:#ff6b6b;--line:#263554}
*{box-sizing:border-box}body{margin:0;background:linear-gradient(135deg,#080d19,#10182a);color:var(--text);font:14px Inter,system-ui,Arial,sans-serif}
header{height:64px;border-bottom:1px solid var(--line);display:flex;align-items:center;padding:0 22px;gap:12px}
.logo{width:32px;height:32px;border-radius:9px;background:linear-gradient(135deg,#6ea8fe,#9b7bff);display:grid;place-items:center;font-weight:800}
h1{font-size:18px;margin:0}.status{margin-left:auto;color:var(--green);font-size:12px}
main{display:grid;grid-template-columns:360px 1fr;gap:16px;padding:16px;min-height:calc(100vh - 64px)}
.panel{background:rgba(18,26,46,.92);border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 10px 30px #0003}
.panel-head{padding:16px 18px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center}
.panel-head strong{font-size:15px}.pill{font-size:11px;color:var(--muted)}
.tabs{display:grid;grid-template-columns:repeat(3,1fr);padding:10px;gap:7px}
.tab{border:1px solid var(--line);background:#0d1424;color:var(--muted);padding:10px;border-radius:9px;cursor:pointer}.tab.active{background:#1b3157;color:#fff;border-color:#3b69a9}
.form{padding:8px 16px 18px}.form-section{display:none}.form-section.active{display:block}
label{display:block;color:var(--muted);font-size:12px;margin:13px 0 6px}input,textarea,select{width:100%;background:#0b1221;border:1px solid var(--line);border-radius:8px;color:var(--text);padding:10px;outline:none}textarea{min-height:125px;resize:vertical}
button{border:0;border-radius:8px;padding:10px 13px;background:#245ca6;color:white;cursor:pointer;font-weight:600}.primary{width:100%;margin-top:14px}.secondary{background:#1b263d;color:#cdd8ef}
.row{display:flex;gap:8px}.row>*{flex:1}
.stream-controls{display:flex;gap:8px;margin-top:14px}.stream-controls button{flex:1}
.quality{margin-top:12px}
.visual{display:flex;flex-direction:column;min-width:0}.toolbar{padding:11px 14px;border-bottom:1px solid var(--line);display:flex;gap:7px;align-items:center}.toolbar button{padding:8px 11px}.counter{margin-left:auto;color:var(--muted);font-size:12px}
.trace{padding:18px;overflow:auto;flex:1}.empty{height:100%;display:grid;place-items:center;color:var(--muted);text-align:center}
.step{border:1px solid var(--line);background:#0c1424;border-radius:10px;margin-bottom:10px;opacity:.25;transform:translateX(8px);transition:.35s}
.step.visible{opacity:1;transform:translateX(0)}.step.current{border-color:#4b7dc4;box-shadow:0 0 0 1px #4b7dc433}
.step-head{display:flex;align-items:center;gap:9px;padding:10px 12px;border-bottom:1px solid var(--line)}.num{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;background:#1d2c49;color:#b9c9e9;font-size:11px}
.dir{font-size:11px;color:var(--accent);margin-left:auto}.proto{font-size:11px;color:var(--orange)}
pre{margin:0;padding:12px;white-space:pre-wrap;color:#cbd6ec;font:12px ui-monospace,SFMono-Regular,Menlo,monospace;line-height:1.5}
.footer{padding:10px 16px;border-top:1px solid var(--line);color:var(--muted);font-size:11px}
@media(max-width:850px){main{grid-template-columns:1fr}.visual{min-height:600px}}
</style>
</head>
<body>
<header><div class="logo">↔</div><h1>Live Protocol Visualizer</h1><div class="status">● local simulation</div></header>
<main>
<section class="panel">
<div class="panel-head"><strong>Activity</strong><span class="pill">User actions → trace</span></div>
<div class="tabs">
<button class="tab active" data-mode="browse">Browsing</button>
<button class="tab" data-mode="mail">Mail</button>
<button class="tab" data-mode="stream">Streaming</button>
</div>
<div class="form">
<div id="browse" class="form-section active">
<label>URL</label><input id="url" value="https://example.com/" placeholder="https://example.com/">
<button class="primary" onclick="runBrowse()">Visit</button>
</div>
<div id="mail" class="form-section">
<label>To</label><input id="to" placeholder="student@example.com">
<label>Subject</label><input id="subject" placeholder="Hello">
<label>Body</label><textarea id="body" placeholder="Write your message..."></textarea>
<button class="primary" onclick="runMail()">Send</button>
</div>
<div id="stream" class="form-section">
<label>Quality</label><select id="quality"><option>360p</option><option>720p</option><option selected>1080p</option><option>4K</option></select>
<div class="stream-controls"><button onclick="runStream('Play')">▶ Play</button><button class="secondary" onclick="runStream('Pause')">Ⅱ Pause</button></div>
</div>
</div>
<div class="footer">Protocol messages are illustrative/simulated; no real network or email traffic is sent.</div>
</section>

<section class="panel visual">
<div class="panel-head"><strong>Live protocol visualizer</strong><span class="pill" id="modeLabel">Waiting for activity</span></div>
<div class="toolbar">
<button onclick="replay()">↻ Replay</button><button onclick="prev()">‹ Previous</button><button onclick="next()">Next ›</button><button id="autoBtn" onclick="toggleAuto()">▶ Auto</button>
<span class="counter" id="counter">0 / 0</span>
</div>
<div class="trace" id="trace"><div class="empty">Choose an activity on the left.<br>The corresponding protocol exchange will appear here step-by-step.</div></div>
</section>
</main>
<script>
let mode='browse', steps=[], index=-1, timer=null, auto=false;
const $=id=>document.getElementById(id);
document.querySelectorAll('.tab').forEach(b=>b.onclick=()=>{mode=b.dataset.mode;document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('active',x===b));document.querySelectorAll('.form-section').forEach(x=>x.classList.toggle('active',x.id===mode));});
function setSteps(label, arr){steps=arr;index=-1;$('modeLabel').textContent=label;$('trace').innerHTML=arr.map((s,i)=>`<div class="step" id="step${i}"><div class="step-head"><span class="num">${i+1}</span><span>${s.title}</span><span class="proto">${s.proto}</span><span class="dir">${s.dir}</span></div><pre>${esc(s.data)}</pre></div>`).join('');$('counter').textContent=`0 / ${arr.length}`;next();}
function esc(s){return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');}
function show(i){if(i<0||i>=steps.length)return;index=i;document.querySelectorAll('.step').forEach((x,j)=>{x.classList.toggle('visible',j<=i);x.classList.toggle('current',j===i)});$('counter').textContent=`${i+1} / ${steps.length}`;document.getElementById('step'+i)?.scrollIntoView({behavior:'smooth',block:'nearest'});}
function next(){if(index<steps.length-1)show(index+1);else stopAuto();}
function prev(){show(Math.max(0,index-1));}
function replay(){stopAuto();if(!steps.length)return;document.querySelectorAll('.step').forEach(x=>x.classList.remove('visible','current'));index=-1;next();}
function toggleAuto(){auto=!auto;$('autoBtn').textContent=auto?'Ⅱ Pause':'▶ Auto';if(auto){if(index>=steps.length-1)replay();timer=setInterval(()=>{if(index<steps.length-1)next();else stopAuto()},850)}else stopAuto();}
function stopAuto(){if(timer)clearInterval(timer);timer=null;auto=false;$('autoBtn').textContent='▶ Auto';}
async function sync(payload){try{await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})}catch(e){}}
function runBrowse(){let u=$('url').value||'https://example.com/';let host;try{host=new URL(u).hostname}catch(e){host='example.com'};sync({mode:'browse',url:u,action:'Visit'});setSteps('Browsing · '+host,[{title:'DNS query',proto:'DNS',dir:'Client → DNS',data:`Transaction ID: 0x4a21\\nFlags: 0x0100 (standard query)\\nQuestions: 1\\nQuery: ${host}  IN  A`},{title:'DNS response',proto:'DNS',dir:'DNS → Client',data:`Transaction ID: 0x4a21\\nFlags: 0x8180 (response)\\nAnswer: ${host}  300  IN  A  93.184.216.34`},{title:'HTTP request',proto:'HTTP/1.1',dir:'Client → Server',data:`GET ${new URL(u).pathname||'/'} HTTP/1.1\\nHost: ${host}\\nUser-Agent: ProtocolVisualizer/1.0\\nAccept: text/html,*/*\\nConnection: keep-alive`},{title:'HTTP response',proto:'HTTP/1.1',dir:'Server → Client',data:`HTTP/1.1 200 OK\\nContent-Type: text/html; charset=UTF-8\\nContent-Length: 1256\\nCache-Control: max-age=300\\n\\n<html>...illustrative response...</html>`}]);}
function runMail(){let to=$('to').value||'student@example.com',sub=$('subject').value||'Hello',body=$('body').value||'Hello';sync({mode:'mail',to,subject:sub,body,action:'Send'});setSteps('Mail · SMTP',[{title:'EHLO',proto:'SMTP',dir:'Client → Mail Server',data:'EHLO client.example\\n250-mail.example\\n250-SIZE 52428800\\n250-STARTTLS'},{title:'MAIL FROM',proto:'SMTP',dir:'Client → Mail Server',data:'MAIL FROM:<sender@example.com>\\n250 2.1.0 OK'},{title:'RCPT TO',proto:'SMTP',dir:'Client → Mail Server',data:`RCPT TO:<${to}>\\n250 2.1.5 OK`},{title:'DATA',proto:'SMTP',dir:'Client → Mail Server',data:`DATA\\n354 End data with <CR><LF>.<CR><LF>\\nTo: ${to}\\nSubject: ${sub}\\n\\n${body}\\n.`},{title:'Message accepted',proto:'SMTP',dir:'Mail Server → Client',data:'250 2.0.0 OK: queued as 9F31A2'},{title:'QUIT',proto:'SMTP',dir:'Client → Mail Server',data:'QUIT\\n221 2.0.0 Bye'}]);}
function runStream(a){let q=$('quality').value;sync({mode:'stream',quality:q,action:a});setSteps(`Streaming · ${q} · ${a}`,[{title:'DNS query',proto:'DNS',dir:'Client → DNS',data:'Query: video.example  IN  A'},{title:'DNS response',proto:'DNS',dir:'DNS → Client',data:'Answer: video.example  60  IN  A  203.0.113.20'},{title:'Manifest request',proto:'HTTP/1.1',dir:'Client → CDN',data:'GET /media/playlist.m3u8 HTTP/1.1\\nHost: video.example\\nAccept: application/vnd.apple.mpegurl'},{title:'Manifest response',proto:'HTTP/1.1',dir:'CDN → Client',data:'#EXTM3U\\n#EXT-X-VERSION:7\\n#EXT-X-TARGETDURATION:4\\n#EXTINF:4.000,\\nseg-001.m4s'},{title:'Segment 1 request',proto:'HTTP/1.1',dir:'Client → CDN',data:'GET /media/1080p/seg-001.m4s HTTP/1.1\\nRange: bytes=0-1048575'},{title:'Segment 1 response',proto:'HTTP/1.1',dir:'CDN → Client',data:'HTTP/1.1 206 Partial Content\\nContent-Type: video/mp4\\nContent-Length: 1048576'},{title:'Segment 2 request',proto:'HTTP/1.1',dir:'Client → CDN',data:'GET /media/1080p/seg-002.m4s HTTP/1.1\\nRange: bytes=0-1048575'},{title:'Segment 2 response',proto:'HTTP/1.1',dir:'CDN → Client',data:'HTTP/1.1 206 Partial Content\\nContent-Type: video/mp4\\nContent-Length: 1048576'}]);}
</script>
</body></html>"""
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
