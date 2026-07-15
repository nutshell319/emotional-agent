const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');

let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 960,
    height: 600,
    minWidth: 720,
    minHeight: 450,
    // 16:10 横屏比例，适配 Windows 桌面使用场景
    title: 'Warmth',
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
  mainWindow.maximize(); // 启动时最大化窗口

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
