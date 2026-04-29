const canvas = document.getElementById('board');
const context = canvas.getContext('2d');
const status = document.getElementById('status');
let socket;
document.getElementById('join').addEventListener('submit', event => {
  event.preventDefault();
  if (socket) socket.close();
  const params = new URLSearchParams({room:document.getElementById('room').value,name:document.getElementById('name').value});
  const current = new WebSocket(`${location.protocol==='https:'?'wss':'ws'}://${location.host}/ws?${params}`);
  socket = current;
  current.onopen = () => { status.textContent = 'Connected. Collect the coins!'; };
  current.onclose = () => { if(socket===current) status.textContent = 'Disconnected. Join again to reconnect.'; };
  current.onerror = () => { status.textContent = 'Connection failed.'; };
  current.onmessage = event => {
    const data = JSON.parse(event.data);
    if(data.error) { status.textContent = data.error; return; }
    const cell = canvas.width / data.size;
    context.fillStyle='#eff3fa';context.fillRect(0,0,500,500);
    context.strokeStyle='#dce3ed';
    for(let i=0;i<=data.size;i++){context.beginPath();context.moveTo(i*cell,0);context.lineTo(i*cell,500);context.moveTo(0,i*cell);context.lineTo(500,i*cell);context.stroke();}
    context.fillStyle='#e5b820';
    for(const [x,y] of data.coins){context.beginPath();context.arc((x+.5)*cell,(y+.5)*cell,cell*.25,0,Math.PI*2);context.fill();}
    for(const [id,player] of Object.entries(data.players)) {
      context.fillStyle=player.color;context.fillRect(player.x*cell+3,player.y*cell+3,cell-6,cell-6);
      if(id===data.you){context.strokeStyle='#17243c';context.lineWidth=2;context.strokeRect(player.x*cell+2,player.y*cell+2,cell-4,cell-4);context.lineWidth=1;}
    }
    const scores=document.getElementById('scores');scores.replaceChildren();
    for(const player of Object.values(data.players).sort((a,b)=>b.score-a.score)){const li=document.createElement('li');li.textContent=`${player.name}: ${player.score}`;scores.appendChild(li);}
  };
});
function move(direction){if(socket && socket.readyState===WebSocket.OPEN)socket.send(JSON.stringify({direction}));}
document.addEventListener('keydown', event => {
  if(['INPUT','TEXTAREA'].includes(event.target.tagName))return;
  const keys={ArrowUp:'up',w:'up',ArrowDown:'down',s:'down',ArrowLeft:'left',a:'left',ArrowRight:'right',d:'right'};
  if(keys[event.key]){event.preventDefault();move(keys[event.key]);}
});
document.querySelectorAll('[data-direction]').forEach(button=>button.addEventListener('click',()=>move(button.dataset.direction)));
document.getElementById('leave').addEventListener('click',()=>{if(socket)socket.close();});
