const http = require('http');
const { spawn } = require('child_process');

async function run() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9245',
    '--disable-gpu',
    '--no-sandbox'
  ]);
  
  await new Promise(r => setTimeout(r, 1500));
  
  try {
    const listRes = await fetch('http://127.0.0.1:9245/json/new', { method: 'PUT' });
    const tab = await listRes.json();
    const ws = new WebSocket(tab.webSocketDebuggerUrl);
    
    await new Promise(resolve => {
      ws.onopen = resolve;
    });

    let msgId = 1;
    function send(method, params = {}) {
      const id = msgId++;
      return new Promise(resolve => {
        const handler = (e) => {
          const data = JSON.parse(e.data);
          if (data.id === id) {
            ws.removeEventListener('message', handler);
            resolve(data.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id, method, params }));
      });
    }

    ws.addEventListener('message', (e) => {
      const data = JSON.parse(e.data);
      if (data.method === 'Runtime.consoleAPICalled') {
        console.log('[BROWSER CONSOLE]', data.params.type, data.params.args.map(a => a.value).join(' '));
      } else if (data.method === 'Runtime.exceptionThrown') {
        console.log('[BROWSER EXCEPTION]', data.params.exceptionDetails.text, data.params.exceptionDetails.exception?.description);
      }
    });

    await send('Page.enable');
    await send('Runtime.enable');
    
    console.log('Navigating to canvas_xaydungphuluc.html...');
    await send('Page.navigate', { url: 'file:///c:/Users/HoangThien/Documents/GitHub/giangbai/canvas_xaydungphuluc.html' });
    
    await new Promise(r => setTimeout(r, 2000));
    
    const evalRes = await send('Runtime.evaluate', {
      expression: (() => {
        const modal = document.querySelector('.modal:not(.hidden)');
        const prog = document.querySelector('.progress-container:not(.hidden)');
        const btn = document.querySelector('#generateAll');
        const subject = document.querySelector('#subject');
        const rect = btn?.getBoundingClientRect();
        const topEl = rect ? document.elementFromPoint(rect.left + 5, rect.top + 5)?.outerHTML.slice(0, 100) : null;
        return {
          hasOpenModal: !!modal,
          modalId: modal?.id,
          hasOpenProgress: !!prog,
          subjectOptions: subject?.options?.length,
          topElementAtBtn: topEl,
          bannerText: document.getElementById('canvasHostBanner')?.textContent,
          bannerClass: document.getElementById('canvasHostBanner')?.className
        };
      })(),
      returnByValue: true
    });
    
    console.log('EVAL RESULT:', JSON.stringify(evalRes?.result?.value, null, 2));
    
    ws.close();
    chrome.kill();
  } catch (err) {
    console.error('ERROR:', err);
    chrome.kill();
  }
}
run();
