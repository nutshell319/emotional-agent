const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');

let mainWindow = null;

function createWindow() {
  const t0 = Date.now();
  console.log('[Main] createWindow start');

  mainWindow = new BrowserWindow({
    width: 960,
    height: 600,
    minWidth: 720,
    minHeight: 450,
    show: false,
    backgroundColor: '#08090d',
    title: 'Warmth',
    icon: path.join(__dirname, 'icon.ico'),
    webPreferences: {
      webSecurity: false,
      nodeIntegration: false,
      contextIsolation: true,
    },
  });
  console.log('[Main] BrowserWindow created +' + (Date.now() - t0) + 'ms');

  Menu.setApplicationMenu(null);
  mainWindow.loadFile('index.html');
  console.log('[Main] loadFile called +' + (Date.now() - t0) + 'ms');

  mainWindow.once('ready-to-show', () => {
    console.log('[Main] ready-to-show +' + (Date.now() - t0) + 'ms');
    mainWindow.maximize();
    console.log('[Main] maximize done +' + (Date.now() - t0) + 'ms');
    mainWindow.show();
    console.log('[Main] show() done +' + (Date.now() - t0) + 'ms');
  });

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
