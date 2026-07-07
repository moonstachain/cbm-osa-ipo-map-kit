<!-- MAPKIT_GATE_V1 · 自愈访问门 (sha256 only) -->
<script>
(function(){
  var HASH='CHANGE_ME_SHA256_OF_YOUR_PASSPHRASE', KEY='mapkit_auth_v1';
  var unlocked=false,node=null,pH='',pB='';
  try{if(localStorage.getItem(KEY)===HASH)unlocked=true}catch(e){}
  function sha(s){return crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)).then(function(b){return Array.from(new Uint8Array(b)).map(function(x){return x.toString(16).padStart(2,'0')}).join('')})}
  function build(){var ov=document.createElement('div');ov.id='og-gate';
    ov.setAttribute('style','position:fixed;inset:0;z-index:2147483647;display:flex;align-items:center;justify-content:center;background:#08090b;color:#f1ece1;font-family:\'Noto Serif SC\',serif');
    ov.innerHTML='<div style="width:min(380px,88vw);padding:36px 32px;background:#13151a;border:1px solid #26282f;border-radius:4px"><h2 style="margin:0 0 8px;font-size:18px;font-weight:500;color:#c9a96a">本OS组织能力 · 战略地图</h2><div style="margin:0 0 28px;font-size:11px;color:#6c7080;font-family:monospace;letter-spacing:.08em">ORG-CAPABILITY STRATEGY MAP · ACCESS</div><input id="og-pwd" type="password" placeholder="访问密码" autocomplete="off" style="width:100%;box-sizing:border-box;padding:12px 14px;font-size:15px;background:#08090b;color:#f1ece1;border:1px solid #26282f;border-radius:3px;font-family:monospace;letter-spacing:.08em;outline:none"/><button id="og-ok" style="width:100%;margin-top:14px;padding:11px;font-size:14px;font-weight:500;background:#c9a96a;color:#08090b;border:none;border-radius:3px;cursor:pointer">进入 / Enter</button><div id="og-err" style="margin-top:10px;font-size:12px;color:#c97a72;min-height:16px"></div><a href="/#matrix" style="display:block;margin-top:18px;text-align:center;font-size:11px;color:#5f6f67;font-family:monospace">&larr; 返回应用矩阵</a></div>';
    var p=ov.querySelector('#og-pwd'),er=ov.querySelector('#og-err'),b=ov.querySelector('#og-ok');
    function go(){var v=p.value;if(!v){er.textContent='请输入密码';return}sha(v).then(function(h){if(h===HASH){try{localStorage.setItem(KEY,h)}catch(e){}unlocked=true;drop()}else{er.textContent='密码错误';p.value=''}})}
    b.addEventListener('click',go);p.addEventListener('keypress',function(e){if(e.key==='Enter')go()});return ov}
  function lock(){var h=document.documentElement,b=document.body;if(h&&h.style.overflow!=='hidden'){pH=h.style.overflow;h.style.overflow='hidden'}if(b&&b.style.overflow!=='hidden'){pB=b.style.overflow;b.style.overflow='hidden'}}
  var sr=false;function drop(){if(node&&node.parentNode)node.parentNode.removeChild(node);node=null;if(!sr){if(document.documentElement)document.documentElement.style.overflow=pH;if(document.body)document.body.style.overflow=pB;sr=true}}
  function ensure(){if(unlocked){drop();return}var r=document.body||document.documentElement;if(!r)return;if(!node||!node.parentNode){node=build();r.appendChild(node);lock();var p=node.querySelector('#og-pwd');if(p)setTimeout(function(){p.focus()},60)}}
  ensure();setInterval(ensure,200);document.addEventListener('DOMContentLoaded',ensure);
})();
</script>