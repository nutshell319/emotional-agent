const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');

let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 960,
    height: 600,
    minWidth: 720,
    minHeight: 450,
    backgroundColor: '#08090d',
    title: 'Warmth',
    icon: path.join(__dirname, 'icon.ico'),
    webPreferences: {
      webSecurity: false,
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  Menu.setApplicationMenu(null);
  mainWindow.loadFile('index.html');
  mainWindow.maximize();

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
