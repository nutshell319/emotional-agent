const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  maximize: () => ipcRenderer.send('maximize-window'),
});
