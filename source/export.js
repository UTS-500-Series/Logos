const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const O=path.join(__dirname,'out');
const jobs=[['uts500-mark.svg',[128,256,512,1024]],['uts500-mark-flat.svg',[512]],['favicon.svg',[16,32,48,180,192,512]],
 ['discord-server-icon.svg',[512,1024]],['discord-bot-avatar.svg',[512,1024]]];
const wide=['uts500-lockup-light.svg','uts500-lockup-dark.svg','uts500-lockup-stacked-light.svg','uts500-lockup-stacked-dark.svg','site-lockup-light.svg','site-lockup-dark.svg'];
(async()=>{const b=await chromium.launch();const p=await b.newPage();
 const shot=async(f,w,h,out)=>{await p.setViewportSize({width:w,height:h});
  await p.setContent(`<html><body style="margin:0;background:transparent"><img src="data:image/svg+xml;base64,${fs.readFileSync(path.join(O,f)).toString('base64')}" width="${w}" height="${h}" style="display:block"></body></html>`);
  await p.screenshot({path:path.join(O,'png',out),omitBackground:true});};
 fs.mkdirSync(path.join(O,'png'),{recursive:true});
 for(const [f,sizes] of jobs) for(const s of sizes) await shot(f,s,s,f.replace('.svg',`-${s}.png`));
 for(const f of wide){const m=fs.readFileSync(path.join(O,f),'utf8').match(/viewBox="0 0 (\d+) (\d+)"/);
  const w=+m[1],h=+m[2],H=400,W=Math.round(w*H/h); await shot(f,W,H,f.replace('.svg','-400h.png'));}
 await b.close();})();
