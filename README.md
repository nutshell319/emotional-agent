<h1 align="center">
  👧🏻 小心 — 情感沟通助手
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status">
  <img src="https://img.shields.io/github/license/nutshell319/emotional-agent" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-purple" alt="PRs">
</p>

<p align="center">
  一个基于 LLM 的情感沟通对话助手。<br>
  倾听你的困扰，理解你的情绪，陪你一起找到答案。
</p>

---

## ✨ 为什么做这个

每个人都会遇到说不清、想不通、放不下的感情困扰。  
朋友可能没空听，家人可能不理解，心理咨询又太贵。

小暖是一个**随时在线**的倾听者——温暖但不说教，专业但不冰冷，隐私完全由你掌控。

---

## 🎯 核心功能

| 功能 | 说明 |
|------|------|
| 💬 **智能对话** | 基于 DeepSeek/豆包等大模型，流式逐字输出，懂中文、会共情 |
| 👤 **用户画像** | 自动从对话中提取你的性格、MBTI、经历等稳定特质，跨会话记忆 |
| 💜 **对象画像** | 为每段对话描述你在意的人（MBTI、星座、关系状态），精准聚焦分析 |
| 🧠 **记忆管理** | 自动提取关键信息，支持查看/清除已提取的记忆，防止跨对话泄漏 |
| 🔍 **截图识别** | 粘贴或上传聊天截图，OCR 自动识别文字内容，分析对话中的情感问题 |
| ✨ **分段打字机动画** | Agent 回复自动分段，逐字打字输出，头像跟随最新段落，流畅自然 |
| 🛡 **防幻觉机制** | 系统 prompt 内置事实底线约束，严禁 AI 编造用户未说过的事 |
| 🚫 **领域预检** | 非情感问题本地拒绝，0 token 消耗 |
| 🗜 **上下文压缩** | 超过 20 轮对话自动摘要，保留关键信息不丢 |
| 💾 **数据自主** | 所有数据存浏览器 localStorage，你的秘密只有你知道 |
| 📥 **导出导入** | JSON 文件备份，换设备一键恢复 |
| 🖥 **桌面应用** | Electron 打包，独立窗口运行，绕过浏览器 CORS 限制 |
| ✏️ **自定义昵称** | 想叫她什么就叫什么 |

---

## 🚀 快速开始

### 在线使用

👉 **[nutshell319.github.io/emotional-agent](https://nutshell319.github.io/emotional-agent/)**

打开即用，无需安装。

### 本地运行

```bash
git clone https://github.com/nutshell319/emotional-agent.git
cd emotional-agent
# 双击 index.html 即可，或用浏览器打开
open index.html
```

### 桌面应用（Electron）

```bash
npm install
npm start
```

桌面版自动绕过 CORS 限制，无需额外配置代理。

### 配置 API

1. 点击右上角 ⚙ 或按 `Ctrl+,` 打开设置
2. 填入 DeepSeek API Key（[获取地址](https://platform.deepseek.com/api_keys)）
3. 默认模型 `deepseek-v4-flash`，支持切换豆包/GPT 等兼容 API

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
| 前端 | 纯原生 HTML/CSS/JS，零依赖 |
| LLM | DeepSeek / 豆包 / 任意 OpenAI 兼容 API |
| OCR | 百度 OCR API（免费 5 万次/天） |
| 存储 | localStorage + JSON 文件 |
| 桌面端 | Electron 28 |
| 部署 | GitHub Pages（Actions 自动化部署） |
| 主题 | 深色紫红配色（#08090d / #b98eff / #e85d75） |

---

## 📁 项目结构

```
emotional-agent/
├── index.html              ← 主程序（单文件，CSS/JS 全部内联）
├── main.js                 ← Electron 主进程
├── package.json            ← Electron 依赖与打包配置
├── README.md               ← 本文件
├── CLAUDE.md               ← AI 辅助开发说明
├── .npmrc                  ← 国内 npm 镜像配置
├── .gitignore
├── .github/workflows/
│   └── pages.yml           ← GitHub Actions Pages 自动部署
├── docs/superpowers/
│   ├── specs/               ← 设计规格
│   └── plans/               ← 实施计划
└── 2026-06-30-emotional-agent-design.md  ← 原始设计文档
```

---

## 🔒 隐私说明

- API Key 仅存浏览器 localStorage，**不上传任何服务器**
- 所有对话数据存在本地，清除浏览器数据即彻底删除
- OCR 截图通过百度 OCR API 处理，仅传输图片文字识别所需数据
- 建议定期使用「导出备份」功能保存重要对话
- 使用 GitHub Pages 托管，页面本身是纯静态文件，无后端无数据库

---

## 📄 License

MIT © [nutshell319](https://github.com/nutshell319)

---

<p align="center">
  <sub>感到孤独的时候，记得有小暖在 💜</sub>
</p>
