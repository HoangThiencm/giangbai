const { spawn } = require('child_process');
async function run() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9248',
    '--disable-gpu',
    '--no-sandbox'
  ]);
  await new Promise(r => setTimeout(r, 1500));
  try {
    const listRes = await fetch('http://127.0.0.1:9248/json/new', { method: 'PUT' });
    const tab = await listRes.json();
    const ws = new WebSocket(tab.webSecketDebuggerUrl);
    await new Promise(r => { ws.onopen = r; });
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
    ws.addEventListener('message', e => {
      const data = JSON.parse(e.data);
      if (data.method === 'Runtime.consoleAPICalled') {
        console.log('[CONSOLE]', data.params.type, data.params.args.map(a => a?.value).join(' '));
      } else if (data.method === 'Runtime.exceptionThrown') {
        console.log('[EXCEPTION]', data.params.exceptionDetails.text, data.params.exceptionDetails.exception?.description);
      }
    });
    await send('Page.enable');
    await send('Runtime.enable');
    await send('Page.navigate', { url: 'file:///c:/Users/HoangThien/Documents/GitHub/giangbai/canvas_xaydungphuluc.html' });
    await new Promise(r => setTimeout(r, 3000));
    const r = await send('Runtime.evaluate', {
      expression: 'JSON.stringify({ modals: document.querySelectorAll(".modal:not(.hidden)").length, subjects: document.getElementById("subject")?.options.length, banner: document.getElementById("canvasHostBanner")?.textContent, progress: document.querySelectorAll(".progress-container:not(.hidden)").length })',
      returnByValue: true
    });
    console.log('CHECK RESULT:', r.result.value);
    ws.close();
    chrome.kill();
  } catch (e) {
    console.error(e);
    chrome.kill();
  }
}
run();
