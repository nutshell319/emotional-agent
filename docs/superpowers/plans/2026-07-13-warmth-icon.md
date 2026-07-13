# Warmth 图标与应用名更新 — 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 生成橘猫 ICO 图标，重命名应用为 Warmth

**Architecture:** Python + Pillow 程序化绘制图标（避免 SVG→PNG 依赖），打包为多尺寸 ICO

**Tech Stack:** Python 3.12, Pillow, 纯 Python（无外部渲染库依赖）

---

### Task 1: 安装 Pillow 并保存 SVG 源文件

**Files:**
- Create: `assets/icon.svg`
- Install: Pillow (pip)

- [ ] **Step 1: 安装 Pillow**

```bash
pip install Pillow
```

- [ ] **Step 2: 保存 SVG 源文件**

写入 `assets/icon.svg`（最终确认的 v4 A 版 SVG）。

---

### Task 2: 生成图标文件

**Files:**
- Create: `scripts/generate_icon.py`
- Create: `icon.ico`
- Create: `icon.png`

- [ ] **Step 1: 编写图标生成脚本**

`scripts/generate_icon.py` — 用 Pillow ImageDraw 程序化绘制猫头图标，渲染多个尺寸，打包为 ICO 和 PNG。

脚本逻辑：
1. 定义绘制函数 `draw_cat(draw, size)` — 按比例缩放所有几何元素
2. 在 256×256 画布上绘制 → 保存为 `icon.png`
3. 渲染 16, 24, 32, 48, 64, 128, 256 七个尺寸
4. 打包为多尺寸 ICO

- [ ] **Step 2: 运行脚本生成图标**

```bash
cd "C:\programs\个人项目\emotional-agent"
python scripts/generate_icon.py
```

预期：`icon.ico` 和 `icon.png` 生成成功。

- [ ] **Step 3: 验证 ICO 包含所有尺寸**

```bash
python -c "from PIL import Image; img=Image.open('icon.ico'); print('ICO sizes:', [s.size for s in img.encoderinfo.get('sizes',[])] if hasattr(img,'encoderinfo') else 'check manually')"
```

- [ ] **Step 4: 提交**

```bash
git add assets/icon.svg scripts/generate_icon.py icon.ico icon.png
git commit -m "✨ 新图标：暖橘简约猫头，Python生成多尺寸ICO"
```

---

### Task 3: 更新应用名称（小心 → Warmth）

**Files:**
- Modify: `package.json`
- Modify: `index.html`

- [ ] **Step 1: 更新 package.json**

```json
{
  "name": "warmth",
  "version": "2.0.0",
  "description": "Warmth — 情感沟通助手",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "build": "electron-builder --win portable"
  },
  "build": {
    "appId": "com.warmth.emotional-agent",
    "productName": "Warmth",
    "win": {
      "target": "portable",
      "icon": "icon.ico"
    }
  },
  "devDependencies": {
    "electron": "^28.2.1",
    "electron-builder": "^24.0.0"
  }
}
```

- [ ] **Step 2: 更新 index.html 标题**

`<title>` 改为 "Warmth"；页面内显示的 "小心" 改为 "Warmth"。

- [ ] **Step 3: 提交**

```bash
git add package.json index.html
git commit -m "🏷️ 应用更名：小心 → Warmth，版本号 2.0.0"
```

---

### Task 4: 更新 README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 更新 README 标题和引用**

- `<h1>` 标题：`👧🏻 小暖 — 情感沟通助手` → `🐱 Warmth — 情感沟通助手`
- 描述中的 "小暖" → "Warmth"
- 桌面应用说明中 productName 参考更新
- 末尾文案更新

- [ ] **Step 2: 提交**

```bash
git add README.md
git commit -m "📝 README更新：应用名改为Warmth"
```

---

### Task 5: 验证

- [ ] **Step 1: 检查 ICO 视觉效果**

```bash
# 打开 icon.png 查看
start icon.png
```

确认不同缩放级别下猫头特征可辨认。

- [ ] **Step 2: Electron 验证（可选）**

```bash
npm start
```

确认窗口图标和任务栏图标显示新猫头。

- [ ] **Step 3: 推送**

```bash
git push
```
