<h1 align="center">
  🧠 Warmth — 情感沟通助手
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.1.0-f5b878" alt="Version">
  <img src="https://img.shields.io/badge/platform-Windows-blue" alt="Platform">
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status">
  <img src="https://img.shields.io/github/license/nutshell319/emotional-agent" alt="License">
</p>

<p align="center">
  <strong>基于 DeepSeek LLM 的情感沟通对话助手</strong><br>
  多人格切换 · 情绪感知 · 记忆脑图 · 浅色/深色主题 · Windows 桌面应用
</p>

<p align="center">
  <a href="https://github.com/nutshell319/emotional-agent/releases/latest"><strong>⬇️ 下载安装包</strong></a>
  &nbsp;·&nbsp;
  <a href="https://nutshell319.github.io/emotional-agent/">🌐 在线版</a>
  &nbsp;·&nbsp;
  <a href="#-快速开始">快速开始</a>
  &nbsp;·&nbsp;
  <a href="#-功能特性">功能特性</a>
</p>

---

## 📥 下载安装

> **v2.1.0** — 第二版：多人格 + 情绪感知 + 视觉焕新

| 平台 | 下载 | 说明 |
|------|------|------|
| 🪟 **Windows** | [**Warmth Setup 2.1.0.exe**](https://github.com/nutshell319/emotional-agent/releases/latest) | NSIS 安装包，可选安装路径，自动创建快捷方式 |
| 🌐 **在线版** | [nutshell319.github.io/emotional-agent](https://nutshell319.github.io/emotional-agent/) | 浏览器直接打开，无需安装 |

> 💡 **覆盖安装**：同路径安装会自动升级，保留所有对话数据和设置（存储在 AppData 中，不在安装目录）。

### 自己构建

```bash
git clone https://github.com/nutshell319/emotional-agent.git
cd emotional-agent
npm install
npm run build        # 输出: dist/Warmth Setup 2.1.0.exe
```

---

## ✨ 为什么做这个

每个人都会遇到说不清、想不通、放不下的感情困扰。  
朋友可能没空听，家人可能不理解，心理咨询又太贵。

Warmth 是一个**随时在线**的倾听者——温暖但不说教，专业但不冰冷，隐私完全由你掌控。

---

## 🎯 核心功能

### 💬 对话体验
| 功能 | 说明 |
|------|------|
| 🎭 **四人**格切换 | 毒舌闺蜜 / 暖心姐姐 / 理性军师 / 温柔树洞，一键切换 AI 性格 |
| 💬 **智能对话** | 基于 DeepSeek 等大模型，流式逐字输出，懂中文、会共情 |
| 🎬 **思考→回复过渡** | "正在理解你…→想到了→开始说"，三阶段自然衔接 |
| ⌨️ **三段式变速打字** | 开头慢（斟酌措辞）→ 中间快（流畅输出）→ 结尾慢（收尾确认） |
| 🎨 **文本自然变异** | 随机口语词、标点软化、停顿标记——读起来不像机器写的 |
| ✨ **分段打字机动画** | 回复自动分段，逐字打字，头像跟随最新段落 |
| 🌓 **浅色/深色主题** | 一键切换，侧边栏底部按钮 |

### 🧠 智能感知
| 功能 | 说明 |
|------|------|
| 💜 **情绪状态追踪** | 实时检测 4 维情绪（难过/愤怒/焦虑/平静）+ 过渡态惯性 |
| 📈 **情绪演化感知** | 比较历史消息，感知情绪变化趋势（"你在好转"/"越来越差了"） |
| 🔗 **话题回溯** | 自动检测历史话题关联，自然地接回之前聊过的内容 |
| 🎯 **风格一致性 RAG** | 检索类似情境的历史回复，保持 AI 风格统一 |
| 🛡 **防幻觉机制** | System Prompt 内置事实底线，严禁编造用户未说过的事 |
| 🚫 **领域预检** | 非情感问题本地拒绝，0 token 消耗 |
| 🗜 **上下文压缩** | 超过 20 轮对话自动摘要，保留关键信息 |

### 👤 用户画像 & 记忆
| 功能 | 说明 |
|------|------|
| 👤 **用户画像** | 自动提取性格、MBTI、经历等稳定特质，跨会话记忆 |
| 💜 **对象画像** | 描述你在意的人（MBTI、星座、关系状态），精准分析 |
| 🧠 **记忆脑图** | 侧边栏展开浮动大窗，记忆节点放射状分布，分类彩色标注 |
| 🔄 **语义去重** | 相似记忆自动合并，超 20 条 LLM 自动提炼 |
| 🎯 **实体混淆防护** | 区分"我的特质"和"TA 的特质"，不会把对象的属性错误归到用户 |

### 🔧 工具 & 安全
| 功能 | 说明 |
|------|------|
| 🔍 **截图识别** | 粘贴或上传聊天截图，OCR 自动识别文字 |
| 📥 **导出导入** | JSON 文件备份，换设备一键恢复 |
| 💾 **数据自主** | 所有数据存浏览器 localStorage，隐私全本地 |
| 🖥 **桌面应用** | Electron 打包，独立窗口运行，绕过 CORS 限制 |
| 🚀 **启动引导屏** | 渐变圆角图标 + "欢迎回来"，丝滑过渡无闪烁 |

---

## 🚀 快速开始

### 方式一：下载安装包（推荐）

👉 **[最新 Release](https://github.com/nutshell319/emotional-agent/releases/latest)** → 下载 `Warmth Setup 2.1.0.exe` → 双击安装

### 方式二：在线使用

👉 **[在线版](https://nutshell319.github.io/emotional-agent/)** — 浏览器打开即用

### 方式三：本地运行

```bash
git clone https://github.com/nutshell319/emotional-agent.git
cd emotional-agent
npm install
npm start
```

### 配置 API

1. 点击右上角 ⚙ 或按 `Ctrl+,` 打开设置
2. 填入 [DeepSeek API Key](https://platform.deepseek.com/api_keys)
3. 默认模型 `deepseek-v4-flash`，支持切换到其他兼容 API

---

## ⌨️ 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl + N` | 新建对话 |
| `Ctrl + ,` | 打开设置 |
| `Esc` | 关闭面板 |
| `Enter` | 发送消息 |
| `Shift + Enter` | 换行 |

---

## 🧱 技术栈

| 层 | 技术 |
|----|------|
| 前端 | 纯原生 HTML/CSS/JS，零依赖（~5000 行单文件） |
| LLM | DeepSeek / 豆包 / 任意 OpenAI 兼容 API |
| OCR | 百度 OCR API（免费 5 万次/天） |
| 存储 | localStorage + JSON 文件 |
| 桌面端 | Electron 28 |
| 部署 | GitHub Pages（Actions 自动化部署） |
| 主题 | 深色/浅色双模式，4 人格各一套配色 |

---

## 📁 项目结构

```
emotional-agent/
├── index.html              ← 主程序（单文件 ~5000 行，CSS/JS 全部内联）
├── main.js                 ← Electron 主进程
├── package.json            ← Electron 28 + electron-builder 打包配置
├── icon.ico                ← 应用图标
├── README.md               ← 本文件
├── .npmrc                  ← 国内 npm 镜像配置
├── .gitignore
├── assets/
│   └── icon.svg            ← 原始图标 SVG
├── scripts/
│   ├── make-portable.js    ← 便携版构建脚本
│   └── vision.js           ← 千问 VL 识图脚本
├── .github/workflows/
│   └── pages.yml           ← GitHub Actions Pages 自动部署
└── docs/superpowers/        ← 设计规格与实施计划
```

---

## 🔒 隐私说明

- API Key 仅存浏览器 localStorage，**不上传任何服务器**
- 所有对话数据存在本地，清除浏览器数据即彻底删除
- 覆盖安装升级时，对话数据不受影响（存储在 AppData 中，不在安装目录）
- 建议定期使用「导出备份」功能保存重要对话

---

## 📄 License

MIT © [nutshell319](https://github.com/nutshell319)

---

<p align="center">
  <sub>感到孤独的时候，记得有 Warmth 在 💜</sub>
</p>
