const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

const PORT = 3456;
const MIME = { '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css' };

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

  if (req.url.startsWith('/proxy/baidu/')) {
    const target = 'https://aip.baidubce.com' + req.url.replace('/proxy/baidu', '');
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      https.request(target, { method: req.method, headers: { 'Content-Type': req.headers['content-type'] || '' } }, pr => {
        res.writeHead(pr.statusCode, pr.headers);
        pr.pipe(res);
      }).on('error', e => { res.writeHead(502); res.end(e.message); }).write(body).end();
    });
    return;
  }

  let fp = req.url === '/' ? '/index.html' : req.url.split('?')[0];
  fp = path.join(__dirname, fp);
  fs.readFile(fp, (err, data) => {
    if (err) { res.writeHead(404); res.end('Not Found'); return; }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(fp)] || 'text/plain' });
    res.end(data);
  });
});

server.listen(PORT, () => console.log('http://localhost:' + PORT));
