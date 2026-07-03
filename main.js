const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');

let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 420,
    height: 750,
    minWidth: 380,
    minHeight: 600,
    title: '小心',
    icon: path.join(__dirname, 'icon.ico'),
    webPreferences: {
      webSecurity: false,       // 允许跨域请求（百度OCR等）
      nodeIntegration: false,   // 安全：网页不直接访问Node
      contextIsolation: true,
    },
  });

  // 隐藏菜单栏
  Menu.setApplicationMenu(null);

  mainWindow.loadFile('index.html');

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
