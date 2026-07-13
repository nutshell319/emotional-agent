# Warmth 应用图标设计规格

## 概述

将 emotional-agent 应用图标从 Electron 默认图标替换为暖系简约橘猫头像，同时将应用名从 "小心" 更改为 "Warmth"。

## 应用名称

- **新名称**：Warmth
- **产品名**（Electron productName）：Warmth
- **应用 ID**：com.warmth.emotional-agent

## 图标设计

### 视觉方案

暖橘色扁平简约猫头，圆角钝耳 + W 形猫嘴，温暖可爱但不繁杂。

### 颜色

| 元素 | 色值 |
|------|------|
| 猫头/耳朵 | #f5b878 (暖橘) |
| 内耳 | #f0a0a0 (粉，45% 透明) |
| 眼睛 | #1a0804 (深棕黑) |
| 眼高光 | #ffffff |
| 腮红 | #ffb0a0 (45% 透明) |
| 鼻头 | #e09080 |
| 嘴线 | #d4a080 |
| 胡须 | #e8b898 |

### 设计元素

- 圆角钝耳（贝塞尔曲线，无缝融入头部圆形）
- 大圆眼 + 单点白色高光
- 粉色圆形腮红（左右各一）
- 粉色椭圆鼻头
- W 形猫嘴（竖线 + 左右弧线）
- 左右各两根胡须
- 投影阴影（feDropShadow, dy=3, stdDeviation=4, opacity=0.25）
- 无渐变、无高光，纯色扁平风

### SVG 源文件

文件：`assets/icon.svg`
视图框：0 0 256 256

## 实施任务

### 1. 生成图标文件

- 将 SVG 转为多尺寸 ICO（16, 24, 32, 48, 64, 128, 256 px）
- 同时生成 PNG（用于 README 等展示）
- 工具：Python + Pillow / cairosvg，或 ImageMagick

### 2. 更新应用名称

- `package.json`：name → "warmth", productName → "Warmth", appId → "com.warmth.emotional-agent"
- `index.html`：页面标题改为 "Warmth"
- `README.md`：标题和相关描述更新
- 其他引用到 "小心"/"小暖" 的地方统一改为 "Warmth"

### 3. 验证

- 检查 ICO 在所有尺寸下的辨识度
- `npm start` 验证 Electron 窗口图标
- 确认 GitHub Pages 图标正常显示

## 交付物

- `icon.ico` — 多尺寸 Windows 图标
- `icon.png` — 256×256 PNG
- `assets/icon.svg` — SVG 源文件
- 更新的 `package.json` / `index.html` / `README.md`
